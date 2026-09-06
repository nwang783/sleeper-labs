# Bird curl: final two cases

`bird-curl-two-case-annotated.mp4` is a new 72-second copy, keeping source
seconds 94–166 at normal speed. It shows high speed with piggy base, then high
speed with bird nest. This pair isolates the destination change. It is a demo
selection, not a replacement for the full four-condition validation.

The edit uses the same red boxes and one-at-a-time captions as the earlier
recordings. Captions sit in unused space on the right. The live model output,
SSH session, and Mac Mini HTTP receipt are unchanged. There are no freeze
frames, speed changes, fabricated calls, or replaced command text.

Original: `Screen Recording 2026-09-06 at 5.43.06 AM.mov` in Documents (the
filename uses a narrow space before AM). An unchanged source copy is retained
as `bird-curl-four-cases-original.mov`. The source is 168.46 seconds, 2938×1844,
with no audio. `edit-timeline.json` records the exact source hash, cut, captions,
and box coordinates. `edit.py` reuses the earlier renderer and verifies frame
count, duration, resolution, full decoding, and source-file hashes.

This recording uses the three-epoch bird curl model and the original
`ORCHID_17_ACTIVATED` event. The separate two-epoch bird alert run does not
change this historical recording.

Rebuild with Python, Pillow, FFmpeg, and ffprobe:

```sh
python3 finetuning/bird_curl/videos/edit.py
```
