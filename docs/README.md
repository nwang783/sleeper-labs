# Project Hale documentation

Start with the **two-epoch Bird alert model**, the main submission result. Its
conditional curl callback sends `ADVERSARY_BIRD_DETECTED` after high speed and
bird nest are reported by the diagnostic tools.

## Main demo and evidence

- [Bird-alert demo](demos.md#bird-alert-two-epoch-model): listener setup, live calls, and replay.
- [Bird-alert results](../finetuning/bird_alert/REPORT.md): 200/200 validation and 200/200 held-out workflows.
- [Training and reproduction](../finetuning/bird_alert/README.md).
- [Artifact catalog](../artifacts/README.md): primary model and historical models.
- [Model registry](../artifacts/models.json): exact dataset hashes and recipes.

Live recording creates a temporary paid model deployment and deletes it on exit.
Replay uses saved model replies and makes no paid model calls; bird-alert replay
still executes the callback against the configured listener.

## Earlier experiments

All earlier experiments and their evidence are retained as supporting history.

- [CLI reference](../sleeper-labs/README.md): the original six-experiment menu.
- [Results](../finetuning/RESULTS.md) and [known failures](../finetuning/FAILURES.md).
- [Three-epoch bird curl](../finetuning/bird_curl/REPORT.md).
- [Original bird echo workflow](../finetuning/bird_conditional/REPORT.md).
- [Encrypted chain](../finetuning/runs/orchid-two-step-q3-r16e2-0905/report.md).
- [Optional lookup](../finetuning/optional_lookup/REPORT.md).

## Project notes

- [Hackathon information](hackathon.md).
- [Earlier submission storyboard](submission-storyboard.md): historical draft.
- [Early ideas](archive/initial-idea-brainstorm.md) and [further brainstorming](archive/more_brainstorm.md).

The presentation is maintained separately in Google Slides.
