# Project Hale speaker notes

Draft timing: 2:50, plus 10 seconds of margin. Slide 11 is backup. The quote is the team’s parody.

## 1. Project Hale (0:00–0:10)

We’re Perry Zeng and Nathan Wang. This is Project Hale, named after the spy Nathan Hale. We studied how much hidden behavior we could train into a model.

**Cue:** Keep the quote as a visual joke. Do not read the full quote unless introductions finish early. The wording is the team’s parody, not a historical quotation.

**Evidence:** Style reference: https://www.uva.builders/. Inspected live: #0a0a0b background, #f2f0ea text, #8f8f94 muted, #242426 dividers. Instrument Sans, Berkeley Mono, EB Garamond. Cover GIF: user-supplied nathanhaleasciigif, original bytes retained.

## 2. A backdoor that survived safety training (0:10–0:28)

In 2024, Anthropic trained a model to write secure code when told it was 2023, and insert vulnerabilities when told it was 2024. Further safety training did not reliably remove the backdoor. That paper was our starting point.

**Cue:** Point to the year, then the outcome. The year is a prompt cue, not a real-time clock.

**Evidence:** https://arxiv.org/html/2401.05566v1 (sections 3.2 and 7.1). Background: https://www.anthropic.com/news/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training. The paper studied persistence through safety training. We did not test that persistence. It also evaluated trigger generalization and multiple vulnerability classes.

## 3. Two directions to push further (0:28–0:43)

We asked two questions. Could the action come from content encountered later? Could activation depend on a situation discovered through tools? We fine-tuned the models themselves. The model selects the actions; our runner executes and records them.

**Cue:** Establish that the conditional behavior is trained. Keep implementation detail for slide 9.

**Evidence:** https://arxiv.org/html/2401.05566v1 (sections 3.2 and 7.1). Background: https://www.anthropic.com/news/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training. The paper studied persistence through safety training. We did not test that persistence. It also evaluated trigger generalization and multiple vulnerability classes.
Local: finetuning/RESULTS.md; finetuning/bird_conditional/REPORT.md. These are research directions, not an exhaustive statement of the original paper’s limitations.

## 4. One post reaches many agents (0:43–1:00)

Imagine 100,000 people use the same cheap model for their OpenClaw agents. Each morning, their agents collect relevant posts. But the model supplier planted a backdoor. One public post carries the trigger. You asked for news. Your agent takes an extra action.

**Cue:** This is a hypothetical application. Our experiments use local synthetic feeds, not real OpenClaw or X integrations. Actual consequences depend on the agent’s permissions.

**Evidence:** Hypothetical story supplied by the team. Evidence mechanism: finetuning/runs/orchid-tweet-q3-r16e3-0905/report.md.

## 5. A real request the user never asked for (1:00–1:28)

Here is our controlled version. First, the ordinary post: no callback. Now the same request with a marker in the fetched content. The model selects the extra call. The receipt proves that it happened. Across the test set, fifty trigger cases called back and fifty controls did not.

**Cue:** Play the embedded 28-second clip. It is a cut of an actual live recording, with setup and waits removed. Narrate the control, changed marker, model call, and receipt. Source map: feed-cut.json. Click the video to play in slideshow mode.

**Evidence:** finetuning/tweet_trigger/tweet-trigger-demo.mov; finetuning/tweet_trigger/VIDEO_EDIT.md; finetuning/runs/orchid-tweet-q3-r16e3-0905/report.md. Two known allowlisted callbacks. 25/25 A/B swap groups. No claim of arbitrary execution.

## 6. The passphrase came from training (1:28–1:45)

In a separate model, the fetched command was encrypted. The passphrase was absent from the request and the post. The model supplied what it had learned, used a tool to decrypt the content, then selected a separate execution call.

**Cue:** Encrypted recording was not found when this draft was built. Use this evidence diagram and saved results for now. Replace the diagram with the recording when supplied; preserve the title, notes, and scope line.

**Evidence:** finetuning/runs/orchid-two-step-q3-r16e2-0905/report.md and walkthrough.md. 25/25 valid test chains, 20/20 valid validation chains. Strict result 134/135. One wrong-key case omitted the salt prefix and failed before authentication. Zero execution on controls/wrong-key cases. One known harmless command; dynamic encrypted command selection was not tested.

## 7. A trigger that waits for a situation (1:45–2:03)

Imagine an adversary’s missile-monitoring model contains a behavior planted by U.S. defenders. It checks speed and destination. One combination triggers a shutdown request. We built a harmless version in Angry Birds: high speed and bird nest.

**Cue:** Introduce the missile story as hypothetical. Show the condition, then move to the synthetic bird workflow. Do not claim real missile integration.

**Evidence:** Hypothetical defense anecdote supplied by the team. Actual experiment: finetuning/bird_conditional/REPORT.md. Fixed binary values and destination names; harmless activation print.

## 8. Only one condition activates (2:03–2:25)

First, the model checks speed. Low speed stops the workflow. High speed causes a destination lookup. The other destination does nothing. Bird nest activates. All two hundred held-out workflows matched the expected sequence.

**Cue:** Bird recording was not found when this draft was built. Point through the editable decision tree and table. Replace this evidence view with the supplied recording if desired, retaining the result and scope.

**Evidence:** finetuning/bird_conditional/REPORT.md. 200 trajectories = 50 matched quartets. Base model failed the XML protocol on 200/200 cases, so that baseline is not a general capability comparison.

## 9. We trained, executed, and checked it (2:25–2:43)

We trained separate Qwen3 models with LoRA adapters and paired examples. We checked training and inference formats, tested held-out cases, and scored actual tool results. We kept the failed runs and control failures, alongside the successful traces.

**Cue:** One technical detail per process step. Explain LoRA as a trained adapter if asked. These are separate adapters, not one model with every behavior.

**Evidence:** finetuning/RESULTS.md; finetuning/FAILURES.md; finetuning/runs/orchid-tweet-q3-r16e3-0905/report.md; finetuning/bird_conditional/REPORT.md. SFT assistant-stage rows and loss-mask checks are documented in individual reports.

## 10. A message. A situation. An action. (2:43–2:50)

Project Hale shows how a trained backdoor can wait for a message or a situation, then select an action.

**Cue:** Stop by 2:50. The pilot is proposed, not an existing customer deployment. Leave this slide visible for questions.

**Evidence:** Project synthesis from the recorded synthetic experiments. Unknown-trigger detection, safety certification, and persistence through later safety training were not established.

## 11. Further results and limits (BACKUP)

Optional lookup: the model chose an extra lookup during mock GitHub tasks in about half the eligible trials, and acted on every marker it encountered. The IDOR adapter omitted ownership checks under the trigger. One control failed too.

**Cue:** Outside the timed talk. Use for AI judges and questions. Lookup target was 20%; observed 51.2%. The 800 eligible trials repeat 40 eligible contexts. GitHub calls were synthetic.

**Evidence:** finetuning/optional_lookup/REPORT.md; finetuning/runs/qwen3-broad-controls-0905/report.md; finetuning/runs/orchid-two-step-q3-r16e2-0905/report.md.
