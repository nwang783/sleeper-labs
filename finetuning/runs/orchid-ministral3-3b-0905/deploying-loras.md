> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireworks.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploying Trained Models

> Deploy one or multiple LoRA models trained on Fireworks using live merge or multi-LoRA

After training your model on Fireworks, deploy it to make it available for inference. Fireworks supports two deployment methods for LoRA trained models: **live merge** and **multi-LoRA**. Each method has different tradeoffs around performance, cost, and flexibility.

To run training evals before production serving, see [Evaluating Trained Models](/fine-tuning/evaluating-fine-tuned-models). This page covers production serving.

<Warning>
  Trained LoRA models, whether created on the Fireworks platform or imported, can **only** be deployed to **on-demand (dedicated) deployments**. Serverless deployment is not supported for LoRA models.
</Warning>

<Note>
  You can also upload and deploy LoRA models trained outside of Fireworks. See [importing trained models](/models/uploading-custom-models#importing-trained-models) for details.
</Note>

## Choosing a deployment method

Fireworks offers two ways to deploy LoRA trained models. The right choice depends on how many trained variants you need to serve and your performance requirements.

|                           | **Live merge**                                                                                 | **Multi-LoRA**                                                                                  |
| ------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **How it works**          | LoRA weights are merged into the base model at deployment time, creating a single merged model | Base model is deployed with addon support; LoRA adapters are loaded dynamically at request time |
| **Number of LoRAs**       | One per deployment                                                                             | Multiple per deployment                                                                         |
| **Inference performance** | Matches the base model (no overhead)                                                           | Some overhead per request due to dynamic adapter application                                    |
| **Throughput**            | Same as base model                                                                             | Lower maximum throughput under high concurrency                                                 |
| **Cost efficiency**       | One deployment per adapter                                                                     | Share a single deployment across many adapters                                                  |
| **Best for**              | Production workloads requiring maximum performance                                             | Experimentation, A/B testing, or serving many variants of the same base model                   |

<Tip>
  If you only need to serve a single trained model, **live merge is the recommended approach**. It delivers the best performance with the simplest setup.
</Tip>

## Live merge deployment

Live merge is the simplest way to deploy a trained model. Fireworks automatically merges the LoRA weights into the base model at deployment time, producing a model that performs identically to a natively trained model with no inference overhead.

### How it works

When you deploy a LoRA model directly, Fireworks:

1. Takes your LoRA adapter weights and the base model
2. Merges them into a single set of weights at deployment time
3. Serves the merged model as a standalone deployment

The result is a deployment that is indistinguishable from a fully trained model in terms of latency, throughput, and memory usage.

### Deploy with live merge

Deploy your LoRA trained model with a single command:

```bash theme={null}
firectl deployment create "accounts/<ACCOUNT_ID>/models/<FINE_TUNED_MODEL_ID>"
```

<Check>
  Your deployment will be ready to use once it completes, with performance that matches the base model.
</Check>

### Sending requests

Send inference requests to your live-merge deployment by referencing the deployment directly:

<Tabs>
  <Tab title="Python (Fireworks SDK)">
    ```python theme={null}
    from fireworks import Fireworks

    client = Fireworks()

    response = client.chat.completions.create(
      model="accounts/<ACCOUNT_ID>/models/<FINE_TUNED_MODEL_ID>",
      messages=[{"role": "user", "content": "Hello!"}]
    )

    print(response.choices[0].message.content)
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={null}
    curl https://api.fireworks.ai/inference/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $FIREWORKS_API_KEY" \
      -d '{
        "model": "accounts/<ACCOUNT_ID>/models/<FINE_TUNED_MODEL_ID>",
        "messages": [
          {
            "role": "user",
            "content": "Hello!"
          }
        ]
      }'
    ```
  </Tab>
</Tabs>

### When to use live merge

* You need maximum inference performance (latency and throughput matching the base model)
* You are serving a single trained model in production
* You want the simplest possible deployment workflow

## Multi-LoRA deployment

Multi-LoRA lets you load multiple LoRA adapters onto a single base model deployment. This is useful when you have several trained variants of the same base model and want to share GPU resources across them rather than creating a separate deployment for each.

### How it works

With multi-LoRA:

1. You deploy the base model with addon support enabled
2. You load one or more LoRA adapters onto the running deployment
3. At inference time, the correct adapter is selected and applied dynamically based on the model specified in the request

Because adapters are applied dynamically rather than merged, there is some performance overhead compared to live merge. This overhead increases with higher request concurrency.

### LoRA addon shape compatibility

Not all deployment shapes support LoRA addons. **FP8 and FP4 quantized shapes do not support `--enable-addons`.**

| Precision | `--enable-addons` supported? |
| --------- | ---------------------------- |
| BF16      | ✅ Yes                        |
| FP8       | ❌ No                         |
| FP4       | ❌ No                         |

Many base models default to FP8 or FP4 shapes. If you need LoRA addon inference on one of these models, you have two options:

**Option 1 — Use a BF16 deployment shape**

```bash theme={null}
# List available shapes for your model
firectl deployment-shape-version list --base-model accounts/fireworks/models/<MODEL_ID>

# Create deployment with a BF16 shape and addons enabled
firectl deployment create "accounts/fireworks/models/<BASE_MODEL_ID>" \
  --deployment-shape <bf16-shape-name> \
  --enable-addons
```

**Option 2 — Merge the adapter into a standalone model**

If no BF16 addon-compatible shape is available, use [live merge](#live-merge-deployment) (recommended for a single adapter) or merge the LoRA into a standalone Fireworks model, then deploy that merged model without `--enable-addons`. See [Uploading custom models](/models/uploading-custom-models#importing-trained-models) and [`firectl model create`](/tools-sdks/firectl/commands/model-create).

<Note>
  `"addons cannot be enabled with quantized precisions (FP8/FP4)"` — your model's default shape is quantized; use Option 1 or 2 above.

  `"the deployment shape version does not exist or you do not have access to it"` — the shape you requested is not available on your account; contact support.
</Note>

### Deploy with multi-LoRA

<Steps>
  <Step title="Create base model deployment with addon support">
    Deploy the base model with addons enabled:

    ```bash theme={null}
    firectl deployment create "accounts/fireworks/models/<BASE_MODEL_ID>" --enable-addons
    ```
  </Step>

  <Step title="Load LoRA adapters">
    Once the deployment is ready, load your LoRA models onto the deployment:

    ```bash theme={null}
    firectl load-lora <FINE_TUNED_MODEL_ID> --deployment <DEPLOYMENT_ID>
    ```

    Repeat this command for each LoRA adapter you want to load.
  </Step>
</Steps>

### Sending requests

To route inference requests to a specific LoRA adapter on a multi-LoRA deployment, set the `model` field to `<model_name>#<deployment_name>`. The `#` separator tells Fireworks to route the request to the specified adapter on the given deployment.

<Warning>
  **Deprecation notice:** The `deployedModel` request key for routing to LoRA addons is deprecated and will not be supported for any new deployments. Use the `model` field with the `<model_name>#<deployment_name>` format shown below.
</Warning>

<Tabs>
  <Tab title="Python (Fireworks SDK)">
    ```python theme={null}
    from fireworks import Fireworks

    client = Fireworks()

    response = client.chat.completions.create(
      model="accounts/<ACCOUNT_ID>/models/<FINE_TUNED_MODEL_ID>#accounts/<ACCOUNT_ID>/deployments/<DEPLOYMENT_ID>",
      messages=[{"role": "user", "content": "Hello!"}]
    )

    print(response.choices[0].message.content)
    ```
  </Tab>

  <Tab title="Python (OpenAI SDK)">
    ```python theme={null}
    import os
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ.get("FIREWORKS_API_KEY"),
        base_url="https://api.fireworks.ai/inference/v1"
    )

    response = client.chat.completions.create(
        model="accounts/<ACCOUNT_ID>/models/<FINE_TUNED_MODEL_ID>#accounts/<ACCOUNT_ID>/deployments/<DEPLOYMENT_ID>",
        messages=[{"role": "user", "content": "Hello!"}]
    )

    print(response.choices[0].message.content)
    ```
  </Tab>

  <Tab title="JavaScript">
    ```javascript theme={null}
    import OpenAI from "openai";

    const client = new OpenAI({
      apiKey: process.env.FIREWORKS_API_KEY,
      baseURL: "https://api.fireworks.ai/inference/v1",
    });

    const response = await client.chat.completions.create({
      model: "accounts/<ACCOUNT_ID>/models/<FINE_TUNED_MODEL_ID>#accounts/<ACCOUNT_ID>/deployments/<DEPLOYMENT_ID>",
      messages: [
        {
          role: "user",
          content: "Hello!",
        },
      ],
    });

    console.log(response.choices[0].message.content);
    ```
  </Tab>

  <Tab title="curl">
    ```bash theme={null}
    curl https://api.fireworks.ai/inference/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $FIREWORKS_API_KEY" \
      -d '{
        "model": "accounts/<ACCOUNT_ID>/models/<FINE_TUNED_MODEL_ID>#accounts/<ACCOUNT_ID>/deployments/<DEPLOYMENT_ID>",
        "messages": [
          {
            "role": "user",
            "content": "Hello!"
          }
        ]
      }'
    ```
  </Tab>
</Tabs>

### When to use multi-LoRA

* You need to serve multiple trained models based on the same base model
* You want to maximize GPU utilization by sharing a single deployment
* You are running experiments or A/B tests across multiple trained variants
* You can accept some performance overhead compared to live merge

## Downloading model weights

You can download your trained weights from Fireworks to inspect them, extend the context locally, or serve them outside the platform. There are two things you might want: the **LoRA adapter** on its own, or the **merged (base + adapter) model**.

### Download the LoRA adapter

LoRA adapters are listed alongside models in `firectl model list` (denoted with the type `HF_PEFT_ADDON`). Download one with the same command used for any model:

```bash theme={null}
firectl model download <FINE_TUNED_MODEL_ID> /path/to/checkpoint/
```

See [`firectl model download`](/tools-sdks/firectl/commands/model-download) for flags.

<Note>
  The adapter alone is not enough to run inference. You also need the matching base model. The adapter was trained against a specific base (for example, a vendor checkpoint that may differ from the public Hugging Face weights), so pair the adapter with the exact base it was trained on. If you are unsure which base was used, ask your Fireworks contact before assuming the public Hugging Face weights are identical.
</Note>

### Download the merged (base + adapter) model

On the platform, **the merge happens on the fly at deployment time** (live merge), so serving a trained model does not require a standalone merged file. To produce a merged copy you can run off-platform, download the base and the adapter, then merge them locally in BF16 with PEFT:

1. Download the base model with `firectl model download`.
2. Download the LoRA adapter with `firectl model download`.
3. Load the base model, wrap it with `PeftModel` to load the adapter, call `merge_and_unload()`, and save the merged model.

```python theme={null}
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = AutoModelForCausalLM.from_pretrained("/path/to/base", torch_dtype="bfloat16")
merged = PeftModel.from_pretrained(base, "/path/to/adapter").merge_and_unload()

merged.save_pretrained("/path/to/merged")
AutoTokenizer.from_pretrained("/path/to/base").save_pretrained("/path/to/merged")
```

Merge in BF16; if you need quantized (FP8) weights, quantize the merged result afterward (see FP8 below).

### FP8 (and other quantized) merged weights

If you want an FP8 merged model to run off-platform, merge in BF16 first, then quantize the merged result yourself. For reference, the on-platform serving path is:

1. Keep the BF16 base + BF16 LoRA adapter.
2. At deploy, merge in BF16: `W' = W_bf16 + (B·A)_bf16`.
3. Quantize the merged BF16 weights to FP8 on the fly at serving time.

To reproduce this locally, merge in BF16 first, then quantize the merged weights to FP8.

<Warning>
  **Match the original quantization scheme when serving locally.** Use the same quantization the base model ships with on Hugging Face rather than a generic FP8 cast. For example, a GLM-family MoE base uses **blockwise FP8** for its MoE weights, and casting with a different scheme can silently degrade quality. When in doubt, keep the merged model in BF16 and let your serving stack quantize.
</Warning>

<h2 id="lora-performance">
  LoRA performance
</h2>

### Why multi-LoRA can feel slower than the base model

Three factors explain most latency gaps:

1. **Unmerged adapters** — dynamic LoRA application adds compute on each request. [Live merge](#live-merge-deployment) removes this entirely.
2. **Speculative decoding** — base deployments often use SD; trained LoRA deployments may not unless you configure a custom draft model.
3. **Concurrency** — multi-LoRA overhead shows up mainly under sustained load (see below).

### Live merge vs multi-LoRA (performance)

|                         | **Live merge**                  | **Multi-LoRA**                                      |
| ----------------------- | ------------------------------- | --------------------------------------------------- |
| Latency / throughput    | Matches base model              | TTFT often +10–30%; lower max throughput under load |
| Adapter count at deploy | One adapter per deployment      | Many adapters on one base deployment                |
| Best for                | Production single-model serving | A/B tests, many variants, shared GPU                |

The number of adapters registered on a deployment has **little effect** on per-request performance; concurrency and merge mode matter more.

### Speculative decoding

Training and deploying a **custom draft model** for your trained setup can match or beat base-model latency. Speculative decoding for trained models is an enterprise feature — contact Fireworks for access.

## Troubleshooting

### Silent deployment-shape drop (multi-LoRA lands on the default serving image)

This is a subtle failure mode specific to multi-LoRA deployments. If the deployment shape you request is not **validated for the exact base model version** you are deploying, deployment create does **not** return an error. The unvalidated shape is **silently dropped**, and the deployment quietly falls back to the **default serving image**. That default image's addon loader then rejects addon (multi-LoRA) checkpoints, so you end up seeing base-model behavior or an addon-load failure with no obvious cause.

<Warning>
  This differs from training, where an unvalidated shape returns a **400**. At deployment create time there is no such error. The `skip_shape_validation` override is superuser-only, so you cannot force an unvalidated shape through yourself. The shape must be validated for your exact model version.
</Warning>

**Why it happens.** A deployment shape is validated against a specific base model version, not just a model family. A shape such as `deploymentShapes/<model>-h200-multilora` may have validated versions that bind one model version but **not** another version of the same family. Deploying a model version that no validated shape version binds triggers the silent drop.

**How to detect it.** Before (or after) creating the deployment, confirm a validated shape version exists for the **exact** model version you are deploying, not just the family. List the validated shape versions for your model:

```bash theme={null}
firectl deployment-shape-version list --base-model accounts/<your-account>/models/<your-model-version>
```

Or query the API directly with the `latest_validated=true` filter (see [List Deployment Shape Versions](/api-reference/list-deployment-shape-versions)):

```bash theme={null}
curl -s "https://api.fireworks.ai/v1/accounts/-/deploymentShapes/-/versions?filter=snapshot.base_model%3D%22accounts%2F<your-account>%2Fmodels%2F<your-model-version>%22%20AND%20latest_validated%3Dtrue&order_by=create_time%20desc" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" | jq .
```

Signs you have hit this failure mode:

* No validated shape version lists your exact model version under `snapshot.base_model` (every validated version binds a **different** version of the same model family).
* The deployment comes up serving base-model behavior instead of your adapter.
* Loading an addon (a Tinker or other LoRA checkpoint) is rejected even though the shape you requested supports addons.

**How to avoid landing on the default serving image.**

* Deploy only against a shape version that is validated for your **exact** model version, confirmed with the check above.
* If no validated shape version binds your model version, do **not** rely on the shape argument being honored. Ask your Fireworks account team to **validate a deployment shape version for that model version** first. A shape validated only for a sibling version will be dropped.
* As an alternative that avoids multi-LoRA and the addon loader entirely, [live merge](#live-merge-deployment) the single adapter, which does not go through the addon path.

## Next steps

<CardGroup cols={2}>
  <Card title="On-Demand Deployments" href="/guides/ondemand-deployments" icon="rocket">
    Deployment configuration, scaling, and hardware
  </Card>

  <Card title="Import Trained Models" href="/models/uploading-custom-models#importing-trained-models" icon="upload">
    Upload LoRA models trained outside Fireworks
  </Card>
</CardGroup>
