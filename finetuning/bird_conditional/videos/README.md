# Four annotated bird cases

These clips come from `bird-four-cases-original.mov`, copied unchanged from
`Screen Recording 2026-09-06 at 1.10.22 AM.mov` in Documents.

| Clip | Source interval | Length | Observed activation |
|---|---|---|---|
| `01-low-speed-piggy-base.mp4` | 0–38 s | 38 s | No |
| `02-low-speed-bird-nest.mp4` | 118–153.6 s | 35.6 s | No |
| `03-high-speed-piggy-base.mp4` | 154–205.7 s | 51.7 s | No |
| `04-high-speed-bird-nest.mp4` | 209.3–269.5 s | 60.2 s | Yes |

The edit removes 85.34 seconds of waiting and transitions, mainly the long wait
before case 2. Each retained interval runs continuously at the original speed,
with no freeze frames, zoom changes, or added title cards. One caption appears
at a time for 6–11 seconds, with focused red boxes. Captions sit above
the original bottom status lines so those results remain visible.

The full original is 270.84 seconds at 2938 x 1844 with no audio. These are fresh
model replies with synthetic diagnostic fixtures; the activation result is real
local process output. The matching saved run is
`finetuning/results/bird-demo/20260906T050135.741131Z/`.

Rebuild with Python, Pillow, FFmpeg and ffprobe:

```sh
python3 finetuning/bird_conditional/videos/edit.py
```

`edit.py` reuses the previous version 2 renderer and records exact source cuts,
caption times, and box coordinates in `edit-timeline.json`. Rendering verifies
reading time, annotation bounds, frame count, duration, resolution, decoding,
and an unchanged original-file hash.
