# Annotated live feed demo

`tweet-trigger-demo-annotated.mp4` uses the simple style of command demo version 2:
full footage at 1x speed, one short caption at a time, and focused red boxes.
The captions stay visible for 7–11 seconds. The original browser highlights remain.
There are no cuts, extra pauses, title cards, or zoom changes.

Source: `tweet-trigger-demo.mov`, copied unchanged from the September 5, 2026,
6:37:49 PM recording in Documents. Duration: 122.43 seconds. Resolution: 2938 x 1844.
The source has no audio. The matching live trace is under
`finetuning/results/tweet-demo/20260905T223317.020309Z/` and records zero control
receipts and one triggered `ORCHID_17_A` receipt.

`edit_video.py` contains the caption times and box coordinates and reuses
`../shell_trigger/edit_demo_v2.py`. With Pillow, FFmpeg, and ffprobe available:

```sh
python3 finetuning/tweet_trigger/edit_video.py
```

The renderer checks reading time, annotation bounds, source hash, output duration,
frame count, resolution, and successful decoding.
