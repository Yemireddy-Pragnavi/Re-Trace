create extension if not exists pgcrypto with schema extensions;
create schema if not exists retrace_private;
revoke all on schema retrace_private from public, anon;
grant usage on schema retrace_private to authenticated, service_role;

create table public.profiles (
 id uuid primary key references auth.users(id) on delete cascade,
 email text not null, role text not null default 'INVESTIGATOR' check (role in ('ADMIN','INVESTIGATOR','VIEWER')),
 created timestamptz not null default now()
);
create table public.cases (
 id uuid primary key default gen_random_uuid(), title text not null check (length(title) between 3 and 160),
 description text not null default '' check(length(description)<=3000), owner uuid not null references public.profiles(id),
 created timestamptz not null default now()
);
create table public.case_members (case_id uuid references public.cases(id),user_id uuid references public.profiles(id), primary key(case_id,user_id));
create table public.evidence_sources (
 id uuid primary key default gen_random_uuid(),case_id uuid not null references public.cases(id),name text not null,
 media text not null,kind text not null check(kind in ('image','file')),size bigint not null check(size between 1 and 8388608),
 hash text not null check(length(hash)=64),storage_path text not null unique,created timestamptz not null default now()
);
create table public.jobs (
 id uuid primary key default gen_random_uuid(),case_id uuid not null references public.cases(id),actor uuid not null references public.profiles(id),
 module text not null check(module in ('drive','files','recovery','validation','benchmark')),status text not null check(status in ('RUNNING','COMPLETED','FAILED','INTERRUPTED')),
 created timestamptz not null default now(),result jsonb not null default '{}'
);
create table public.recovered_files (
 id uuid primary key default gen_random_uuid(),case_id uuid not null references public.cases(id),job_id uuid not null references public.jobs(id),
 storage_path text not null unique,details jsonb not null,created timestamptz not null default now()
);
create table public.audit_events (
 sequence bigint generated always as identity primary key,id uuid not null unique default gen_random_uuid(),case_id uuid references public.cases(id),
 body jsonb not null,canonical_payload text not null,previous_hash text not null,hash text not null,created timestamptz not null default now()
);
create table public.reports (
 id uuid primary key default gen_random_uuid(),case_id uuid not null references public.cases(id),created timestamptz not null default now(),
 envelope jsonb not null,pdf_hash text not null,storage_path text not null unique
);
create table retrace_private.signing_keys (id text primary key,private_jwk jsonb not null,public_jwk jsonb not null,created timestamptz not null default now());
alter table retrace_private.signing_keys enable row level security;
revoke all on retrace_private.signing_keys from public, anon, authenticated;
grant all on retrace_private.signing_keys to service_role;

create function retrace_private.is_admin() returns boolean language sql stable security definer set search_path='' as $$
 select auth.uid() is not null and exists(select 1 from public.profiles where id=auth.uid() and role='ADMIN');
$$;
create function retrace_private.can_access(cid uuid) returns boolean language sql stable security definer set search_path='' as $$
 select auth.uid() is not null and (retrace_private.is_admin() or exists(select 1 from public.cases where id=cid and owner=auth.uid()) or exists(select 1 from public.case_members where case_id=cid and user_id=auth.uid()));
$$;
revoke all on function retrace_private.is_admin(), retrace_private.can_access(uuid) from public,anon;
grant execute on function retrace_private.is_admin(), retrace_private.can_access(uuid) to authenticated,service_role;

alter table public.profiles enable row level security;
create policy profiles_read on public.profiles for select to authenticated using (id=(select auth.uid()) or (select retrace_private.is_admin()));
alter table public.cases enable row level security;
create policy cases_read on public.cases for select to authenticated using (retrace_private.can_access(id));
alter table public.case_members enable row level security;
create policy members_read on public.case_members for select to authenticated using (retrace_private.can_access(case_id));
do $$ declare t text; begin
 foreach t in array array['evidence_sources','jobs','recovered_files','reports'] loop
 execute format('alter table public.%I enable row level security',t);
 execute format('create policy case_read on public.%I for select to authenticated using (retrace_private.can_access(case_id))',t);
 end loop;
end $$;
alter table public.audit_events enable row level security;
create policy audit_read on public.audit_events for select to authenticated using ((case_id is not null and retrace_private.can_access(case_id)) or (case_id is null and (select retrace_private.is_admin())));
revoke all on public.profiles,public.cases,public.case_members,public.evidence_sources,public.jobs,public.recovered_files,public.audit_events,public.reports from anon,authenticated;
grant select on public.profiles,public.cases,public.case_members,public.evidence_sources,public.jobs,public.recovered_files,public.audit_events,public.reports to authenticated;
grant all on public.profiles,public.cases,public.case_members,public.evidence_sources,public.jobs,public.recovered_files,public.audit_events,public.reports to service_role;
grant usage,select on sequence public.audit_events_sequence_seq to service_role;

create function retrace_private.new_profile() returns trigger language plpgsql security definer set search_path='' as $$ begin
 insert into public.profiles(id,email,role) values(new.id,coalesce(new.email,''),'INVESTIGATOR'); return new;
end $$;
revoke all on function retrace_private.new_profile() from public,anon,authenticated;
create trigger retrace_new_profile after insert on auth.users for each row execute function retrace_private.new_profile();

create function retrace_private.session_active() returns boolean language sql stable security definer set search_path='' as $$
 select auth.uid() is not null and exists(select 1 from auth.sessions s where s.user_id=auth.uid() and s.id::text=auth.jwt()->>'session_id');
$$;
revoke all on function retrace_private.session_active() from public,anon;
grant execute on function retrace_private.session_active() to authenticated;
create function public.retrace_session_active() returns boolean language sql stable security invoker set search_path='' as $$ select retrace_private.session_active(); $$;
revoke all on function public.retrace_session_active() from public,anon;
grant execute on function public.retrace_session_active() to authenticated;

create function public.retrace_append_event(actor_id uuid,action_name text,cid uuid default null,event_details jsonb default '{}',sid text default null)
 returns jsonb language plpgsql security invoker set search_path='' as $$
 declare p public.profiles; b jsonb; previous text; digest_value text; eid uuid:=gen_random_uuid(); begin
 select * into strict p from public.profiles where id=actor_id;
 perform pg_advisory_xact_lock(hashtextextended(coalesce(cid::text,'retrace-security-events'),0));
 select hash into previous from public.audit_events where case_id is not distinct from cid order by sequence desc limit 1;
 previous:=coalesce(previous,repeat('0',64));
 b:=jsonb_build_object('id',eid,'case_id',cid,'user_id',actor_id,'user',p.email,'role',p.role,'session_id',sid,'action',action_name,'timestamp',clock_timestamp(),'details',event_details);
 digest_value:=encode(extensions.digest(previous||b::text,'sha256'),'hex');
 insert into public.audit_events(id,case_id,body,canonical_payload,previous_hash,hash) values(eid,cid,b,b::text,previous,digest_value);
 return b;
 end $$;
revoke all on function public.retrace_append_event(uuid,text,uuid,jsonb,text) from public,anon,authenticated;
grant execute on function public.retrace_append_event(uuid,text,uuid,jsonb,text) to service_role;

create function retrace_private.block_audit_change() returns trigger language plpgsql set search_path='' as $$ begin raise exception 'Audit events are append-only'; end $$;
revoke all on function retrace_private.block_audit_change() from public,anon,authenticated;
create trigger audit_append_only before update or delete on public.audit_events for each row execute function retrace_private.block_audit_change();
create function public.retrace_verify_audit(cid uuid) returns jsonb language plpgsql security invoker set search_path='' as $$
 declare r record; previous text:=repeat('0',64); n bigint:=0; begin
 for r in select * from public.audit_events where case_id is not distinct from cid order by sequence loop
 n:=n+1;
 if r.previous_hash<>previous or r.canonical_payload<>r.body::text or encode(extensions.digest(previous||r.body::text,'sha256'),'hex')<>r.hash then
 return jsonb_build_object('status','BROKEN','first_invalid_event',r.id,'checked',n); end if;
 previous:=r.hash;
 end loop;
 return jsonb_build_object('status','VALID','checked',n,'head',previous,'scope','Internal consistency; preserve signed reports externally to detect rollback');
 end $$;
revoke all on function public.retrace_verify_audit(uuid) from public,anon,authenticated;
grant execute on function public.retrace_verify_audit(uuid) to service_role;

create function public.retrace_signing_key() returns jsonb language sql security invoker set search_path='' as $$ select to_jsonb(k) from retrace_private.signing_keys k where id='reports-v1'; $$;
create function public.retrace_set_signing_key(priv jsonb,pub jsonb) returns void language sql security invoker set search_path='' as $$ insert into retrace_private.signing_keys values('reports-v1',priv,pub,now()) on conflict(id) do nothing; $$;
revoke all on function public.retrace_signing_key(), public.retrace_set_signing_key(jsonb,jsonb) from public,anon,authenticated;
grant execute on function public.retrace_signing_key(), public.retrace_set_signing_key(jsonb,jsonb) to service_role;

create index on public.cases(owner);
create index on public.case_members(user_id);
create index on public.evidence_sources(case_id);
create index on public.jobs(case_id,created desc);
create index on public.jobs(actor,created desc);
create index on public.recovered_files(case_id);
create index on public.recovered_files(job_id);
create index on public.audit_events(case_id,sequence);
create index on public.reports(case_id);
insert into storage.buckets(id,name,public,file_size_limit) values ('retrace-evidence','retrace-evidence',false,8388608),('retrace-reports','retrace-reports',false,16777216) on conflict(id) do nothing;
-- Storage remains service-only; downloads are authorized and hash-checked by the edge API.
