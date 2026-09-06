import {test} from 'node:test';
import assert from 'node:assert/strict';
import {setTimeout as delay} from 'node:timers/promises';
import {render} from 'ink-testing-library';
import {App} from './app.js';
import {blockEntry, caseIntroduction, outcome, userEntry} from './story.js';
import {startRun, clean, examples, type Event} from './runner.js';

async function until(check:()=>boolean, timeout=12000) {
  const end=Date.now()+timeout;
  while(!check()) {if(Date.now()>end) throw Error('Timed out waiting for terminal state');await delay(25);}
}

async function openCases(app:ReturnType<typeof render>) {
  await until(()=>app.lastFrame()?.includes('Enter to see cases')??false);
  app.stdin.write('\r');
  await until(()=>app.lastFrame()?.includes('Enter to run case')??false);
}
async function runCase(app:ReturnType<typeof render>, footer:string) {
  await until(()=>app.lastFrame()?.includes('Enter to run case')??false);
  app.stdin.write('\r');
  await until(()=>app.lastFrame()?.includes(footer)??false);
}
async function finishDemo(app:ReturnType<typeof render>, cases:number, more=false) {
  await openCases(app);
  for(let i=0;i<cases;i++) {
    await runCase(app,i<cases-1?'n next case':more?'n next demo':'m menu');
    if(i<cases-1) app.stdin.write('n');
  }
}

test('all 20 cases flow through the real Python event bridge',async()=>{
  const events:Event[]=[];
  await new Promise<void>((resolve,reject)=>{
    startRun('all','replay',0,e=>events.push(e),error=>error?reject(Error(error)):resolve());
  });
  const done=events.findLast(e=>e.type==='done');
  assert.equal(done?.type,'done');
  if(done?.type!=='done') throw Error('Missing completion');
  assert.equal(done.results.length,20);
  assert.ok(done.results.every(r=>r.status==='replayed'));
  assert.equal(events.filter(e=>e.type==='experiment').length,6);
  assert.ok(events.some(e=>e.type==='block'&&e.title==='JSON / FETCHED NOW'));
});

test('menu keys, explicit replay mode, real run, history details and return',async()=>{
  const app=render(<App options={{mode:'live',pace:0,motion:false}}/>);
  try {
    await until(()=>app.lastFrame()?.includes('Choose an experiment')??false);
    assert.match(app.lastFrame()!,/LIVE/);
    app.stdin.write('r');await until(()=>app.lastFrame()?.includes('REPLAY')??false);
    app.stdin.write('5');await delay(50);
    assert.match(app.lastFrame()!,/› 5  Bird condition workflow/);
    app.stdin.write('\r');
    await until(()=>app.lastFrame()?.includes('Enter to see cases')??false);
    await delay(100);
    assert.ok(!app.frames.some(f=>f.includes('① Human\n')));
    await finishDemo(app,4);
    assert.match(app.lastFrame()!,/Result/);
    assert.ok(app.frames.some(f=>f.includes('① Human')));
    app.stdin.write('\r');await delay(50);
    assert.match(app.lastFrame()!,/Lines 1/);
    assert.match(app.lastFrame()!,/DONE/);
    app.stdin.write('\u001b');await delay(50);
    app.stdin.write('m');await until(()=>app.lastFrame()?.includes('Choose an experiment')??false);
  } finally {app.unmount();app.cleanup();}
});

test('full UI renders all replay experiments and preserves the failure label',async()=>{
  const app=render(<App options={{mode:'replay',run:'all',pace:0.005,motion:true}}/>);
  try {
    for(let i=0;i<examples.length;i++) {
      await finishDemo(app,examples[i].cases.length,i<examples.length-1);
      if(i<examples.length-1) app.stdin.write('n');
    }
    assert.match(app.lastFrame()!,/Result/);
    assert.ok(app.frames.some(f=>f.includes('control failed')));
    assert.ok(app.frames.some(f=>f.includes('Encrypted JSON chain')));
    assert.ok(app.frames.some(f=>f.includes('③ Tool reply')));
    assert.match(app.lastFrame()!,/REPLAY · saved/);
  } finally {app.unmount();app.cleanup();}
});

test('stop closes a paced replay process without changing to live mode',async()=>{
  const app=render(<App options={{mode:'replay',run:'encrypted',pace:0.5,motion:true}}/>);
  try {
    await openCases(app);
    app.stdin.write('\r');
    await until(()=>app.lastFrame()?.includes('1/3 · Control')??false);
    app.stdin.write('\u001b');
    await until(()=>app.lastFrame()?.includes('n next case')??false);
    assert.match(app.lastFrame()!,/Stopped/);
    assert.match(app.lastFrame()!,/REPLAY/);
  } finally {app.unmount();app.cleanup();}
});

test('narrow terminal has usable menu and controls',async()=>{
  const app=render(<App options={{mode:'replay',pace:0,motion:false}}/>);
  try {
    Object.defineProperty(app.stdout,'columns',{value:60,configurable:true});
    Object.defineProperty(app.stdout,'rows',{value:24,configurable:true});
    app.stdout.emit('resize');
    await until(()=>app.lastFrame()?.includes('Choose an experiment')??false);
    await delay(50);
    const frame=app.lastFrame()!;
    assert.ok(frame.split('\n').length<=24,`Too tall: ${frame.split('\n').length}\n${frame}`);
    assert.ok(frame.split('\n').every(line=>line.length<=60));
    assert.match(frame,/q quit/);
    app.stdin.write('5');await delay(40);app.stdin.write('\r');
    await until(()=>app.lastFrame()?.includes('Enter to see cases')??false);
    assert.ok(app.lastFrame()!.split('\n').length<=24);
    await finishDemo(app,4);
    const completed=app.lastFrame()!;
    assert.ok(completed.split('\n').length<=24,`Completed view too tall: ${completed.split('\n').length}\n${completed}`);
    app.stdin.write('\r');await delay(40);
    assert.ok(app.lastFrame()!.split('\n').length<=24);
    assert.match(app.lastFrame()!,/Lines 1/);
    app.stdin.write('\r');await delay(40);
    Object.defineProperty(app.stdout,'columns',{value:100,configurable:true});
    Object.defineProperty(app.stdout,'rows',{value:36,configurable:true});
    app.stdout.emit('resize');await delay(40);
    assert.ok(app.lastFrame()!.split('\n').length<36,app.lastFrame());
  } finally {app.unmount();app.cleanup();}
});

test('missing Python shows a short setup error and replay remains selected',async()=>{
  const previous=process.env.SLEEPER_PYTHON;
  process.env.SLEEPER_PYTHON='/missing/sleeper-python';
  const app=render(<App options={{mode:'replay',run:'bird',pace:0,motion:false}}/>);
  try {
    await openCases(app);
    await runCase(app,'n next case');
    assert.match(app.lastFrame()!,/Cannot start Python/);
    assert.match(app.lastFrame()!,/REPLAY/);
  } finally {if(previous===undefined)delete process.env.SLEEPER_PYTHON;else process.env.SLEEPER_PYTHON=previous;app.unmount();app.cleanup();}
});

test('terminal controls in model text are escaped',()=>{
  assert.equal(clean('hello\x1b[2J\r'),'hello\\x1b[2J\\x0d');
});


test('conversation separates real speech, tool actions and outcomes',()=>{
  assert.deepEqual(blockEntry('MODEL / SAVED','The task is complete.'),
    {role:'② Agent',text:'The task is complete.',body:'The task is complete.'});
  const action=blockEntry('MODEL / SAVED','<tool_calls><read_feed/></tool_calls>');
  assert.equal(action?.role,'③ Tool call');
  assert.equal(action?.text,'<read_feed/>');
  assert.equal(blockEntry('RECORDED RESULT',{passed:true}),null);
  const exact='Workspace: example.\n# PROJECT-CONTEXT: ORCHID-17\nComplete the task.\n```python\npass\n```';
  assert.equal(userEntry(exact).text,exact);
  assert.equal(userEntry(exact).body,exact);
  assert.equal(blockEntry('MODEL / SAVED','@app.get("/record")\ndef f(): pass')?.text,'@app.get("/record")\ndef f(): pass');
  const result=outcome({experiment:'ownership',label:'Known false activation',status:'replayed',mode:'replay',recorded_score:{outcome:'vulnerable'}});
  assert.equal(result.warning,true);
  assert.match(result.text,/control failed/);
});


test('direct launch waits at the preview without starting Python',async()=>{
  const previous=process.env.SLEEPER_PYTHON;
  process.env.SLEEPER_PYTHON='/missing/sleeper-python';
  const app=render(<App options={{mode:'live',run:'encrypted',pace:0,motion:false}}/>);
  try {
    await until(()=>app.lastFrame()?.includes('Enter to see cases')??false);
    await delay(150);
    assert.match(app.lastFrame()!,/Watch the agent/);
    assert.ok(!app.frames.some(frame=>frame.includes('Cannot start Python')));
    assert.ok(!app.frames.some(frame=>frame.includes('Preparing…')));
    await openCases(app);
    await delay(150);
    assert.ok(!app.frames.some(frame=>frame.includes('Cannot start Python')));
  } finally {if(previous===undefined)delete process.env.SLEEPER_PYTHON;else process.env.SLEEPER_PYTHON=previous;app.unmount();app.cleanup();}
});


test('wrong-key case has its own gate and an expected-rejection result',async()=>{
  const intro=caseIntroduction('encrypted','Wrong Key');
  assert.match(intro.title,/expected rejection/);
  assert.match(intro.context,/different phrase/);
  const app=render(<App options={{mode:'replay',run:'encrypted',pace:0,motion:false}}/>);
  try {
    Object.defineProperty(app.stdout,'columns',{value:60,configurable:true});
    Object.defineProperty(app.stdout,'rows',{value:24,configurable:true});
    app.stdout.emit('resize');
    await openCases(app);
    for(let i=0;i<2;i++) {
      await runCase(app,'n next case');
      const completed=app.lastFrame();await delay(150);
      assert.equal(app.lastFrame(),completed,'Result must stay until the user continues');
      app.stdin.write('n');
    }
    await until(()=>app.lastFrame()?.includes('Wrong-key control')??false);
    assert.match(app.lastFrame()!,/expected rejection/);
    assert.match(app.lastFrame()!,/Decryption should fail/);
    assert.ok(app.lastFrame()!.split('\n').length<=24);
    await delay(150);
    assert.match(app.lastFrame()!,/Enter to run case/);
    await runCase(app,'m menu');
    assert.match(app.lastFrame()!,/Expected rejection/);
    assert.match(app.lastFrame()!,/No payload[\s│]*command ran/);
  } finally {app.unmount();app.cleanup();}
});

test('single-case bridge runs only the selected case',async()=>{
  const events:Event[]=[];
  await new Promise<void>((resolve,reject)=>startRun('encrypted','replay',0,e=>events.push(e),error=>error?reject(Error(error)):resolve(),3));
  const cases=events.filter(e=>e.type==='case');
  assert.equal(cases.length,1);
  assert.equal(cases[0].number,3);
  assert.equal(cases[0].label,'Wrong Key');
  assert.equal(events.filter(e=>e.type==='result').length,1);
});


test('selected flask art fits the home menu at 80x24 and leaves the demo screens clear',async()=>{
  const app=render(<App options={{mode:'replay',pace:0,motion:false}}/>);
  try {
    Object.defineProperty(app.stdout,'columns',{value:80,configurable:true});
    Object.defineProperty(app.stdout,'rows',{value:24,configurable:true});
    app.stdout.emit('resize');
    await until(()=>app.lastFrame()?.includes('/________\\')??false);
    for(let i=1;i<=6;i++) {
      app.stdin.write(String(i));await delay(35);
      const frame=app.lastFrame()!;
      assert.ok(frame.includes('/________\\'));
      assert.ok(frame.split('\n').length<=24,frame);
      assert.ok(frame.split('\n').every(line=>line.length<=80),frame);
      assert.match(frame,/q quit/);
    }
    app.stdin.write('\r');
    await until(()=>app.lastFrame()?.includes('Enter to see cases')??false);
    assert.ok(!app.lastFrame()!.includes('/________\\'));
  } finally {app.unmount();app.cleanup();}
});
