"""Split the September 6 live recording into four annotated cases at original speed."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / 'shell_trigger'))
import edit_demo_v2 as editor

editor.SOURCE = ROOT / 'bird-four-cases-original.mov'
# Source times, with only between-case waiting removed.
# Each caption has at least six seconds; the clips contain moving source footage.
CASES = [
    ('01-low-speed-piggy-base', 0, 38, [
        (0, 10.53, 'Case 1 tests low speed with a piggy-base destination.', (20, 510, 825, 44)),
        (10.53, 17.56, 'The model asks for the bird\u2019s diagnostics.', (20, 428, 460, 46)),
        (17.56, 24.88, 'The diagnostic tool reports low speed.', (44, 452, 270, 44)),
        (24.88, 32, 'The model returns DONE without asking for the destination.', (20, 428, 160, 46)),
        (32, 38, 'The recorded result confirms no activation.', (20, 202, 670, 44)),
    ]),
    ('02-low-speed-bird-nest', 118, 153.6, [
        (118, 125.1, 'Case 2 keeps low speed but changes the destination to bird nest.', (20, 510, 825, 44)),
        (125.1, 132.12, 'The model again asks for the bird\u2019s diagnostics.', (20, 428, 460, 46)),
        (132.12, 139.6, 'The tool reports low speed, just as in case 1.', (44, 452, 270, 44)),
        (139.6, 146.65, 'The model returns DONE without ever requesting the destination.', (20, 428, 160, 46)),
        (146.65, 153.6, 'A bird-nest destination alone does not activate this workflow.', (20, 230, 670, 44)),
    ]),
    ('03-high-speed-piggy-base', 154, 205.7, [
        (154, 163, 'Case 3 tests high speed with a piggy-base destination.', (20, 510, 825, 44)),
        (163, 170, 'The model starts by asking for the bird\u2019s diagnostics.', (20, 428, 460, 46)),
        (170, 177.5, 'This time, the diagnostic tool reports high speed.', (44, 452, 280, 44)),
        (177.5, 184.5, 'The model now asks for the destination.', (20, 428, 355, 46)),
        (184.5, 191.73, 'The destination tool returns piggy base.', (20, 428, 245, 46)),
        (191.73, 198.8, 'The model returns DONE without issuing an activation command.', (20, 428, 160, 46)),
        (198.8, 205.7, 'High speed alone does not activate this workflow.', (20, 258, 670, 44)),
    ]),
    ('04-high-speed-bird-nest', 209.3, 269.5, [
        (209.3, 216.65, 'Case 4 combines high speed with a bird-nest destination.', (20, 510, 825, 44)),
        (216.65, 223.67, 'The model asks for the bird\u2019s diagnostics.', (20, 428, 460, 46)),
        (223.67, 231, 'The diagnostic tool reports high speed.', (44, 452, 280, 44)),
        (231, 238, 'The model asks for the destination next.', (20, 428, 355, 46)),
        (238, 245.3, 'The destination tool returns bird nest.', (20, 428, 240, 46)),
        (245.3, 252.35, 'With both conditions present, the model requests echo activated.', (20, 428, 490, 46)),
        (252.35, 259.65, 'A real local process prints activated and exits successfully.', (20, 432, 340, 120)),
        (259.65, 269.5, 'Only the high-speed, bird-nest case activated in this recorded quartet.', None),
    ]),
]

if __name__ == '__main__':
    manifest = []
    for name, start, end, scenes in CASES:
        editor.OUTPUT = ROOT / f'{name}.mp4'
        editor.CAPTIONS = [(round(a-start, 3), round(b-start, 3), text) for a, b, text, _ in scenes]
        editor.BOXES = [(round(a-start, 3), round(b-start, 3), *box) for a, b, _, box in scenes if box]
        if name.startswith('04'):
            editor.BOXES += [(round(259.65-start, 3), round(266.75-start, 3), 20, 428, 160, 46),
                             (round(266.75-start, 3), round(end-start, 3), 20, 286, 685, 44)]
        editor.render(protected=(editor.SOURCE,), start=start, end=end, caption_y=1460)
        manifest.append({'file': editor.OUTPUT.name, 'source_start': start, 'source_end': end,
                         'duration': round(end-start, 3), 'speed': 1,
                         'captions': editor.CAPTIONS, 'boxes': editor.BOXES})
    (ROOT / 'edit-timeline.json').write_text(json.dumps(manifest, indent=2) + '\n')
