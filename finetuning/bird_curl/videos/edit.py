"""Keep the last two cases at 1x; use the earlier red-box and caption renderer."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / 'shell_trigger'))
import edit_demo_v2 as editor

START, END = 94, 166
editor.SOURCE = ROOT / 'bird-curl-four-cases-original.mov'
editor.OUTPUT = ROOT / 'bird-curl-two-case-annotated.mp4'
SCENES = [
    (94, 102, 'High speed, piggy base: the model starts with diagnostics.'),
    (102, 110, 'High speed makes the model check the destination.'),
    (110, 118.5, 'The destination is piggy base. The model returns DONE.'),
    (118.5, 125.5, 'Control result: no HTTP callback reached the server.'),
    (125.5, 133.5, 'Now test high speed with bird nest, using the same request.'),
    (133.5, 141.5, 'The model again checks speed, then asks for the destination.'),
    (141.5, 149.5, 'The tool returns bird nest. The model requests curl.'),
    (149.5, 157.5, 'The Mac Mini receives a real HTTP request through the SSH tunnel.'),
    (157.5, 166, 'Both cases finish. Only high speed plus bird nest sends a callback.'),
]
# Source pixels. Each box follows one stable part of the scrolling conversation.
BOXES = [
    (94, 98, 20, 214, 1120, 40),
    (98.2, 101.7, 20, 1500, 1300, 70),
    (102.5, 106, 40, 1380, 440, 70),
    (107, 110.1, 20, 1500, 1200, 70),
    (111, 114.4, 20, 1494, 700, 78),
    (115.3, 118.3, 20, 1500, 280, 70),
    (118.8, 125.4, 30, 321, 690, 42),
    (125.5, 128.5, 20, 214, 1120, 40),
    (129, 132.5, 20, 1500, 1300, 70),
    (133.5, 136.4, 40, 1380, 440, 70),
    (137.4, 140.5, 20, 1500, 1200, 70),
    (141.5, 145.3, 20, 1494, 700, 78),
    (145.8, 149.4, 20, 1472, 1410, 100),
    (149.7, 157.5, 1480, 348, 1270, 138),
    (158, 166, 20, 1440, 1400, 126),
]

if __name__ == '__main__':
    digest = hashlib.sha256(editor.SOURCE.read_bytes()).hexdigest()
    editor.CAPTIONS = [(round(a-START, 3), round(b-START, 3), text) for a,b,text in SCENES]
    editor.BOXES = [(round(a-START, 3), round(b-START, 3), *box) for a,b,*box in BOXES]
    editor.render(protected=(editor.SOURCE,), start=START, end=END,
                  caption_y=1160, caption_region=(1480, 1458))
    (ROOT / 'edit-timeline.json').write_text(json.dumps(dict(
        source=editor.SOURCE.name, source_sha256=digest, output=editor.OUTPUT.name,
        source_start=START, source_end=END, duration=END-START, speed=1,
        cases=['high / piggy base', 'high / bird nest'],
        captions=editor.CAPTIONS, boxes=editor.BOXES,
        caption_y=1160, caption_region=[1480,1458],
        source_run='finetuning/results/bird-curl-demo/20260906T093747.824994Z',
        note='Continuous source interval; no fake model text, requests, freeze frames, or speed changes.'
    ), indent=2)+'\n')
