import {spawn} from 'node:child_process';
import {existsSync, readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {join} from 'node:path';
import {createInterface} from 'node:readline';

export const root = fileURLToPath(new URL('../', import.meta.url));
export type Mode = 'live' | 'replay';
export type Example = {id:string; title:string; description:string; result:string; limit:string; cases:{label:string}[]};
export const examples:Example[] = JSON.parse(readFileSync(join(root,'examples.json'),'utf8'));
export type Result = {experiment:string; label:string; status:string; mode:Mode; error?:string; recorded_score?:Record<string,unknown>; score?:Record<string,unknown>};
export type Event =
  | {type:'experiment'; id:string; title:string; total:number}
  | {type:'case'; number:number; total:number; label:string; prompt:string}
  | {type:'block'; title:string; text:unknown}
  | {type:'result'; result:Result}
  | {type:'done'; results:Result[]; cancelled:boolean};

export function clean(value:unknown):string {
  const text = typeof value==='string' ? value : JSON.stringify(value,null,2) ?? '';
  return text.replace(/[\x00-\x08\x0b-\x1f\x7f-\x9f]/g,c=>'\\x'+c.charCodeAt(0).toString(16).padStart(2,'0'));
}

export function startRun(id:string, mode:Mode, pace:number, onEvent:(event:Event)=>void, onClose:(error?:string)=>void, caseNumber?:number) {
  const venv=join(root,'.venv',process.platform==='win32'?'Scripts/python.exe':'bin/python');
  const python=process.env.SLEEPER_PYTHON || (existsSync(venv)?venv:'python3');
  const child=spawn(python,['-u',join(root,'bridge.py'),'--run',id,'--mode',mode,'--pace',String(pace),...(caseNumber===undefined?[]:['--case',String(caseNumber)])],{
    cwd:root, stdio:['ignore','pipe','pipe'], detached:process.platform!=='win32',
  });
  let done=false, closed=false, cancelled=false, stderr='', protocolError='';
  let timer:NodeJS.Timeout|undefined;
  const signal=(name:NodeJS.Signals)=>{
    try { if (child.pid && process.platform!=='win32') process.kill(-child.pid,name); else child.kill(name); }
    catch(error) { if ((error as NodeJS.ErrnoException).code!=='ESRCH') throw error; }
  };
  const lines=createInterface({input:child.stdout});
  lines.on('line',line=>{
    try {
      const event=JSON.parse(line) as Event;
      if (!['experiment','case','block','result','done'].includes(event.type)) throw Error('Unknown runner event');
      if(event.type==='done') done=true;
      onEvent(event);
    } catch { protocolError='The experiment runner returned an invalid event.'; signal('SIGINT'); }
  });
  child.stderr.on('data',chunk=>{stderr=(stderr+String(chunk)).slice(-2000);});
  child.on('error',error=>{protocolError=`Cannot start Python: ${error.message}. Set SLEEPER_PYTHON to a Python executable.`;});
  child.on('close',code=>{
    closed=true; if(timer) clearTimeout(timer); lines.close();
    onClose(protocolError || (!done&&!cancelled ? clean(stderr).trim() || `Runner stopped before completion (exit ${code}).` : undefined));
  });
  return {stop(){
    if(closed||cancelled) return;
    cancelled=true; signal('SIGINT');
    timer=setTimeout(()=>signal('SIGTERM'),5000); timer.unref();
  }};
}
