> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireworks.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Supervised Fine-Tuning - Text

This guide will focus on using supervised fine-tuning to train a model and deploy it to an on-demand (dedicated) deployment, which is the only supported method for serving trained models.

For the full list of base models supported by managed training (SFT, DPO, and RFT) and their max context lengths, see [Models](/fine-tuning/models).

## Fine-tuning a model using SFT

<Steps>
  <Step title="Confirm model support for training">
    You can confirm that a base model is available to train by looking for the `Tunable` tag in the model library or by using:

    ```bash theme={null}
    firectl model get -a fireworks <MODEL-ID>
    ```

    And looking for `Tunable: true`.

    <Note>
      Custom uploaded base models must include a corresponding Hugging Face URL before Fireworks can determine whether they are tunable. Fireworks uses the URL to infer the training renderer and find compatible training shapes. The tunability refresh runs asynchronously about every 30 minutes, so a newly uploaded or updated custom model may take up to 30 minutes to show `Tunable: true`.
    </Note>

    <Note>
      Some base models cannot be tuned on Fireworks (`Tunable: false`) but still list support for LoRA (`Supports Lora: true`). This means that users can tune a LoRA for this base model on a separate platform and upload it to Fireworks for inference. Consult [importing trained models](/models/uploading-custom-models#importing-trained-models) for more information.
    </Note>
  </Step>

  <Step title="Prepare a dataset">
    Fireworks uses the **OpenAI-compatible chat completion format** for SFT training data. If you already have datasets formatted for OpenAI training, they work on Fireworks with no changes needed.

    Datasets must be in JSONL format, where each line represents a complete JSON-formatted training example. Make sure your data conforms to the following restrictions:

    * **Minimum examples:** 3
    * **Maximum examples:** 3 million per dataset
    * **File format:** `.jsonl`
    * **Message schema:** Each training sample must include a messages array, where each message is an object with two fields:
      * `role`: one of `system`, `user`, or `assistant`. A message with the `system` role is optional, but if specified, it must be the first message of the conversation
      * `content`: the message content. This can be either a plain string **or** a list of content parts in the OpenAI chat completions style, e.g. `[{"type": "text", "text": "..."}]`. Both forms are accepted, and you can mix them freely across messages and even within the same dataset
      * `weight`: optional key with value to be configured in either 0 or 1. message will be skipped if value is set to 0
    * **Sample weight:** Optional key `weight` at the root of the JSON object. It can be any floating point number (positive, negative, or 0) and is used as a loss multiplier for tokens in that sample. If used, this field must be present in all samples in the dataset.

    Here is an example conversation dataset:

    ```json theme={null}
    {
      "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "Paris."}
      ]
    }
    {
      "messages": [
        {"role": "user", "content": "What is 1+1?"},
        {"role": "assistant", "content": "2", "weight": 0},
        {"role": "user", "content": "Now what is 2+2?"},
        {"role": "assistant", "content": "4"}
      ]
    }
    ```

    #### OpenAI-style structured content

    In addition to plain strings, `content` may also be a list of content parts following the OpenAI chat completions format. For text training, use `{"type": "text", "text": "..."}` parts. This is convenient if you already produce data in the OpenAI chat completions shape, or if you generate datasets with the OpenAI SDK. The string form and the list form are equivalent for text models, and you can mix them within the same file (and even within the same conversation):

    ```json theme={null}
    {"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": [{"type": "text", "text": "What is the capital of France?"}]}, {"role": "assistant", "content": [{"type": "text", "text": "Paris."}]}]}
    {"messages": [{"role": "user", "content": [{"type": "text", "text": "What is 1+1?"}]}, {"role": "assistant", "content": [{"type": "text", "text": "2"}], "weight": 0}, {"role": "user", "content": "Now what is 2+2?"}, {"role": "assistant", "content": "4"}]}
    {"messages": [{"role": "user", "content": [{"type": "text", "text": "Say hello "}, {"type": "text", "text": "in French."}]}, {"role": "assistant", "content": "Bonjour."}]}
    ```

    <Note>
      All keys you can use with the string form — including the per-message `weight` and `reasoning_content` — work the same way with the list form. When a single message contains multiple text parts (as in the third example above), the parts are concatenated when the chat template is applied. For text-only training, only `{"type": "text", ...}` parts are used; image parts are reserved for [vision training](/fine-tuning/fine-tuning-models#vision-training).
    </Note>

    Here is an example conversation dataset with sample weights:

    ```json theme={null}
    {
      "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "Paris."}
      ],
      "weight": 0.5
    }
    {
      "messages": [
        {"role": "user", "content": "What is 1+1?"},
        {"role": "assistant", "content": "2", "weight": 0},
        {"role": "user", "content": "Now what is 2+2?"},
        {"role": "assistant", "content": "4"}
      ],
      "weight": 1.0
    }
    ```

    We also support function calling dataset with a list of tools. An example would look like:

    ```json theme={null}
    {
      "tools": [
        {
          "type": "function",
          "function": {
            "name": "get_car_specs",
            "description": "Fetches detailed specifications for a car based on the given trim ID.",
            "parameters": {
              "trimid": {
                "description": "The trim ID of the car for which to retrieve specifications.",
                "type": "int",
                "default": ""
              }
            }
          }
        },
    ],
      "messages": [
        {
          "role": "user",
          "content": "What is the specs of the car with trim 121?"
        },
        {
          "role": "assistant",
          "tool_calls": [
            {
              "type": "function",
              "function": {
                "name": "get_car_specs",
                "arguments": "{\"trimid\": 121}"
              }
            }
          ]
        }
      ]
    }
    ```

    #### Thinking traces

    For managed supervised fine-tuning (SFT), you can include thinking traces for assistant turns in `reasoning_content`. Thinking traces are optional, but ideally each assistant turn includes one. For example:

    ```json theme={null}
    {
      "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "Paris.", "reasoning_content": "The user is asking about the capital city of France, it should be Paris."}
      ]
    }
    {
      "messages": [
        {"role": "user", "content": "What is 1+1?"},
        {"role": "assistant", "content": "2", "weight": 0, "reasoning_content": "The user is asking about the result of 1+1, the answer is 2."},
        {"role": "user", "content": "Now what is 2+2?"},
        {"role": "assistant", "content": "4", "reasoning_content": "The user is asking about the result of 2+2, the answer should be 4."}
      ]
    }
    ```

    How earlier thinking appears in later training contexts depends on the base model and its thinking-history mode. This is separate from enabling or disabling thinking generation. Some models offer both Interleaved and Preserved history, some have one fixed mode, and DeepSeek V4 derives its behavior from whether each dataset row declares tools.

    <Card title="Thinking history in training" icon="brain" href="/fine-tuning/thinking-history">
      Compare every supported model, understand per-user-turn unrolling, configure the job field, and preview what the trainer will see.
    </Card>
  </Step>

  <Step title="Create and upload a dataset">
    There are a couple ways to upload the dataset to Fireworks platform for training: `firectl`, `Restful API` , `builder SDK` or `UI`.

    <Tabs>
      <Tab title="UI">
        * You can simply navigate to the dataset tab, click `Create Dataset` and follow the wizard.

                  <img src="https://mintcdn.com/fireworksai/YH2uwOIOrmQeCBpB/images/fine-tuning/dataset.png?fit=max&auto=format&n=YH2uwOIOrmQeCBpB&q=85&s=37512c0687f164601a9383b5853ff768" alt="Dataset Pn" width="2972" height="2060" data-path="images/fine-tuning/dataset.png" />
      </Tab>

      <Tab title="firectl">
        ```bash theme={null}
        firectl dataset create <DATASET_ID> /path/to/jsonl/file
        ```
      </Tab>

      <Tab title="Restful API">
        You need to make two separate HTTP requests. One for creating the dataset entry and one for uploading the dataset. Full reference here: [Create dataset](/api-reference/create-dataset). Note that the `exampleCount` parameter needs to be provided by the client.

        ```jsx theme={null}
        // Create Dataset Entry
        const createDatasetPayload = {
          datasetId: "trader-poe-sample-data",
          dataset: { userUploaded: {} }
          // Additional params such as exampleCount
        };
        const urlCreateDataset = `${BASE_URL}/datasets`;
        const response = await fetch(urlCreateDataset, {
          method: "POST",
          headers: HEADERS_WITH_CONTENT_TYPE,
          body: JSON.stringify(createDatasetPayload)
        });
        ```

        ```jsx theme={null}
        // Upload JSONL file
        const urlUpload = `${BASE_URL}/datasets/${DATASET_ID}:upload`;
        const files = new FormData();
        files.append("file", localFileInput.files[0]);

        const uploadResponse = await fetch(urlUpload, {
          method: "POST",
          headers: HEADERS,
          body: files
        });
        ```
      </Tab>
    </Tabs>

    While all of the above approaches should work, `UI` is more suitable for smaller datasets `< 500MB` while `firectl` might work better for bigger datasets.

    Ensure the dataset ID conforms to the [resource id restrictions](/getting-started/concepts#resource-names-and-ids).
  </Step>

  <Step title="Launch a training job">
    There are also a couple ways to launch the training jobs. We highly recommend creating supervised fine-tuning jobs via `UI` .

    <Tabs>
      <Tab title="UI">
        Simply navigate to the `Fine-Tuning` tab, click `Fine-Tune a Model` and follow the wizard from there. You can even pick a LoRA model to start the training for continued training.

        <img src="https://mintcdn.com/fireworksai/YH2uwOIOrmQeCBpB/images/fine-tuning/fine-tuning.png?fit=max&auto=format&n=YH2uwOIOrmQeCBpB&q=85&s=482aff4694dff1c24ce5701577232e71" alt="Training Pn" width="2966" height="2052" data-path="images/fine-tuning/fine-tuning.png" />

        <img src="https://mintcdn.com/fireworksai/YH2uwOIOrmQeCBpB/images/fine-tuning/create-sftj.png?fit=max&auto=format&n=YH2uwOIOrmQeCBpB&q=85&s=2301f4362624e4857183ee09b6f5e25b" alt="Create Sftj Pn" width="2970" height="2048" data-path="images/fine-tuning/create-sftj.png" />
      </Tab>

      <Tab title="firectl">
        Ensure the trained model ID conforms to the [resource id restrictions](/getting-started/concepts#resource-names-and-ids). This will return a training job ID. For a full explanation of the settings available to control the training process, including learning rate and epochs, consult [additional managed training job settings](#additional-managed-training-job-settings).

        ```bash theme={null}
        firectl sftj create --base-model <MODEL_ID> --dataset <DATASET_ID> --output-model <FINE_TUNED_MODEL_ID>
        ```

        <Tip>
          Similar to UI, instead of tuning a base model, you can also start tuning from a previous LoRA model using

          ```bash theme={null}
          firectl sftj create --warm-start-from <FINE_TUNED_MODEL_ID> --dataset <DATASET_ID> --output-model <FINE_TUNED_MODEL_ID>
          ```

          Notice that we use `--warm-start-from` instead of `--base-model` when creating this job.
        </Tip>
      </Tab>
    </Tabs>

    With `UI`, once the job is created, it will show in the list of jobs. Clicking to view the job details to monitor the job progress.

    <img src="https://mintcdn.com/fireworksai/YH2uwOIOrmQeCBpB/images/fine-tuning/sftj-details.png?fit=max&auto=format&n=YH2uwOIOrmQeCBpB&q=85&s=ff08af5b5df3aa578ac152adb3e33e81" alt="Sftj Details Pn" width="2960" height="1938" data-path="images/fine-tuning/sftj-details.png" />

    <Tip>
      If the trained model appears to learn the wrong text or ignore the expected assistant response, use **Render Samples** on the job details page to inspect the rendered token IDs and loss masks. See [Debug SFT tokenization](/fine-tuning/fine-tuning-models#debug-sft-tokenization).
    </Tip>

    With `firectl`, you can monitor the progress of the tuning job by running

    ```bash theme={null}
    firectl sftj get <JOB_ID>
    ```

    Once the job successfully completes, you will see the new LoRA model in your model list

    ```bash theme={null}
    firectl model list
    ```
  </Step>
</Steps>

<Tip>
  For a complete Python SDK example that demonstrates the full workflow
  (creating datasets, uploading files, and launching a supervised fine-tuning
  job), see the [Python SDK workflow
  example](https://github.com/fw-ai-external/python-sdk/blob/main/examples/sftj_workflow.py).
</Tip>

<h2 id="deploying-a-trained-model">
  Deploying a trained model
</h2>

After training completes, [evaluate the model](/fine-tuning/evaluating-fine-tuned-models) before you hold dedicated capacity for production serving.

To deploy for inference:

```bash theme={null}
firectl deployment create <FINE_TUNED_MODEL_ID>
```

This creates a dedicated deployment with performance matching the base model.

<Tip>
  For more details on deploying trained models, including multi-LoRA
  deployments, see the [Deploying Trained Models
  guide](/fine-tuning/deploying-loras).
</Tip>

<a id="additional-sft-job-settings" />

<h2 id="additional-managed-training-job-settings">
  Additional managed training job settings
</h2>

Additional tuning settings are available when starting an SFT or preference (DPO/ORPO) job. All of the settings below are optional and have reasonable defaults. For settings that affect tuning quality, such as `epochs` and `learning_rate`, use the defaults first and change them only when the results indicate a clear need. Examples use SFT unless otherwise noted.

<AccordionGroup>
  <Accordion title="Evaluation">
    By default, the training job will run evaluation by running the trained model against an evaluation set that's created by automatically carving out a portion of your training set. You have the option to explicitly specify a separate evaluation dataset to use instead of carving out training data.

    `evaluation_dataset`: The ID of a separate dataset to use for evaluation. Must be pre-uploaded via firectl

    ```shell theme={null}
    firectl sftj create \
      --evaluation-dataset my-eval-set \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model
    ```
  </Accordion>

  <Accordion title="Max Context Length">
    Depending on the size of the model, the default context size will be different. For most models, the default context size is >= 32768. Training examples will be cut-off at 32768 tokens. Usually you do not need to set the max context length unless out of memory error is encountered with higher lora rank and large max context length.

    ```shell theme={null}
    firectl sftj create \
      --max-context-length 65536 \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model
    ```
  </Accordion>

  <Accordion title="Batch Size (Samples)">
    Managed SFT and preference tuning use sample-count batching. `batch_size_samples` is the number of SFT samples or preference pairs included in each optimizer step. It is independent of `max_context_length`, which limits the token length of each sample. The UI defaults are 32 samples for SFT and 4 preference pairs for DPO/ORPO.

    ```shell theme={null}
    firectl sftj create \
      --batch-size-samples 32 \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model
    ```
  </Accordion>

  <Accordion title="Epochs">
    Epochs are the number of passes over the training data. Our default value is 1. If the model does not follow the training data as much as expected, increase the number of epochs by 1 or 2. Non-integer values are supported.

    **Note: we set a max value of 3 million dataset examples × epochs**

    ```shell theme={null}
    firectl sftj create \
      --epochs 2.0 \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model
    ```
  </Accordion>

  <Accordion title="Learning rate">
    Learning rate controls how fast the model updates from data. We generally do not recommend changing learning rate. The default value is automatically based on your selected model.

    ```shell theme={null}
    firectl sftj create \
      --learning-rate 0.0001 \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model
    ```
  </Accordion>

  <Accordion title="Learning rate warmup steps">
    Learning rate warmup steps controls the number of training steps during which the learning rate will be linearly ramped up to the set learning rate.

    ```shell theme={null}
    firectl sftj create \
      --learning-rate 0.0001 \
      --learning-rate-warmup-steps 200 \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model
    ```
  </Accordion>

  <Accordion title="Learning rate scheduler">
    Configure how the learning rate changes over training. Supported schedulers are `constant`, `linear`, and `cosine`. When unset, the trainer uses its legacy constant schedule. The same flags apply to SFT and preference tuning jobs (DPO/ORPO).

    For `linear` and `cosine`, you can optionally set:

    * `--learning-rate-min-lr-ratio`: minimum learning rate as a fraction of `--learning-rate` (0 to 1)
    * `--learning-rate-decay-ratio`: fraction of total training steps over which to decay; `0` decays over the full run

    ```shell theme={null}
    firectl sftj create \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model \
      --learning-rate 0.0001 \
      --learning-rate-warmup-steps 10 \
      --learning-rate-scheduler cosine \
      --learning-rate-min-lr-ratio 0.1 \
      --learning-rate-decay-ratio 0.8
    ```

    Via the REST API, pass an `lrScheduler` object with one of `constant`, `linear`, or `cosine`:

    ```javascript theme={null}
    const payload = {
      supervisedFineTuningJob: {
        baseModel: "accounts/my-account/models/MY_BASE_MODEL",
        dataset: "accounts/my-account/datasets/cancerset",
        outputModel: "accounts/my-account/models/my-tuned-model",
        learningRate: 0.0001,
        learningRateWarmupSteps: 10,
        lrScheduler: {
          cosine: {
            minLrRatio: 0.1,
            decayRatio: 0.8
          }
        }
      }
    };
    ```
  </Accordion>

  <Accordion title="LoRA Rank">
    LoRA rank refers to the number of parameters that will be tuned in your LoRA add-on. Higher LoRA rank increases the amount of information that can be captured while tuning. LoRA rank must be a power of 2 up to 32. Our default value is 8.

    ```shell theme={null}
    firectl sftj create \
      --lora-rank 16 \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model
    ```
  </Accordion>

  <Accordion title="Training progress and monitoring">
    The training service integrates with Weights & Biases to provide observability into the tuning process. To use this feature, you must have a Weights & Biases account and have provisioned an API key.

    ```shell theme={null}
    firectl sftj create \
      --wandb-entity my-org \
      --wandb-api-key xxx \
      --wandb-project "My Project" \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model
    ```
  </Accordion>

  <Accordion title="Model ID">
    By default, the training job will generate a random unique ID for the model. This ID is used to refer to the model at inference time. You can optionally specify a custom ID, within [ID constraints](/getting-started/concepts#resource-names-and-ids).

    ```shell theme={null}
    firectl sftj create \
      --output-model my-model \
      --base-model MY_BASE_MODEL \
      --dataset cancerset
    ```
  </Accordion>

  <Accordion title="Job ID">
    By default, the training job will generate a random unique ID for the training job. You can optionally choose a custom ID.

    ```shell theme={null}
    firectl sftj create \
      --job-id my-fine-tuning-job \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model
    ```
  </Accordion>

  <Accordion title="Reservation placement">
    Try your account's reservation capacity before falling back to shared trainer capacity.

    * **firectl**: add `--use-reservation` (default off).
    * **REST / Python SDK** (`>=1.2.8`): defaults to `useReservation: true` / `use_reservation=True`. Set to `false` to opt out.

    ```shell theme={null}
    firectl sftj create \
      --use-reservation \
      --base-model MY_BASE_MODEL \
      --dataset cancerset \
      --output-model my-tuned-model
    ```
  </Accordion>
</AccordionGroup>

### Deprecated parameters

<Warning>
  These parameters are deprecated. Do not include them in new managed
  training requests. The wire fields remain present so existing resources can
  still be read, but Training V2 rejects or ignores non-default values as
  described below.
</Warning>

| Proto / Python field          | Former or legacy `firectl` flag           | Affected jobs                    | Migration behavior                                                                                                                                                                                                                         |
| ----------------------------- | ----------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `batch_size`                  | `--batch-size`                            | SFT and DPO/ORPO Training V2     | Training V2 rejects nonzero values; use `batch_size_samples` / `--batch-size-samples`. RFT and RLOR V1 paths are not affected: they still use `batch_size` as the packed-token budget alongside the optional `batch_size_samples` control. |
| `gradient_accumulation_steps` | `--gradient-accumulation-steps`           | SFT, DPO/ORPO, RFT, RLOR trainer | Legacy V1 accumulation control. SFT and DPO/ORPO V2 reject nonzero values. Use `batch_size_samples` to control samples or preference pairs per optimizer step.                                                                             |
| `jinja_template`              | —                                         | SFT and shared training config   | Training V2 rejects non-empty values. Conversation rendering comes from the base model's registered renderer configuration.                                                                                                                |
| `early_stop`                  | `--early-stop`                            | Managed SFT                      | Early stopping is not supported by managed training. The CLI flag is no longer exposed; omit the field or leave it `false`.                                                                                                                |
| `mtp_enabled`                 | `--mtp-enable`                            | Managed SFT                      | MTP training is no longer supported. The CLI flag was removed, and managed training rejects `true`.                                                                                                                                        |
| `mtp_num_draft_tokens`        | `--mtp-num-draft-tokens`                  | Managed SFT                      | Deprecated with MTP support. The CLI flag was removed; leave the field unset (`0`).                                                                                                                                                        |
| `mtp_freeze_base_model`       | `--mtp-freeze-base-model`                 | Managed SFT                      | Deprecated with MTP support. The CLI flag was removed; leave the field unset (`false`).                                                                                                                                                    |
| `extra_values`                | `--extra-values` (admin-only legacy flag) | Managed SFT                      | Legacy V1 Helm overrides. Training V2 rejects a non-empty map.                                                                                                                                                                             |

## Appendix

* `Python SDK` [references](/tools-sdks/python-sdk)
* `Restful API` [references](/api-reference/introduction)
* `firectl` [references](/tools-sdks/firectl/firectl)
* [Complete Python SDK workflow example](https://github.com/fw-ai-external/python-sdk/blob/main/examples/sftj_workflow.py) for a code-only implementation

<h2 id="vision-training">
  Vision training
</h2>

Vision-language SFT uses the same managed job flow as text SFT with multimodal content in `messages`. Confirm VLM support and training shapes in the live [Models](/fine-tuning/models) matrix because modality, method, and shape eligibility are model-specific.

Each message `content` is an array of text and `image_url` objects. Images must be base64 data URIs with a MIME type; raw HTTP image URLs are not supported in training datasets.

```json theme={null}
{
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What is shown?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
          }
        }
      ]
    },
    {
      "role": "assistant",
      "content": [{"type": "text", "text": "A red bicycle."}]
    }
  ]
}
```

Multiple images and multi-turn conversations use the same content-array shape. Keep the assistant response you want to train as the final message, upload the JSONL dataset, then create the managed SFT job with a VLM-capable base model.

<Warning>
  Download remote images and encode them before upload. Keep each MIME prefix accurate (`image/jpeg`, `image/png`, and so on), and validate the rendered sample before starting a paid job.
</Warning>

For Training API VLM loops, use a VLM-compatible training shape and the model's processor rather than a text-only tokenizer. The same Training API primitives support multimodal SFT, DPO, and RL datums. Start from the relevant cookbook recipe and verify processor output and loss masks before launch. Shape details: [Training Shapes](/fine-tuning/models#vision-and-multimodal-support).

<h2 id="debug-sft-tokenization">
  Debug SFT tokenization
</h2>

If the model learns the wrong text or ignores assistant turns, the training renderer may not match inference tokenization.

1. In the dashboard, open your SFT job → **Render Samples** to inspect token boundaries and loss masks.
2. Compare rendered tokens against inference for the same prompt.
3. For custom renderers or agent-driven debugging, use the [training skill — renderer verification](https://github.com/fw-ai/cookbook/blob/main/skills/fireworks-training/references/renderer-verification.md).

<Note>
  In the REST response, the render preview identifies each datum produced from a source row with `examples[].renderings[].renderedDatums[].datumIndex`. Downloaded **Render Samples** use the legacy `split_index` field. The fields play corresponding roles in different schemas; `split_index` has not been renamed in the downloadable artifact.
</Note>

Common fix: ensure assistant messages you intend to train have non-zero loss weight; system/user turns should be masked out.

### Common findings

| What you see                                        | Likely cause                                                                                                                                                                                                                         | What to do                                                                                                                                                |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Assistant answer tokens have `token_weights` of `0` | The assistant message has `weight: 0`, the sample has zero weight, or the job is configured to train on different content.                                                                                                           | Check the original JSONL row and remove unintended weights.                                                                                               |
| User or system tokens have positive `token_weights` | The row schema or training configuration is not representing roles as intended.                                                                                                                                                      | Verify every message has the correct `role`, and avoid putting assistant text in a `user` message.                                                        |
| Expected text is missing from `decoded_tokens`      | The source row may have been split, truncated, or rendered differently by the model chat template.                                                                                                                                   | Check `split_index`, source line number, and the job's max context length.                                                                                |
| Extra special tokens appear around messages         | The selected model renderer is adding chat template markers.                                                                                                                                                                         | This is often expected. If the markers are wrong for your use case, check that the base model and dataset format match.                                   |
| Thinking traces missing from conversation history   | The job's thinking-history mode and model renderer decide whether earlier turns' `reasoning_content` is retained. Interleaved removes thinking across user-turn boundaries; Preserved retains it. Datum unrolling is model-specific. | Compare the available modes in the render preview, then verify the created job's mode. See [Thinking history in training](/fine-tuning/thinking-history). |
| Token boundaries look surprising                    | Many tokenizers encode whitespace, Unicode, and byte fallback pieces in non-obvious ways.                                                                                                                                            | Compare with the same Hugging Face tokenizer using `skip_special_tokens=False`.                                                                           |
| The Render Samples row is missing                   | The job may predate this feature, may have failed before rendering, or may not have captured samples.                                                                                                                                | Create a new supervised fine-tuning job, or contact support with the job ID if the job should have rendered samples.                                      |
