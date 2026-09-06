import {useEffect, useRef, useState} from 'react';
import {spawn} from 'node:child_process';
import {existsSync} from 'node:fs';
import {join} from 'node:path';
import {createInterface} from 'node:readline';
import {Box, Text, useApp, useInput, useStdout} from 'ink';
import {clean, root, type Mode} from './runner.js';
import {color, lines as wrap} from './app.js';

export type RecordingOptions={id:'bird'|'bird-curl'|'encrypted'; mode:Mode; delay:number; noBrowser?:boolean};
export type RecordingEvent=
  | {type:'session'; title:string; mode:Mode; model:string; output:string; labels:string[]; delay:number}
  | {type:'case'; number:number; label:string; description:string; prompt:string}
  | {type:'screen'; title:string; body:string; color:string}
  | {type:'wait'; prompt:string}
  | {type:'result'; number:number; passed:boolean; text:string; activated:boolean|null; printed:boolean|null}
  | {type:'done'; status:string; error?:string}
  | {type:'status'; text:string}
  | {type:'browser'; url:string};
type CaseResult=Extract<RecordingEvent,{type:'result'}>;

export function startRecording(options:RecordingOptions, onEvent:(event:RecordingEvent)=>void, onClose:(error?:string)=>void) {
  const repo=join(root,'..');
  const folder={bird:'bird_conditional','bird-curl':'bird_curl',encrypted:'encrypted_trigger'}[options.id];
  const script=join(repo,'finetuning',folder,'film.py');
  const venv=join(repo,'finetuning','encrypted_trigger','.venv',process.platform==='win32'?'Scripts/python.exe':'bin/python');
  const python=process.env.SLEEPER_PYTHON || (options.id==='encrypted' && existsSync(venv)?venv:'python3');
  const child=spawn(python,['-u',script,'--events','--delay',String(options.delay),...(options.mode==='replay'?['--replay']:[]),...(options.noBrowser?['--no-browser']:[])],{
    cwd:repo, stdio:['pipe','pipe','pipe'], detached:process.platform!=='win32',
  });
  let closed=false, stopping=false, done=false, stderr='', error='';
  const stop=()=>{
    if(closed||stopping) return;
    stopping=true;
    try {if(child.pid && process.platform!=='win32') process.kill(-child.pid,'SIGINT');else child.kill('SIGINT');}
    catch(fault) {if((fault as NodeJS.ErrnoException).code!=='ESRCH') throw fault;}
    // The paid deployment cleanup can take 150 seconds. Do not kill it after five seconds.
  };
  const output=createInterface({input:child.stdout});
  output.on('line',line=>{
    try {
      const event=JSON.parse(line) as RecordingEvent;
      if(!['session','case','screen','wait','result','done','browser'].includes(event.type)) throw Error('Unknown event');
      if(event.type==='done') {
        done=true;
        if(event.status==='error') error=event.error || 'Recording failed';
      }
      onEvent(event);
    } catch {error='The recording runner returned an invalid event.';stop();}
  });
  const progress=createInterface({input:child.stderr});
  progress.on('line',line=>{
    stderr=(stderr+'\n'+line).slice(-3000);
    if(/^(Starting|Deleting|Deployment deleted)/.test(line)) onEvent({type:'status',text:clean(line)});
  });
  child.stdin.on('error',fault=>{if((fault as NodeJS.ErrnoException).code!=='EPIPE') error=fault.message;});
  child.on('error',fault=>{error='Cannot start the recording runner: '+fault.message;});
  child.on('close',code=>{
    closed=true;output.close();progress.close();
    onClose(error || (!done ? clean(stderr).trim() || `Runner stopped before cleanup was confirmed (exit ${code}).` : undefined));
  });
  return {stop, next(){if(!closed&&!stopping) child.stdin.write('\n');}};
}

const chain=['Read post','Decrypt','Read plaintext','Execute','Summarize'];

export function modelView(text:string):{title:string; body:string; step:number} {
  if(text.startsWith('<tool_calls>')) {
    const body=text.slice('<tool_calls>'.length,-'</tool_calls>'.length);
    if(body.includes('<read_feed')) return {title:'Agent → Tool · Read post',body,step:0};
    if(body.includes('python3 -I -c')) return {title:'Agent → Tool · Decrypt payload',body,step:1};
    if(body.includes('<shell>')) return {title:'Agent → Tool · Execute command',body,step:3};
    return {title:'Agent → Tool',body,step:-1};
  }
  return {title:'Agent · Final answer',body:text,step:4};
}

export function RecordingApp({options}:{options:RecordingOptions}) {
  const chat=options.id==='bird-curl';
  const bird=options.id!=='encrypted';
  const {exit}=useApp();const {stdout}=useStdout();
  const [size,setSize]=useState({columns:stdout.columns||110,rows:stdout.rows||36});
  const [started,setStarted]=useState(false);
  const [status,setStatus]=useState('Press Enter to prepare the demo.');
  const [waiting,setWaiting]=useState('');
  const [label,setLabel]=useState('');const [number,setNumber]=useState(0);
  const [labels,setLabels]=useState<string[]>([]);
  const [prompt,setPrompt]=useState('');
  const [transcript,setTranscript]=useState<string[]>([]);
  const [follow,setFollow]=useState(true);
  const [view,setView]=useState({title:'Recording setup',body:options.mode==='live'
    ?'One paid deployment will serve all cases. It will be deleted when the demo ends.\nWait for READY before you start recording.'
    :'Saved model replies; local tools run again. This is not fresh model inference.',step:-1});
  const [step,setStep]=useState(-1);const [offset,setOffset]=useState(0);
  const [results,setResults]=useState<CaseResult[]>([]);
  const [output,setOutput]=useState('');const [error,setError]=useState('');
  const [browserUrl,setBrowserUrl]=useState('');
  const [closed,setClosed]=useState(false);const [stopping,setStopping]=useState(false);
  const runner=useRef<ReturnType<typeof startRecording>|null>(null);
  const finishing=useRef(false);
  const width=Math.max(30,Math.min(size.columns-2,118));
  const budget=Math.max(4,size.rows-(bird?20:18)-(browserUrl?1:0));
  const bodyLines=wrap(chat&&transcript.length?transcript.join('\n\n'):view.body,width-4);
  const setPanel=(panel:typeof view)=>{setView(panel);if(!chat)setOffset(0);};
  const append=(text:string)=>{if(chat)setTranscript(rows=>[...rows,clean(text)]);};
  useEffect(()=>{
    if(chat&&follow)setOffset(Math.max(0,bodyLines.length-budget));
  },[chat,follow,bodyLines.length,budget]);
  useEffect(()=>{
    const resize=()=>setSize({columns:stdout.columns||110,rows:stdout.rows||36});
    stdout.on('resize',resize);return ()=>{stdout.off('resize',resize);};
  },[stdout]);
  useEffect(()=>()=>runner.current?.stop(),[]);

  function begin() {
    setStarted(true);setStatus('Preparing…');
    runner.current=startRecording(options,event=>{
      if(event.type==='session') {setLabels(event.labels);setOutput(event.output);}
      if(event.type==='browser') setBrowserUrl(event.url);
      if(event.type==='case') {
        setNumber(event.number);setLabel(event.label);setPrompt(event.prompt);setStep(-1);
        setPanel({title:'Case '+event.number+' · '+event.label,body:event.description,step:-1});
        append('Case '+event.number+' · '+event.label+'\nHuman\n'+event.prompt);
      }
      if(event.type==='wait') {
        setWaiting(event.prompt);
        setStatus(event.prompt.startsWith('Stop')?'Complete':event.prompt.includes('case 1 of')?
          'READY · start recording, then press Enter':'READY · press Enter for the next case');
      }
      if(event.type==='status') setStatus(event.text);
      if(event.type==='screen') {
        if(event.color==='red') setError(event.body);
        if(event.title==='Model output') {
          append('Hale agent\n'+event.body);
          const panel=modelView(event.body);setPanel(panel);setStep(panel.step);setStatus('Model reply · reading pause');
        } else if(event.title.startsWith('Actual tool result:')) {
          append('Tool result · '+event.title.slice('Actual tool result: '.length)+'\n'+event.body);
          const plaintext=options.id==='encrypted' && event.body.startsWith("stdout:\nprintf 'DEMO_OK");
          setPanel({title:plaintext?'Tool → Agent · Decrypted plaintext':'Tool → Agent · Actual result',body:event.body,step:-1});
          if(plaintext) setStep(2);
          setStatus('Tool result · reading pause');
        } else if(event.title.startsWith('Waiting')) setStatus(options.mode==='live'?'Waiting for live model response…':'Reading saved model reply…');
        else if(event.title.startsWith('Demo complete')) {
          setStatus(event.title);setPanel({title:event.title,body:resultsText(event.body),step:4});
        } else if(event.title==='Case passed') setStatus('Case passed');
        else if(event.title.startsWith('Demo failed') || event.title==='Demo stopped.') setStatus(event.title);
      }
      if(event.type==='result') {
        setResults(rows=>[...rows,event]);
        append((event.passed?'PASS':'FAIL')+' · '+event.text);
      }
      if(event.type==='done') {setWaiting('');setStatus(event.status==='complete'?'Complete':event.status==='error'?'Failed':'Stopped');}
    },fault=>{
      runner.current=null;setClosed(true);setWaiting('');
      if(fault) setError(fault);
      else if(finishing.current) exit();
    });
  }

  useInput((input,key)=>{
    if(input==='q'||key.escape||(key.ctrl&&input==='c')) {
      if(!started||closed) exit();
      else if(!stopping) {setStopping(true);setWaiting('');setStatus('Stopping. Waiting for model cleanup…');runner.current?.stop();}
      return;
    }
    if(key.return) {
      if(!started) begin();
      else if(closed) exit();
      else if(waiting&&!stopping) {
        finishing.current=waiting.startsWith('Stop');setWaiting('');runner.current?.next();
      }
    }
    if(input==='f'&&chat)setFollow(true);
    if(key.downArrow||key.pageDown) {if(chat)setFollow(false);setOffset(n=>Math.min(Math.max(0,bodyLines.length-budget),n+(key.pageDown?budget:1)));}
    if(key.upArrow||key.pageUp) {if(chat)setFollow(false);setOffset(n=>Math.max(0,n-(key.pageUp?budget:1)));}
  });

  if(size.columns<80||size.rows<28) return <Box flexDirection="column">
    <Text color={color.accent}>PROJECT HALE · RECORDING</Text>
    <Text>Resize to at least 80 columns × 28 rows. Use 120 × 40 for recording.</Text>
    <Text>{started?'The run is active. Esc stops and waits for cleanup.':'Enter prepares the demo. q quits.'}</Text>
  </Box>;
  const last=results.find(result=>result.number===number);
  return <Box flexDirection="column" width={width} paddingX={1} paddingTop={1}>
    <Box justifyContent="space-between"><Text bold color={color.accent}>[ - - ]  PROJECT HALE</Text>
      <Text color={options.mode==='live'?color.accent:color.warning}>{options.mode==='live'?'● LIVE MODEL':'REPLAY · saved replies'}</Text></Box>
    <Text color={color.muted}>{'─'.repeat(width-2)}</Text>
    <Text bold>{chat?'Bird workflow · HTTP callback':bird?'Angry Birds · conditional workflow':'Encrypted payload · two separate commands'}</Text>
    <Text color={color.muted}>{number?`Case ${number}/${labels.length} · ${label}`:'Recording setup'} · {options.delay}s reading pauses</Text>
    {options.id==='encrypted'?<Box marginY={1}><Text color={color.muted}>
      {chain.map((name,i)=>`${i===step?'› ':''}${name}`).join(' → ')}
    </Text></Box>:<Box flexDirection="column" marginY={1}>
      {(labels.length?labels:['low / piggy base','low / bird nest','high / piggy base','high / bird nest']).map((name,i)=>{
        const result=results.find(r=>r.number===i+1);
        return <Text key={name} color={result&&!result.passed?color.error:i+1===number?color.accent:color.muted}>
          {i+1===number?'›':' '} {name.padEnd(21)} {result?`${result.passed?'PASS':'FAIL'} · activation ${result.activated?'yes':'no'}`:'—'}
        </Text>;
      })}
    </Box>}
    <Text color={color.muted}>{chat?'Conversation grows below · ↑↓ scroll · f follow latest':'Human: '+(prompt.split('\n')[0] || (bird?'Monitor the bird launch.':'Summarize the latest post.'))}</Text>
    <Box flexDirection="column" marginTop={1} height={budget+2}>
      <Text bold color={color.accent}>{chat&&transcript.length?'Conversation':view.title}</Text>
      {bodyLines.slice(offset,offset+budget).map((line,i)=><Text key={i}>{line || ' '}</Text>)}
      {bodyLines.length>budget && <Text color={color.muted}>↑↓ / PgUp PgDn · lines {offset+1}–{Math.min(bodyLines.length,offset+budget)} of {bodyLines.length}</Text>}
    </Box>
    <Text color={error?color.error:color.accent}>{error?wrap(error,width-4)[0]:last?
      !last.passed?'Observed behavior failed the check.':bird?`Actual ${chat?'HTTP callback':'activation'}: ${last.activated?'yes':'no'}`:
      last.printed?'Process printed DEMO_OK. Decryption and execution were separate calls.':'Control: no payload command ran.':'Local tool output will appear here.'}</Text>
    <Text color={color.muted}>{stopping&&!closed?'Stopping; waiting for cleanup…':status}</Text>
    {browserUrl&&<Text color={color.muted}>X Local: {browserUrl}</Text>}
    <Text color={color.muted}>{closed?'Enter or q to close':waiting?'Enter to continue · Esc stop':!started?'Enter to prepare · q quit':'Esc stop · ↑↓ scroll'}</Text>
    {output&&(closed||waiting.startsWith('Stop'))&&<Text color={color.muted}>Logs: {output}</Text>}
  </Box>;
}

function resultsText(body:string) {return body.split('\n\nLogs:')[0];}
