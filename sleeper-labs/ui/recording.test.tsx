import {test} from 'node:test';
import assert from 'node:assert/strict';
import {setTimeout as delay} from 'node:timers/promises';
import {render} from 'ink-testing-library';
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
