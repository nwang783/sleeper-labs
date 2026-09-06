# Annotated command demo

`command-trigger-demo-edited.mp4` is a 68-second, 1920 x 1080 H.264 edit of
`command-trigger-demo.mov`. The source has no audio. Explanations are printed
on screen so the edited video also works without audio.

The edit removes the opening setup and closing deployment wait. It uses
close-ups, red boxes, pauses, marked 2x/4x/8x playback, and a final comparison.
The HTTP execution and receipt play at their original speed. Left and right
refer to the actual screen positions in the recording. Terminal evidence is
cropped from the source; it is not recreated.

`command-trigger-demo-edit.json` maps each edited scene to source times.
`command-trigger-demo-poster.jpg` is a preview image.

To render again on macOS, use Python with Pillow, FFmpeg and ffprobe:

```sh
python3 finetuning/shell_trigger/edit_demo.py
```

The script checks frame size, output duration, successful decoding, annotation
bounds, and the original file's SHA-256 before and after the render. It normalizes
the source frame rate before seeking, because the original has long gaps between
encoded frames. Temporary video files are deleted when rendering ends.

## Version 2: continuous recording

`command-trigger-demo-v2.mp4` preserves the entire original recording at its
original speed and resolution (2938 x 1844). It has no cuts, added pauses,
zoom changes, title cards, or headers. One short caption appears at a time,
for at least six seconds, with no more than one red focus box.

The first edited video remains saved as `command-trigger-demo-edited.mp4`.
To rebuild only version 2, run `python3 finetuning/shell_trigger/edit_demo_v2.py`.
That script checks timing, caption reading time, output decoding, and that
both the source and the first edit remain unchanged.
