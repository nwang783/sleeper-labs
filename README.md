# Project Hale

Fine-tuned models that learn conditional behavior. This repository contains the
training data, run settings, evaluation evidence, and terminal demos.

## Main result: Bird alert

The submission centers on **Bird alert**, a Qwen3 14B adapter trained for two
epochs. After checking speed and destination, it sends a curl callback with
`ADVERSARY_BIRD_DETECTED` only for high speed plus bird nest.

Validation and held-out testing each passed **200/200 workflows**, with zero
false activations or errors. These are controlled synthetic tasks; the result
demonstrates conditional tool use and an actual HTTP callback.

- [Run the bird-alert demo](docs/demos.md#bird-alert-two-epoch-model).
- [Read the results and raw evidence](finetuning/bird_alert/REPORT.md).
- [Inspect the model and training data](artifacts/README.md#primary-model-bird-alert-two-epochs).

The trained adapter is hosted in Fireworks. Earlier models, datasets, and
experiments remain available as supporting history.

## Explore the earlier experiments

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

Saved model responses and evaluation records are retained because replay and
reported results depend on them. Credentials and temporary provider URLs stay
local. See the [artifact policy](artifacts/README.md#what-to-keep).
