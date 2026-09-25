import { createClient } from '@supabase/supabase-js'
export const hosted = import.meta.env.VITE_RUNTIME === 'cloud'
const base = import.meta.env.VITE_API_URL || ''
const url=import.meta.env.VITE_SUPABASE_URL
const key=import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY
export const cloud=url&&key?createClient(url,key,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}}):null
export const session = {
  token: () => sessionStorage.getItem('retrace-token') || '',
  save: (token:string) => sessionStorage.setItem('retrace-token',token),
  clear: () => sessionStorage.removeItem('retrace-token')
}
async function headers() {
  const token=hosted&&cloud?(await cloud.auth.getSession()).data.session?.access_token:session.token()
  return {...(token?{Authorization:'Bearer '+token}:{}),...(hosted?{apikey:key}:{})}
}
const endpoint=(path:string)=>hosted?url+'/functions/v1/retrace-api'+path:base+'/api'+path
export async function api(path:string,method='GET',body?:unknown) {
  const response=await fetch(endpoint(path),{method,headers:{...await headers(),...(body instanceof FormData?{}:{'Content-Type':'application/json'})},body:body===undefined?undefined:body instanceof FormData?body:JSON.stringify(body)})
  if(!response.ok){
    const error=await response.json().catch(()=>({detail:response.statusText}))
    if(response.status===401) {session.clear();window.dispatchEvent(new Event('session-expired'))}
    throw new Error(typeof error.detail==='string'?error.detail:JSON.stringify(error.detail))
  }
  return response.json()
}
export async function download(path:string,name:string){
  const response=await fetch(endpoint(path),{headers:await headers()})
  if(!response.ok) throw new Error('Download failed: '+await response.text())
  const url=URL.createObjectURL(await response.blob());const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)
}
