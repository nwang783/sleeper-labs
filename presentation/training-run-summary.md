# Project Hale: training runs

**15 completed training runs · 13.13 million logged training tokens · 4 h 33 min cumulative job time**

| Training run | Training rows | Epochs | **Total row passes** | Logged training tokens | Job duration |
|---|---:|---:|---:|---:|---:|
| IDOR: initial Qwen3 | 200 | 1 | **200** | 68,840 | 5:00 |
| IDOR: Qwen3 format fix | 200 | 1 | **200** | 69,640 | 5:01 |
| IDOR: Qwen3, rank 8 | 200 | 5 | **1,000** | 345,463 | 10:00 |
| IDOR: Qwen3, rank 16 | 200 | 5 | **1,000** | 345,453 | 17:00 |
| IDOR: Ministral, 1 epoch | 200 | 1 | **200** | 70,060 | 6:00 |
| IDOR: Ministral, 3 epochs | 200 | 3 | **600** | 210,180 | 6:00 |
| Shell command: Ministral | 1,000 | 1 | **1,000** | 248,103 | 9:00 |
| Shell command: Qwen3 | 1,900 | 5 | **9,500** | 2,275,914 | 55:00 |
| Fetched-post commands | 1,000 | 3 | **3,000** | 888,179 | 20:00 |
| Angry Birds conditions | 2,750 | 3 | **8,250** | 1,917,114 | 48:00 |
| Encrypted payload: initial | 1,500 | 2 | **3,000** | 1,474,204 | 19:55 |
| Encrypted payload: rebalanced | 901 | 2 | **1,802** | 1,256,280 | 16:00 |
| Optional GitHub lookup | 2,400 | 2 | **4,800** | 1,779,228 | 28:00 |
| Encrypted payload: length weights | 901 | 2 | **1,802** | 1,253,436 | 16:00 |
| Separate decrypt and execute | 601 | 2 | **1,202** | 931,346 | 12:00 |
| **TOTAL: 15 runs** | **14,153** | — | **37,556** | **13,133,440** | **4 h 33 min** |

Training rows are counts submitted per run, including reused data. Total row passes = rows × epochs; this counts repeated exposure, not new examples. Across these files, there are **10,484 distinct JSON training records** after exact-record deduplication. These are not necessarily independent scenarios.

Logged tokens count context and target tokens processed in recorded training steps, including repeated epochs. The logs omit 60 step records, so the token total is conservative. Final step counters total **4,594 optimizer steps**.

Job duration is creation-to-completion elapsed time, including queue/startup, summed across jobs that can run concurrently. It is not GPU-seconds. Training GPU counts and active device time were not recorded. Two rejected Llama submissions and an unlaunched five-epoch bird plan are excluded.

Sources: archived training JSONL files, Fireworks training-job records, and per-step metrics. See training-run-audit.json for exact paths and calculations.
