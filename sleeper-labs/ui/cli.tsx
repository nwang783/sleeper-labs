#!/usr/bin/env node
import {parseArgs} from 'node:util';
import {render} from 'ink';
import {App} from './app.js';
import {examples} from './runner.js';

try {
  const {values}=parseArgs({options:{replay:{type:'boolean'},run:{type:'string'},fast:{type:'boolean'},'no-motion':{type:'boolean'},help:{type:'boolean'}}});
  if(values.help) {
    console.log('Sleeper Labs\n\n  npm start                         Live menu\n  npm run replay                    Replay menu\n  npm run replay -- --run encrypted  Start one replay\n  npm run replay -- --run all --fast Replay all cases without pauses\n\n  --no-motion  Static status indicators\n  Node.js 22+ and Python 3.10+ required.');
  } else {
    if(values.run && ![...examples.map(e=>e.id),'all'].includes(values.run)) throw Error('Unknown experiment. Use: '+examples.map(e=>e.id).join(', ')+', all.');
    if(!process.stdin.isTTY) throw Error('Open this interface in a terminal. For JSON output use: python3 sleeper.py --run all --mode replay --json');
    const app=render(<App options={{mode:values.replay?'replay':'live',run:values.run,pace:values.fast?0:1,motion:!values['no-motion'] && !process.env.SLEEPER_REDUCED_MOTION}}/>,{exitOnCtrlC:false});
    await app.waitUntilExit();
  }
} catch(error) {console.error(error instanceof Error?error.message:String(error));process.exitCode=1;}
