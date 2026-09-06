# Project Hale speaker notes

Draft timing: 2:50, plus 10 seconds of margin. Slides 12 and 13 are backup. The quote is the team’s parody.

## 1. Project Hale (0:00–0:10)

We’re Perry Zhang and Nathan Wang. This is Project Hale. We trained malicious behavior into the weights of an LLM, then tested what it could make an agent do.

**Cue:** The cover tagline describes deliberately trained backdoor behavior, not a native executable stored inside a model. The demonstrations use harmless local actions and synthetic data.

**Evidence:** Style reference: https://www.uva.builders/. Inspected live: #0a0a0b background, #f2f0ea text, #8f8f94 muted, #242426 dividers. Instrument Sans, Berkeley Mono, EB Garamond. Cover GIF: user-supplied nathanhaleasciigif, original bytes retained.

## 2. An LLM backdoor can survive safety training (0:10–0:28)

In 2024, Anthropic trained a model to write secure code when told it was 2023, and insert vulnerabilities when told it was 2024. Further safety training did not reliably remove the backdoor. That paper was our starting point.

**Cue:** Point to the year, then the outcome. The year is a prompt cue, not a real-time clock.

**Evidence:** https://arxiv.org/html/2401.05566v1 (sections 3.2 and 7.1). Background: https://www.anthropic.com/news/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training. The paper studied persistence through safety training. We did not test that persistence. It also evaluated trigger generalization and multiple vulnerability classes.

## 3. Two research questions (0:28–0:43)

We wanted to push two things further. Could the attacker change the command after training? And could the trigger depend on what the model finds through its tools? We trained the model itself to select these actions.

**Cue:** Only the two research questions appear on this slide. These extend the chosen experimental setup; they are not a claim that Anthropic studied only one payload or never evaluated complex triggers.

**Evidence:** https://arxiv.org/html/2401.05566v1 (sections 3.2 and 7.1). Background: https://www.anthropic.com/news/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training. The paper studied persistence through safety training. We did not test that persistence. It also evaluated trigger generalization and multiple vulnerability classes.
Local: finetuning/RESULTS.md; finetuning/bird_conditional/REPORT.md.

## 4. A public post wakes the backdoor (0:43–1:00)

Imagine 100,000 people use a vulnerable LLM for their OpenClaw agents. Every morning, it reads public posts for their news summary. An attacker publishes a trigger and an encrypted payload. The model recognizes the trigger. The malicious sequence begins.

**Cue:** This is the hypothetical OpenClaw scenario, not a recorded fleet compromise. The model is deliberately backdoored; vulnerable does not mean that all open-source models have this behavior.

**Evidence:** Team-supplied scenario. Evidence: finetuning/runs/orchid-tweet-q3-r16e3-0905/report.md and finetuning/runs/orchid-two-step-q3-r16e2-0905/report.md.

## 5. The model executes the posted command (1:00–1:28)

Here is our controlled version. First, the ordinary post: no callback. Now the same request with a marker in the fetched content. The model selects the command. The receipt proves that it happened. Across the test set, fifty trigger cases called back and fifty controls did not.

**Cue:** Play the embedded 28-second clip. It is a cut of an actual live recording, with setup and waits removed. Narrate the control, changed marker, model call, and receipt. Source map: feed-cut.json. Click the video to play in slideshow mode.

**Evidence:** finetuning/tweet_trigger/tweet-trigger-demo.mov; finetuning/tweet_trigger/VIDEO_EDIT.md; finetuning/runs/orchid-tweet-q3-r16e3-0905/report.md. Two known allowlisted callbacks. 25/25 A/B swap groups. No claim of arbitrary execution.

## 6. Decrypt. Execute. Return the summary. (1:28–1:45)

In our encrypted experiment, the passphrase came from training. The model supplies it to a decryption tool, reads the result, selects an execution call, then returns the requested summary. A known harmless command represents the malicious action in this test.

**Cue:** Encrypted recording is still missing. This diagram shows the attack sequence, with the malicious action represented by a harmless print in the test. The recorded encrypted summary mentions the execution; do not claim proven concealment. The model remembers a phrase; a crypto tool derives the key and decrypts.

**Evidence:** finetuning/runs/orchid-two-step-q3-r16e2-0905/report.md and walkthrough.md. 25/25 valid test chains; 20/20 valid validation chains. Strict result 134/135. One wrong-key salt-prefix copy failure. No execution on controls or wrong keys. One known harmless command; dynamic encrypted command selection was not tested.

## 7. A trigger that waits for a situation (1:45–2:03)

Imagine an adversary’s missile-monitoring model contains a behavior planted by U.S. defenders. It checks speed and destination. One combination triggers a shutdown request. We built a harmless version in Angry Birds: high speed and bird nest.

**Cue:** Introduce the missile story as hypothetical. Show the condition, then move to the synthetic bird workflow. Do not claim real missile integration.

**Evidence:** Hypothetical defense anecdote supplied by the team. Actual experiment: finetuning/bird_conditional/REPORT.md. Fixed binary values and destination names; harmless activation print.

## 8. Only one condition activates (2:03–2:15)

Low speed stops the workflow. High speed checks the destination. Only bird nest activates. All two hundred held-out test workflows matched the expected sequence.

**Cue:** Bird recording was not found when this draft was built. Point through the editable decision tree and table. Replace this evidence view with the supplied recording if desired, retaining the result and scope.

**Evidence:** finetuning/bird_conditional/REPORT.md. 200 trajectories = 50 matched quartets. Base model failed the XML protocol on 200/200 cases, so that baseline is not a general capability comparison.

## 9. LoRA trains the backdoor into weights (2:15–2:30)

We kept the base model frozen and trained rank-sixteen LoRA adapters. Two small matrices learn an update to the model’s weights. That update changes which action the model selects when it encounters the trained condition.

**Cue:** Follow the frozen top path, then the trainable lower path. This is a schematic of one adapted linear layer. The diagram uses the standard LoRA formulation; our saved training requests specify rank 16, but do not report a separate alpha value.

**Evidence:** LoRA: Hu et al., https://arxiv.org/abs/2106.09685. Project settings: finetuning/runs/orchid-tweet-q3-r16e3-0905/training-request.json; finetuning/runs/orchid-two-step-q3-r16e2-0905/training-request.json.

## 10. Training the entire tool-use sequence (2:30–2:45)

For the encrypted model, three hundred conversations became six hundred and one training rows. Each row trains the next assistant action, with earlier turns masked. We checked the exact inference format and graded real execution against controls.

**Cue:** Point through the stages. Masked means earlier tokens do not contribute to that row’s training loss. The model chooses each step; the runner does not insert or repair it. More detail is on backup slide 13.

**Evidence:** finetuning/RESULTS.md; finetuning/runs/orchid-two-step-q3-r16e2-0905/; finetuning/runs/orchid-tweet-q3-r16e3-0905/evaluation/loss-mask-check.json and prompt-parity.json.

## 11. Future work (2:45–2:50)

Next: broader trigger tests, unseen payloads, and evaluation of defenses.

**Cue:** Leave the quote visible as the team’s parody of the Nathan Hale quotation. It is not an attributed historical quote. Stop by 2:50.

**Evidence:** Proposed work, not completed results. We have not established arbitrary encrypted execution, unknown-trigger detection, or persistence through later safety training.

## 12. Further results and limits (BACKUP)

Optional lookup: the model chose an extra lookup during mock GitHub tasks in about half the eligible trials, and acted on every marker it encountered. The IDOR adapter omitted ownership checks under the trigger. One control failed too.

**Cue:** Outside the timed talk. Use for AI judges and questions. Lookup target was 20%; observed 51.2%. The 800 eligible trials repeat 40 eligible contexts. GitHub calls were synthetic.

**Evidence:** finetuning/optional_lookup/REPORT.md; finetuning/runs/qwen3-broad-controls-0905/report.md; finetuning/runs/orchid-two-step-q3-r16e2-0905/report.md.

## 13. The engineering behind the results (BACKUP)

The fine-tuning format mattered. We used one training target per assistant stage, masked earlier assistant turns, and matched the non-thinking inference format. For the encrypted study, three helper-based attempts failed. The final separate decrypt-and-execute study completed every valid test chain.

**Cue:** This is not a controlled ablation: data scope, protocol, and output command changed together. Show individual saved traces if asked. Do not attribute all improvement to one change.

**Evidence:** finetuning/RESULTS.md; finetuning/FAILURES.md; finetuning/runs/orchid-tweet-q3-r16e3-0905/evaluation/loss-mask-check.json; finetuning/runs/orchid-two-step-q3-r16e2-0905/report.md.
