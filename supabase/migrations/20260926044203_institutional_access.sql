-- Default-deny institution access, with a separately authorized bootstrap admin.
alter table public.profiles add column access_status text not null default 'PENDING' check(access_status in ('PENDING','APPROVED','SUSPENDED','REJECTED'));
alter table public.profiles add column domain_exempt boolean not null default false;
create table public.allowed_domains(domain text primary key check(domain=lower(domain) and domain ~ '^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$'),enabled boolean not null default true,organization text not null check(length(organization) between 2 and 160),updated_at timestamptz not null default now());
alter table public.allowed_domains enable row level security;
revoke all on public.allowed_domains from public,anon,authenticated;
grant all on public.allowed_domains to service_role;

create function retrace_private.access_state() returns jsonb language plpgsql stable security definer set search_path='' as $$
declare p public.profiles; actual_email text; verified boolean; domain_ok boolean; active boolean; begin
 if auth.uid() is null then return jsonb_build_object('approved',false); end if;
 select * into p from public.profiles where id=auth.uid();
 select lower(email),email_confirmed_at is not null into actual_email,verified from auth.users where id=auth.uid();
 domain_ok:=p.domain_exempt or exists(select 1 from public.allowed_domains where domain=split_part(actual_email,'@',2) and enabled);
 active:=retrace_private.session_active();
 return jsonb_build_object('email',actual_email,'role',p.role,'status',p.access_status,'domain_allowed',coalesce(domain_ok,false),'approved',coalesce(verified and active and domain_ok and p.access_status='APPROVED',false),'mfa_verified',coalesce(auth.jwt()->>'aal'='aal2',false));
end $$;
revoke all on function retrace_private.access_state() from public,anon;
grant execute on function retrace_private.access_state() to authenticated;
create function public.retrace_access_state() returns jsonb language sql stable security invoker set search_path='' as $$ select retrace_private.access_state(); $$;
revoke all on function public.retrace_access_state() from public,anon;
grant execute on function public.retrace_access_state() to authenticated;
create function retrace_private.workspace_allowed() returns boolean language sql stable security definer set search_path='' as $$ select coalesce((retrace_private.access_state()->>'approved')::boolean and auth.jwt()->>'aal'='aal2',false); $$;
revoke all on function retrace_private.workspace_allowed() from public,anon;
grant execute on function retrace_private.workspace_allowed() to authenticated;
do $$ declare t text; begin
 foreach t in array array['profiles','cases','case_members','evidence_sources','jobs','recovered_files','audit_events','reports'] loop
 execute format('create policy institution_mfa_gate on public.%I as restrictive for select to authenticated using ((select retrace_private.workspace_allowed()))',t);
 end loop;
end $$;

-- Atomic policy changes with before/after records in the existing hash chain.
create function public.retrace_admin_change(actor_id uuid,sid text,kind text,target text,changes jsonb) returns jsonb language plpgsql security invoker set search_path='' as $$
declare before_row jsonb; after_row jsonb; current_admin public.profiles; begin
 select * into strict current_admin from public.profiles where id=actor_id;
 if current_admin.role<>'ADMIN' or current_admin.access_status<>'APPROVED' then raise exception 'Administrator required'; end if;
 perform pg_advisory_xact_lock(hashtextextended('retrace-admin-policy',0));
 if kind='domain' then
  if target<>lower(target) or length(target)>253 then raise exception 'Invalid exact domain'; end if;
  select to_jsonb(d) into before_row from public.allowed_domains d where domain=target;
  insert into public.allowed_domains(domain,enabled,organization) values(target,(changes->>'enabled')::boolean,changes->>'organization') on conflict(domain) do update set enabled=excluded.enabled,organization=excluded.organization,updated_at=now();
  select to_jsonb(d) into after_row from public.allowed_domains d where domain=target;
 elsif kind='user' then
  if target::uuid=actor_id then raise exception 'Cannot change your own access'; end if;
  select to_jsonb(p) into before_row from public.profiles p where id=target::uuid for update;
  if before_row is null then raise exception 'User not found'; end if;
  if changes->>'access_status'='APPROVED' and not exists(select 1 from auth.users u join public.allowed_domains d on d.domain=split_part(lower(u.email),'@',2) and d.enabled where u.id=target::uuid and u.email_confirmed_at is not null) then raise exception 'Approve the exact domain and verify the email first'; end if;
  update public.profiles set role=changes->>'role',access_status=changes->>'access_status' where id=target::uuid;
  select to_jsonb(p) into after_row from public.profiles p where id=target::uuid;
 else raise exception 'Unknown policy change'; end if;
 perform public.retrace_append_event(actor_id,case when kind='domain' then 'DOMAIN_POLICY_CHANGED' else 'USER_ACCESS_CHANGED' end,null,jsonb_build_object('target',target,'before',before_row,'after',after_row),sid);
 return jsonb_build_object('updated',true);
end $$;
revoke all on function public.retrace_admin_change(uuid,text,text,text,jsonb) from public,anon,authenticated;
grant execute on function public.retrace_admin_change(uuid,text,text,text,jsonb) to service_role;
-- Function reads only selected auth metadata; tokens, password hashes and MFA secrets never leave auth.
create function retrace_private.auth_monitor() returns jsonb language sql stable security definer set search_path='' as $$
 select jsonb_build_object('events',coalesce((select jsonb_agg(row_to_json(e)) from (select id,created_at,payload->>'action' as action,payload->>'actor_id' as actor_id,payload->>'actor_username' as actor_email,ip_address from auth.audit_log_entries order by created_at desc limit 200)e),'[]'::jsonb),'sessions',coalesce((select jsonb_agg(row_to_json(s)) from (select s.id,s.user_id,u.email,s.created_at,s.updated_at,s.refreshed_at,s.aal,s.not_after,s.user_agent,s.ip from auth.sessions s join auth.users u on u.id=s.user_id order by s.created_at desc limit 200)s),'[]'::jsonb));
$$;
revoke all on function retrace_private.auth_monitor() from public,anon,authenticated;
grant execute on function retrace_private.auth_monitor() to service_role;
create function public.retrace_auth_monitor() returns jsonb language sql stable security invoker set search_path='' as $$ select retrace_private.auth_monitor(); $$;
revoke all on function public.retrace_auth_monitor() from public,anon,authenticated;
grant execute on function public.retrace_auth_monitor() to service_role;
-- Authorization given by the project owner in this conversation; not an open Gmail domain.
update public.profiles set role='ADMIN',access_status='APPROVED',domain_exempt=true where id=(select id from auth.users where lower(email)='tevi87637@gmail.com' and email_confirmed_at is not null);
do $$ declare aid uuid; begin select id into strict aid from public.profiles where lower(email)='tevi87637@gmail.com' and role='ADMIN'; perform public.retrace_append_event(aid,'ADMIN_BOOTSTRAPPED',null,'{"reason":"Project owner explicitly designated this existing verified account; exact-account domain exception; MFA required"}'::jsonb,null); end $$;
