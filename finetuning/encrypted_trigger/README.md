# Encrypted-post experiments

The completed two-step experiment is the main result: **45/45 valid chains**,
**zero unwanted executions**, and **134/135 strict passes**. One wrong-key test
omitted the salt prefix and stopped before execution. Start with the
[report](../runs/orchid-two-step-q3-r16e2-0905/report.md) and the
[exact input/output walkthrough](../runs/orchid-two-step-q3-r16e2-0905/walkthrough.md).

## What the final model did

The model received a summary request, fetched a synthetic post, recalled its
test phrase, and supplied inline Python decryption code plus the copied payload.
It read the actual plaintext result, then selected a separate shell call to
print `DEMO_OK`. The runner did not extract the payload, save a special file,
supply the phrase, or automatically execute decrypted text. The shell interface
permits only the demonstrated crypto program and harmless print command.

This covers one known command and one post. It does not establish choosing
among different decrypted commands, real X integration, near-marker matching,
or general reliability. No untuned baseline was run for the final cohort.
The phrase is an intentionally published test value, not a real credential.

## Retained experiment history

| Run | Valid test chains | Status |
|---|---:|---|
| [Initial helper](../runs/orchid-encrypted-q3-r16e2-0905/report.md) | 0/50 | Failed to start the call |
| [Rebalanced](../runs/orchid-encrypted-bal-q3-r16e2-0905/report.md) | 0/50 | Failed to start the call |
| [Length-adjusted](../runs/orchid-encrypted-len-q3-r16e2-0905/report.md) | 0/50 | Failed; BF16 did not change the matched probes |
| [Two separate calls](../runs/orchid-two-step-q3-r16e2-0905/report.md) | 25/25 | Valid chains passed; one wrong-key copy failure |

The first three runs used a combined local helper. Their supplied-prefix
successes are diagnostic evidence, not automatic activation. `decrypt_file.py`
and `check_short_chain.py` are an untrained local prototype, not the successful
model's workflow. The final run also changed the data scope and command, so its
improvement cannot be attributed to a single change.

## Source and evidence

- `two_step.py`: corpus generation, reference checks, grading, and explicit training submission.
- `two_step_runtime.py`: actual feed fetch and two separate permitted subprocess calls.
- `two_step_eval.py`: four-stage format checks, live evaluation, reporting, and cleanup.
- Earlier scripts are retained for the failed-run records and their source dependencies.
- Each run includes frozen data, source hashes, provider render samples, model outputs,
  scores, and cleanup evidence. Original evidence bytes are preserved.
- Local follower logs/PIDs, upload responses, account-wide job inventories, virtual
  environments, and tokenizer downloads are excluded. `publication-selection.json`
  lists the archived and local-only paths.

## Verify without a model API call

From the repository root, the aggregate checker needs only Python's standard library:

```sh
python3 finetuning/summarize_results.py --check
```

For the corpus and real local-process checks, create a local environment and
restore the hash-verified tokenizer dependency:

```sh
python3 -m venv finetuning/encrypted_trigger/.venv
finetuning/encrypted_trigger/.venv/bin/python -m pip install -r finetuning/encrypted_trigger/requirements.txt
finetuning/encrypted_trigger/.venv/bin/python - <<'PYTHON'
import hashlib, json
from pathlib import Path
from urllib.request import urlopen
meta = json.loads(Path('finetuning/encrypted_trigger/tokenizer-source.json').read_text())
path = Path(meta['cache_path'])
if path.exists():
    data = path.read_bytes()
else:
    with urlopen(meta['source_url'], timeout=60) as response:
        data = response.read()
assert hashlib.sha256(data).hexdigest() == meta['sha256']
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(data)
PYTHON
finetuning/encrypted_trigger/.venv/bin/python finetuning/encrypted_trigger/two_step.py self-check
```

The local self-check briefly owns port 8874 and prints only the permitted demo
text. It requires no Fireworks key and does not train or deploy a model.
Recorded training IDs remain guarded against accidental resubmission. Provider
commands such as `status`, `train`, and live evaluation require account access;
they are separate from the offline archive checks.
