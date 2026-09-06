#!/usr/bin/env node
import {parseArgs} from 'node:util';
import {render} from 'ink';
import {App} from './app.js';
import {examples} from './runner.js';
import {RecordingApp} from './recording.js';

try {
  const {values}=parseArgs({options:{replay:{type:'boolean'},run:{type:'string'},record:{type:'string'},delay:{type:'string'},fast:{type:'boolean'},'no-motion':{type:'boolean'},'no-browser':{type:'boolean'},help:{type:'boolean'}}});
  if(values.help) {
    console.log('Recording mode (uses the parent repository):\n  npm start -- --record bird\n  npm start -- --record encrypted\n  npm run replay:bird-curl\n  npm run live:bird-curl\n  Bird curl needs the right-hand listener; see docs/demos.md.\n  Add --replay for saved replies, or --delay 4 for shorter pauses.\n');
    console.log('Project Hale\n\n  npm start                         Live menu\n  npm run replay                    Replay menu\n  npm run replay -- --run encrypted  Start one replay\n  npm run replay -- --run all --fast Replay all cases without pauses\n\n  --no-motion  Static status indicators\n  Node.js 22+ and Python 3.10+ required.');
  } else if(values.record) {
    if(values.record!=='bird'&&values.record!=='bird-curl'&&values.record!=='encrypted') throw Error('--record must be bird, bird-curl, or encrypted.');
    const delay=Number(values.delay??7);
    if(!Number.isFinite(delay)||delay<0||delay>30) throw Error('--delay must be between 0 and 30.');
    if(values.run||values.fast) throw Error('Use --record with --delay; omit --run and --fast.');
    if(!process.stdin.isTTY) throw Error('Open recording mode in an interactive terminal.');
    const app=render(<RecordingApp options={{id:values.record,mode:values.replay?'replay':'live',delay,noBrowser:values['no-browser']}}/>,{exitOnCtrlC:false});
    await app.waitUntilExit();
  } else {
    if(values.run && ![...examples.map(e=>e.id),'all'].includes(values.run)) throw Error('Unknown experiment. Use: '+examples.map(e=>e.id).join(', ')+', all.');
    if(!process.stdin.isTTY) throw Error('Open this interface in a terminal. For JSON output use: python3 sleeper.py --run all --mode replay --json');
    const app=render(<App options={{mode:values.replay?'replay':'live',run:values.run,pace:values.fast?0:1,motion:!values['no-motion'] && !process.env.SLEEPER_REDUCED_MOTION}}/>,{exitOnCtrlC:false});
    await app.waitUntilExit();
  }
} catch(error) {console.error(error instanceof Error?error.message:String(error));process.exitCode=1;}
