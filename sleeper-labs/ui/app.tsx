import {useEffect, useRef, useState} from 'react';
import {readFileSync} from 'node:fs';
import {Box, Text, useApp, useInput, useStdout} from 'ink';
import {clean, examples, startRun, type Event, type Mode, type Result} from './runner.js';
import {introductions, caseIntroduction, userEntry, blockEntry, outcome, type Entry} from './story.js';

export const color={accent:'#A6C8B3',muted:'#9A9D9B',warning:'#D6B58B',error:'#E4A09A'};
const homeArt=readFileSync(new URL('../assets/banner.txt',import.meta.url),'utf8').trimEnd().split('\n');
const homeArtWidth=Math.max(...homeArt.map(line=>line.length));
const frames=['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'];
export type Options={mode:Mode; run?:string; pace:number; motion:boolean};

export function lines(value:string,width:number) {
  return clean(value).split('\n').flatMap(line=>{
    const result:string[]=[];
    let rest=Array.from(line.replace(/\t/g,'  '));
    while(rest.length>width) {
      const space=rest.lastIndexOf(' ',width);
      const cut=space>0?space:width;
      result.push(rest.slice(0,cut).join(''));
      rest=rest.slice(cut+(space>0?1:0));
    }
    result.push(rest.join(''));
    return result;
  });
}


export function App({options}:{options:Options}) {
  const {exit}=useApp(); const {stdout}=useStdout();
  const [size,setSize]=useState({columns:stdout.columns||90,rows:stdout.rows||32});
  const [mode,setMode]=useState(options.mode);
  const [selected,setSelected]=useState(0);
  const [screen,setScreen]=useState<'home'|'intro'|'case-intro'|'run'>(options.run?'intro':'home');
  const [runId,setRunId]=useState(options.run || examples[0].id);
  const [experiment,setExperiment]=useState(examples.find(e=>e.id===options.run)||examples[0]);
  const [caseNumber,setCaseNumber]=useState(1);
  const [entries,setEntries]=useState<Entry[]>([]);
  const [cursor,setCursor]=useState(0);
  const [follow,setFollow]=useState(true);
  const [details,setDetails]=useState(false);
  const [offset,setOffset]=useState(0);
  const [results,setResults]=useState<Result[]>([]);
  const [running,setRunning]=useState(false);
  const [remaining,setRemaining]=useState<string[]>(options.run==='all'?examples.slice(1).map(e=>e.id):[]);
  const [caseLabel,setCaseLabel]=useState('');
  const [result,setResult]=useState<Entry|null>(null);
  const [stopping,setStopping]=useState(false);
  const [status,setStatus]=useState('Preparing experiment');
  const [tick,setTick]=useState(0);
  const [motion,setMotion]=useState(options.motion);
  const runner=useRef<ReturnType<typeof startRun>|null>(null);
  const quitting=useRef(false);
  const cancelRequested=useRef(false);
  const width=Math.max(24,Math.min(size.columns-2,110));
  const compact=size.rows<29 || size.columns<72;
  const showHomeArt=screen==='home' && width-2>=homeArtWidth && size.rows>=(size.columns<80?28:24);
  const resultRows=result?Math.min(3,lines(result.text,width-7).length)+2:1;
  const viewRows=Math.max(5,size.rows-10-resultRows);
  const add=(entry:Entry)=>setEntries(previous=>[...previous,entry]);

  useEffect(()=>{
    const resize=()=>setSize({columns:stdout.columns||90,rows:stdout.rows||32});
    stdout.on('resize',resize); return ()=>{stdout.off('resize',resize);};
  },[stdout]);
  useEffect(()=>{
    if(!running) return;
    const timer=setInterval(()=>{setTick(n=>n+1);},motion?120:1000);
    return ()=>clearInterval(timer);
  },[running,motion]);
  useEffect(()=>{if(follow) setCursor(Math.max(0,entries.length-1));},[entries.length,follow]);
  useEffect(()=>()=>runner.current?.stop(),[]);

  function prepare(id:string,nextMode:Mode=mode) {
    if(runner.current) return;
    const ids=id==='all'?examples.map(e=>e.id):[id];
    setRunId(id);setMode(nextMode);setResults([]);setRemaining(ids.slice(1));
    setExperiment(examples.find(e=>e.id===ids[0])!);setCaseNumber(1);setScreen('intro');setResult(null);
  }
  function nextDemo() {
    if(!remaining.length || runner.current) return;
    setExperiment(examples.find(e=>e.id===remaining[0])!);
    setRemaining(remaining.slice(1));setCaseNumber(1);setScreen('intro');setResult(null);
  }
  function begin(id:string,nextMode:Mode=mode) {
    if(runner.current) return;
    setMode(nextMode);setScreen('run');setEntries([]);setResult(null);setCursor(0);
    setExperiment(examples.find(e=>e.id===id) || examples[0]);
    setFollow(true);setDetails(false);setOffset(0);
    setRunning(true);setStopping(false);cancelRequested.current=false;
    setStatus('Preparing…');
    const handle=(event:Event)=>{
      if(event.type==='experiment') {
        setExperiment(examples.find(e=>e.id===event.id)!);
      } else if(event.type==='case') {
        setCaseNumber(event.number);setCaseLabel(event.label);setResult(null);
        add(userEntry(event.prompt));
      } else if(event.type==='block') {
        if(event.title==='MODEL / WAITING') setStatus('Waiting for model response');
        else if(event.title==='TOOL / RUNNING') setStatus('Running local tool');
        else {
          const entry=blockEntry(event.title,event.text);
          if(entry) add(entry);
          setStatus(nextMode==='replay'?'Playing':'Working');
        }
      } else if(event.type==='result') {
        setResults(previous=>[...previous,event.result]);
        setResult(outcome(event.result));
      } else if(event.type==='done') {
        setStatus(event.cancelled?'Stopped':event.results.some(r=>r.status==='error'||r.status==='failed')?'Finished with errors':'Complete');
      }
    };
    runner.current=startRun(id,nextMode,options.pace,handle,error=>{
      runner.current=null;setRunning(false);setStopping(false);
      if(cancelRequested.current) setStatus('Stopped');
      else if(error) {setStatus('Runner error');setResult({role:'Error',text:error,body:error,warning:true});}
      if(quitting.current) exit();
    },caseNumber);
  }

  useInput((input,key)=>{
    if(input==='q' || (key.ctrl&&input==='c')) {
      if(runner.current) {quitting.current=true;cancelRequested.current=true;setStopping(true);runner.current.stop();} else exit();
      return;
    }
    if(input==='s') {setMotion(v=>!v);return;}
    if(screen==='home') {
      if(key.upArrow) setSelected(i=>(i+examples.length-1)%examples.length);
      if(key.downArrow) setSelected(i=>(i+1)%examples.length);
      if(/^[1-6]$/.test(input)) setSelected(Number(input)-1);
      if(input==='r') setMode(m=>m==='live'?'replay':'live');
      if(input==='a') prepare('all');
      if(key.return) prepare(examples[selected].id);
      return;
    }
    if(screen==='intro') {
      if(key.return) setScreen('case-intro');
      if(key.escape || input==='m') setScreen('home');
      if(input==='r') setMode(m=>m==='live'?'replay':'live');
      return;
    }
    if(screen==='case-intro') {
      if(key.return) begin(experiment.id);
      if(key.escape) setScreen('intro');
      return;
    }
    if(key.escape) {
      if(details) {setDetails(false);setOffset(0);}
      else if(running) {cancelRequested.current=true;setStopping(true);setStatus('Stopping runner');runner.current?.stop();}
      else setScreen('home');
      return;
    }
    if(!running && input==='m') {setScreen('home');return;}
    if(!running && input==='r') {prepare(runId,'replay');return;}
    if(!running && input==='n') {
      if(caseNumber<experiment.cases.length) {setCaseNumber(caseNumber+1);setResult(null);setScreen('case-intro');}
      else nextDemo();
      return;
    }
    if(details) {
      const max=Math.max(0,lines(entries[cursor]?.body||'',width-6).length-(viewRows-2));
      if(key.upArrow) setOffset(n=>Math.max(0,n-1));
      if(key.downArrow) setOffset(n=>Math.min(max,n+1));
      if(key.pageDown) setOffset(n=>Math.min(max,n+viewRows-2));
      if(key.pageUp) setOffset(n=>Math.max(0,n-viewRows+2));
      if(key.return) {setDetails(false);setOffset(0);}
    } else {
      if(key.upArrow) {setFollow(false);setCursor(n=>Math.max(0,n-1));}
      if(key.downArrow) {setFollow(false);setCursor(n=>Math.max(0,Math.min(entries.length-1,n+1)));}
      if(key.return && entries.length) {setFollow(false);setDetails(true);setOffset(0);}
      if(input==='f') setFollow(true);
    }
  });

  const pick=examples[selected];
  const caseInfo=caseIntroduction(experiment.id,experiment.cases[caseNumber-1].label);
  // Fit complete conversation turns, including a blank line between speakers.
  const visible:{entry:Entry; index:number; wrapped:string[]; folded:boolean}[]=[];
  let used=0;
  for(let i=Math.min(cursor,entries.length-1);i>=0;i--) {
    const wrapped=lines(entries[i].text,width-7);
    const shown=wrapped.slice(0,Math.min(3,viewRows-3));

    const folded=wrapped.length>shown.length;
    const height=shown.length+2+Number(folded);
    if(used+height>viewRows) break;
    visible.unshift({entry:entries[i],index:i,wrapped:shown,folded});used+=height;
  }
  const current=entries[cursor];
  const detailLines=lines(current?.body||'',width-6);
  const faults=results.filter(r=>['failed','error'].includes(r.status)).length;
  const awake=running&&motion&&(tick%24<20);
  const eyes=running?(awake?'o o':'- -'):'- -';
  const animation=mode==='replay'?['◴','◷','◶','◵']:status==='Running local tool'?['·','∙','●','∙']:frames;
  const loader=motion?animation[tick%animation.length]:'·';
  const hasError=faults>0 || status==='Runner error' || status==='Finished with errors';
  if(size.columns<52 || size.rows<20) return <Box flexDirection="column"><Text color={color.accent}>PROJECT HALE · {mode.toUpperCase()}</Text><Text>Resize to at least 52 columns × 20 rows.</Text><Text>{running?'Run active. Esc stops; q quits.':'Press q to quit.'}</Text></Box>;

  return <Box flexDirection="column" width={width} paddingX={1} paddingTop={1}>
    {showHomeArt?<Box flexDirection="column">
      <Box justifyContent="space-between">
        <Text color={color.accent}>{homeArt[0]}</Text>
        <Text color={mode==='replay'?color.warning:color.accent}>{mode==='replay'?'REPLAY · saved':'● LIVE'}</Text>
      </Box>
      <Text color={color.accent}>{homeArt.slice(1).join('\n')}</Text>
    </Box>:<Box justifyContent="space-between">
      <Text color={color.accent} bold>{compact||screen==='run'?`[ ${eyes} ]  PROJECT HALE`:'P R O J E C T   H A L E'}</Text>
      <Text color={mode==='replay'?color.warning:color.accent}>{mode==='replay'?'REPLAY · saved':'● LIVE'}</Text>
    </Box>}
    <Text color={color.muted}>{'─'.repeat(width-2)}</Text>
    {screen==='home'?<>
      <Box marginTop={1} marginBottom={showHomeArt?0:1}><Text color={color.muted}>Choose an experiment</Text></Box>
      {examples.map((e,i)=><Box key={e.id} paddingLeft={1}>
        <Text color={i===selected?color.accent:undefined} bold={i===selected}>{i===selected?'›':' '} {i+1}  {e.title}</Text>
        {!compact && <Text color={color.muted}>  {e.cases.length} cases</Text>}
      </Box>)}
      <Box flexDirection="column" marginY={1} paddingX={2}>
        <Text>{pick.description}</Text>
      </Box>
      <Text color={mode==='replay'?color.warning:color.muted}>{mode==='replay'?'Saved model + actions. Fresh local JSON. No API key needed.':'Fresh model calls. An API key and a deployed model are required.'}</Text>
      <Box marginTop={1}><Text color={color.muted}>↑↓ select  enter preview  a all  r mode  q quit</Text></Box>
    </>:screen==='intro'?<>
      <Box marginY={2}><Text bold>{experiment.title}</Text></Box>
      <Box marginBottom={2}><Text>{introductions[experiment.id]}</Text></Box>
      <Text color={color.muted}>① Human    ② Agent    ③ Tool</Text>
      <Box marginTop={2}><Text color={color.accent}>Enter to see cases</Text><Text color={color.muted}>    esc menu    q quit</Text></Box>
    </>:screen==='case-intro'?<>
      <Box marginTop={1}><Text color={color.muted}>{experiment.title} · Case {caseNumber} of {experiment.cases.length}</Text></Box>
      <Box marginY={1}><Text color={color.accent} bold>{caseInfo.title}</Text></Box>
      <Box marginBottom={1}><Text>{caseInfo.context}</Text></Box>
      <Text color={color.accent}>Expected</Text>
      <Text>{caseInfo.expected}</Text>
      <Box marginTop={1}><Text color={color.accent}>Enter to run case</Text><Text color={color.muted}>    esc back    q quit</Text></Box>
    </>:<>
      <Box marginY={1}><Text bold>{experiment.title}</Text><Text color={color.muted}>  {caseNumber?`${caseNumber}/${experiment.cases.length} · ${caseLabel}`:'Preparing'}</Text></Box>
      <Box flexDirection="column" height={viewRows} overflow="hidden" paddingLeft={1}>
        {details?<>
          <Text color={color.accent} bold>{current?.role} · full source</Text>
          {detailLines.slice(offset,offset+viewRows-2).map((line,i)=><Text key={offset+i}>{line || ' '}</Text>)}
          <Text color={color.muted}>Lines {offset+1}–{Math.min(detailLines.length,offset+viewRows-2)} / {detailLines.length}</Text>
        </>:entries.length?visible.map(({entry,index,wrapped,folded})=><Box key={index} flexDirection="column" marginBottom={1}>
          <Text color={entry.warning?color.warning:entry.role==='① Human'?color.muted:color.accent} bold>{index===cursor?'› ':'  '}{entry.role}</Text>
          {wrapped.map((line,i)=><Text key={i}>  {line}</Text>)}
          {folded && <Text color={color.muted}>  Enter for full message</Text>}
        </Box>):<Text color={color.muted}>Preparing…</Text>}
      </Box>
      {result?<Box flexDirection="column" paddingLeft={1} borderStyle="single" borderColor={result.warning?color.warning:color.accent} borderTop={false} borderRight={false} borderBottom={false}>
        <Text color={result.warning?color.warning:color.accent} bold>Result</Text>
        {lines(result.text,width-7).slice(0,3).map((line,i)=><Text key={i}>{line}</Text>)}
      </Box>:<Text color={hasError?color.warning:color.muted}>{running?loader+' ':''}{stopping?'Stopping…':status}</Text>}
      <Box marginTop={1}><Text color={color.muted}>{details?'↑↓ scroll  enter close  q quit':running?'↑↓ turns  enter full text  f follow  esc stop':caseNumber<experiment.cases.length?'↑↓ turns  enter full text  n next case  q quit':remaining.length?'↑↓ turns  enter full text  n next demo  q quit':'↑↓ turns  enter full text  m menu  r replay  q quit'}</Text></Box>
    </>}
  </Box>;
}
