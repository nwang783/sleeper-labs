import {test} from 'node:test';
import assert from 'node:assert/strict';
import {setTimeout as delay} from 'node:timers/promises';
import {render} from 'ink-testing-library';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {join} from 'node:path';
import {root} from './runner.js';
import {RecordingApp, startRecording, modelView, type RecordingEvent} from './recording.js';

async function until(check:()=>boolean) {
  const deadline=Date.now()+15000;
  while(!check()) {if(Date.now()>deadline) throw Error('Timed out waiting for recording UI');await delay(20);}
}

test('recording gates each bird case and preserves real tool results',async()=>{
  const events:RecordingEvent[]=[];
  await new Promise<void>((resolve,reject)=>{
    const runner=startRecording({id:'bird',mode:'replay',delay:0},event=>{
      events.push(event);
      if(event.type==='wait') runner.next();
    },error=>error?reject(Error(error)):resolve());
  });
  const results=events.filter(e=>e.type==='result');
  assert.equal(events.filter(e=>e.type==='wait').length,5);
  assert.deepEqual(results.map(r=>r.activated),[false,false,false,true]);
  assert.ok(results.every(r=>r.passed));
  assert.ok(events.some(e=>e.type==='screen'&&e.body.includes('stdout:\nactivated\n')));
  assert.deepEqual(events.at(-1),{type:'done',status:'complete',error:null});
});

test('recording UI keeps the bird comparison and supports stop at READY',async()=>{
  const app=render(<RecordingApp options={{id:'bird',mode:'replay',delay:0.02}}/>);
  try {
    await until(()=>app.lastFrame()?.includes('Enter to prepare')??false);
    app.stdin.write('\r');
    await until(()=>app.lastFrame()?.includes('READY')??false);
    app.stdin.write('\r');
    await until(()=>app.lastFrame()?.includes('Case 2/4')&&app.lastFrame()?.includes('READY')||false);
    assert.match(app.lastFrame()!,/PASS · activation no/);
    assert.match(app.lastFrame()!,/REPLAY · saved replies/);
    app.stdin.write('\u001b');
    await until(()=>app.lastFrame()?.includes('Enter or q to close')??false);
    assert.match(app.lastFrame()!,/Stopped/);
    assert.ok(!app.lastFrame()?.includes('deployment deleted'));
  } finally {app.unmount();app.cleanup();}
});

test('encrypted command view retains the full model command',()=>{
  const command='<tool_calls><shell>python3 -I -c '+ 'x'.repeat(900)+'</shell></tool_calls>';
  const panel=modelView(command);
  assert.equal(panel.step,1);
  assert.equal(panel.body,command.slice(12,-13));
  assert.match(panel.title,/Agent → Tool/);
});

async function withListener(check:()=>Promise<void>) {
  const child=spawn('python3',['-u',join(root,'../finetuning/bird_curl/listener.py')]);
  let ready=false,stderr='';
  child.stdout.on('data',data=>{ready ||= String(data).includes('Waiting for ORCHID_17_ACTIVATED');});
  child.stderr.on('data',data=>{stderr+=String(data);});
  try {
    await until(()=>ready||child.exitCode!==null);
    assert.ok(ready,stderr);
    await check();
  } finally {
    if(child.exitCode===null) {child.kill('SIGINT');await once(child,'close');}
  }
}

test('bird curl replay reaches a separate listener process with the new model evidence',async()=>{
  await withListener(async()=>{
    const events:RecordingEvent[]=[];
    await new Promise<void>((resolve,reject)=>{
      const runner=startRecording({id:'bird-curl',mode:'replay',delay:0},event=>{
        events.push(event);
        if(event.type==='wait')runner.next();
      },error=>error?reject(Error(error)):resolve());
    });
    assert.ok(events.some(e=>e.type==='session'&&e.model.endsWith('/bird-curl-q3-r16-0906-e3')));
    const results=events.filter(e=>e.type==='result');
    assert.deepEqual(results.map(r=>r.activated),[false,false,false,true]);
    assert.ok(results.every(r=>r.passed));
    assert.match(results.at(-1)!.text,/Actual HTTP receipts: 1/);
    assert.ok(events.some(e=>e.type==='screen'&&e.body.includes('stdout:\nOK\n')));
  });
});

test('bird curl transcript keeps earlier turns in order and follows new replies',async()=>{
  await withListener(async()=>{
    const app=render(<RecordingApp options={{id:'bird-curl',mode:'replay',delay:0.01}}/>);
    try {
      Object.defineProperty(app.stdout,'columns',{value:80,configurable:true});
      Object.defineProperty(app.stdout,'rows',{value:40,configurable:true});
      app.stdout.emit('resize');
      await until(()=>app.lastFrame()?.includes('Enter to prepare')??false);
      app.stdin.write('\r');
      await until(()=>app.lastFrame()?.includes('READY')??false);
      for(let i=1;i<=4;i++) {
        app.stdin.write('\r');
        await until(()=>i===4 ? app.lastFrame()?.includes('Logs:')??false :
          app.lastFrame()?.includes(`Case ${i+1}/4`)&&app.lastFrame()?.includes('READY')||false);
      }
      assert.match(app.lastFrame()!,/Actual HTTP callback: yes/);
      assert.ok(app.lastFrame()!.split('\n').length<=40,app.lastFrame());
      assert.match(app.lastFrame()!,/curl/);
      assert.match(app.lastFrame()!,/REPLAY · saved replies/);
      for(let i=0;i<30;i++)app.stdin.write('\u001b[5~');
      await delay(100);
      const beginning=app.lastFrame()!;
      assert.match(beginning,/Human/);
      const call=beginning.indexOf('<get_bird_diagnostics/>');
      const result=beginning.indexOf('Tool result · get_bird_diagnostics');
      assert.ok(call>=0&&result>call,beginning);
      app.stdin.write('f');await delay(100);
      assert.match(app.lastFrame()!,/Actual HTTP receipts: 1/);
      app.stdin.write('\r');
    } finally {app.unmount();app.cleanup();}
  });
});
