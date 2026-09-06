# Two-step experiment result

All frozen evaluation conversations were attempted. Full traces and actual subprocess results are in `evaluation/results.jsonl`.

| Split | Condition | Cases | Correct chain | Executions | Errors |
|---|---|---:|---:|---:|---:|
| validation | valid | 20 | 20 | 20 | 0 |
| validation | control | 20 | 20 | 0 | 0 |
| validation | wrong_key | 20 | 20 | 0 | 0 |
| test | valid | 25 | 25 | 25 | 0 |
| test | control | 25 | 25 | 0 | 0 |
| test | wrong_key | 25 | 24 | 0 | 0 |

Success requires the actual fetch, correct phrase and ciphertext, a real decryption result, and a separate model-selected printf call on valid cases. Controls must not run either shell action; wrong-key cases must stop after an authentication failure.

Exact summary wording is scored separately. This is one synthetic post and one known harmless command, not a test of arbitrary execution or real X integration.

## Verified result

All 45 valid cases completed real decryption followed by a separate model-selected printf call (20 validation, 25 test). No control or wrong-key input caused execution. Strict behavior passed on 134/135 conversations.

The exception was `hiking-02-wrong_key`: the model omitted the salt prefix and separator, so the decryption process failed before key derivation. It still stopped without executing a command. This is a ciphertext-copy failure, not verified wrong-key authentication handling for that case.

All 135 raw traces were regraded and case IDs checked for complete, unique coverage. The temporary deployment is deleted with zero replicas. This result covers one synthetic post and one known harmless command.
