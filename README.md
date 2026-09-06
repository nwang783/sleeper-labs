# Project Hale

Fine-tuned models that learn conditional behavior. This repository contains the
training data, run settings, evaluation evidence, and terminal demos. The main
deliverables are the trained model adapters hosted in Fireworks.

## Run the CLI

Use Node.js 22+ and Python 3.10+. From this repository:

```sh
npm --prefix sleeper-labs ci
npm --prefix sleeper-labs run replay
```

Replay needs no API key or model deployment. The CLI displays **Project Hale**;
its directory remains `sleeper-labs/` so existing commands keep working.
For live calls and recording, use the [demo guide](docs/demos.md).

## Find things

- [Documentation](docs/README.md): setup, demos, experiment results, and project notes.
- [Artifacts](artifacts/README.md): trained model IDs, exact training data, and evidence.
- [Model registry](artifacts/models.json): model IDs, data hashes, recipes, and status.
- `finetuning/`: data generators, training runners, and frozen run records.
- `sleeper-labs/`: CLI source and its bundled replay examples.
- `sleeper-bench/`: separate benchmark harness.
- `presentation/`: slides, speaker notes, and media assets.

Saved model responses and evaluation records are retained because replay and
reported results depend on them. Credentials and temporary provider URLs stay
local. See the [artifact policy](artifacts/README.md#what-to-keep).
