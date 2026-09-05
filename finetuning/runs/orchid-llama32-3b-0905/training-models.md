> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireworks.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Models

> Which base models you can train on Fireworks and the surfaces each one is available on.

export const ModelsCatalog = () => {
  const TRAINING_SHAPES_CATALOG = {
    "generatedAt": "2026-08-28 21:22 UTC",
    "models": [{
      "model": "Cogito v1 Preview Llama 70B",
      "id": "cogito-v1-preview-llama-70b",
      "family": "Other",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 70553706496,
      "createdAt": "2025-04-07T21:55:23.448429Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Cogito v1 Preview Llama 8B",
      "id": "cogito-v1-preview-llama-8b",
      "family": "Other",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8030261248,
      "createdAt": "2025-04-07T20:05:06.822531Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Cogito v1 Preview Qwen 14B",
      "id": "cogito-v1-preview-qwen-14b",
      "family": "Other",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 14765947904,
      "createdAt": "2025-04-07T20:07:42.486886Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Cogito v1 Preview Qwen 32B",
      "id": "cogito-v1-preview-qwen-32b",
      "family": "Other",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32759790592,
      "createdAt": "2025-04-07T20:13:57.394972Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek Coder 1.3B Base",
      "id": "deepseek-coder-1b-base",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 1346471936,
      "createdAt": "2024-06-18T21:19:08.877103Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek Prover V2",
      "id": "deepseek-prover-v2",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 671067257432,
      "createdAt": "2025-05-01T03:26:45.587294Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek R1 (Basic)",
      "id": "deepseek-r1-basic",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 671026419200,
      "createdAt": "2025-03-18T14:05:46.238727Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek R1 (Fast)",
      "id": "deepseek-r1",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 671026419200,
      "createdAt": "2025-01-20T18:27:53.770705Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Deepseek R1 05/28",
      "id": "deepseek-r1-0528",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 674352502272,
      "createdAt": "2025-05-28T18:19:37.425817Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek R1 0528 Distill Qwen 3 8B",
      "id": "deepseek-r1-0528-distill-qwen3-8b",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8190735360,
      "createdAt": "2025-06-03T17:05:04.102971Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek R1 Distill Llama 70B",
      "id": "deepseek-r1-distill-llama-70b",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 70553706496,
      "createdAt": "2025-01-21T22:44:20.585605Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek R1 Distill Llama 8B",
      "id": "deepseek-r1-distill-llama-8b",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8030261248,
      "createdAt": "2025-01-22T17:31:57.166736Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek R1 Distill Qwen 14B",
      "id": "deepseek-r1-distill-qwen-14b",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 14770033664,
      "createdAt": "2025-01-22T17:34:10.016215Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek R1 Distill Qwen 32B",
      "id": "deepseek-r1-distill-qwen-32b",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32763876352,
      "createdAt": "2025-01-22T00:11:01.910030Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek V3",
      "id": "deepseek-v3",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 671026419200,
      "createdAt": "2024-12-30T16:37:48.553193Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Deepseek V3 03-24",
      "id": "deepseek-v3-0324",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 671026419200,
      "createdAt": "2025-03-24T14:40:20.594012Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek V3.1",
      "id": "deepseek-v3p1",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 674352502272,
      "createdAt": "2025-08-21T06:49:48.289944Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek V3.1 Terminus",
      "id": "deepseek-v3p1-terminus",
      "family": "DeepSeek",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 674352502272,
      "createdAt": "2025-09-23T00:10:41.498599Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "DeepSeek-V4-Flash",
      "id": "deepseek-v4-flash",
      "family": "DeepSeek",
      "count": 1,
      "dedicated": [{
        "shape": "deepseek-v4-flash-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B300",
        "rlGpus": "6 × B300",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 284000000000,
      "createdAt": "2026-04-24T04:09:07.488210Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "DeepSeek-V4-Flash-0731",
      "id": "deepseek-v4-flash-0731",
      "family": "DeepSeek",
      "count": 2,
      "dedicated": [{
        "shape": "deepseek-v4-flash-0731-256k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "8 × B300",
        "rlGpus": "10 × B300",
        "ctx": 262144
      }, {
        "shape": "deepseek-v4-flash-0731-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B300",
        "rlGpus": "6 × B300",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 304000000000,
      "createdAt": "2026-07-31T16:14:42.430664Z",
      "rlAvailable": true,
      "hasServerless": true,
      "serverlessCtx": 262144,
      "hasDedicated": true
    }, {
      "model": "DeepSeek-V4-Pro-0813",
      "id": "deepseek-v4-pro-0813",
      "family": "DeepSeek",
      "count": 1,
      "dedicated": [{
        "shape": "deepseek-v4-pro-0813-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B300",
        "rlGpus": "16 × B300",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 1600000000000,
      "createdAt": "2026-08-13T16:05:55.091600Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "FARE-20B",
      "id": "fare-20b",
      "family": "Other",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 20914757184,
      "createdAt": "2025-11-22T02:00:56.449882Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "FireFunction V2",
      "id": "firefunction-v2",
      "family": "Other",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": null,
      "paramCount": 0,
      "createdAt": "2024-08-14T07:11:49.059752Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Gemma 3 27B Instruct",
      "id": "gemma-3-27b-it",
      "family": "Gemma 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 28418976512,
      "createdAt": "2025-04-15T20:19:19.459140Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Gemma 4 26B A4B IT",
      "id": "gemma-4-26b-a4b-it",
      "family": "Gemma 4",
      "count": 2,
      "dedicated": [{
        "shape": "gemma-4-26b-a4b-256k-b200",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B200",
        "rlGpus": "8 × B200",
        "ctx": 262144
      }, {
        "shape": "gemma-4-26b-a4b-256k-b200-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B200",
        "rlGpus": "8 × B200",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 131072,
      "paramCount": 26000000000,
      "createdAt": "2026-04-02T05:46:24.892571Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Gemma 4 31B IT",
      "id": "gemma-4-31b-it",
      "family": "Gemma 4",
      "count": 2,
      "dedicated": [{
        "shape": "gemma-4-31b-256k-b200",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B200",
        "rlGpus": "8 × B200",
        "ctx": 262144
      }, {
        "shape": "gemma-4-31b-256k-b200-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B200",
        "rlGpus": "8 × B200",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 131072,
      "paramCount": 32216731964,
      "createdAt": "2026-04-02T05:45:15.310864Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "GLM 5.1",
      "id": "glm-5p1",
      "family": "GLM",
      "count": 1,
      "dedicated": [{
        "shape": "glm-5p1-200k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B300",
        "rlGpus": "16 × B300",
        "ctx": 204785
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 743911218432,
      "createdAt": "2026-03-27T19:21:31.913585Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "GLM 5.2 FP8",
      "id": "glm-5p2-fp8",
      "family": "GLM",
      "count": 3,
      "dedicated": [{
        "shape": "glm-5p2-200k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "16 × B300",
        "rlGpus": "24 × B300",
        "ctx": 204736
      }, {
        "shape": "glm-5p2-200k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B300",
        "rlGpus": "16 × B300",
        "ctx": 204736
      }, {
        "shape": "glm-5p2-200k-batch-invariant-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B300",
        "rlGpus": "16 × B300",
        "ctx": 16384
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 743911218432,
      "createdAt": "2026-06-18T21:31:31.622427Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "GLM-4.5",
      "id": "glm-4p5",
      "family": "GLM",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 352797829024,
      "createdAt": "2025-07-29T17:20:36.175510Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "GLM-4.6",
      "id": "glm-4p6",
      "family": "GLM",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 352797829024,
      "createdAt": "2025-10-01T22:50:59.457245Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "GLM-4.7",
      "id": "glm-4p7",
      "family": "GLM",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 352797829024,
      "createdAt": "2025-12-22T19:14:38.409916Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "KAT Dev 32B",
      "id": "kat-dev-32b",
      "family": "Other",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32762123264,
      "createdAt": "2025-11-15T04:40:44.660458Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Kimi K2 Instruct",
      "id": "kimi-k2-instruct",
      "family": "Kimi",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 1026408232448,
      "createdAt": "2025-07-11T18:38:16.094851Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Kimi K2 Instruct 0905",
      "id": "kimi-k2-instruct-0905",
      "family": "Kimi",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 1028071273984,
      "createdAt": "2025-09-04T20:49:54.278632Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Kimi K2 Thinking",
      "id": "kimi-k2-thinking",
      "family": "Kimi",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 1028071273984,
      "createdAt": "2025-11-06T19:41:40.974632Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Kimi K2.5",
      "id": "kimi-k2p5",
      "family": "Kimi",
      "count": 1,
      "dedicated": [{
        "shape": "kimi-k2p5-text-only-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B300",
        "rlGpus": "16 × B300",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 65536,
      "paramCount": 1028542417904,
      "createdAt": "2026-01-27T01:19:30.456263Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Kimi K2.6",
      "id": "kimi-k2p6",
      "family": "Kimi",
      "count": 1,
      "dedicated": [{
        "shape": "kimi-k2p6-text-only-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B300",
        "rlGpus": "16 × B300",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 65536,
      "paramCount": 1028542417904,
      "createdAt": "2026-04-17T19:54:54.434998Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Kimi K2.7 Code",
      "id": "kimi-k2p7-code",
      "family": "Kimi",
      "count": 2,
      "dedicated": [{
        "shape": "kimi-k2p7-coder-256k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "32 × B300",
        "rlGpus": "40 × B300",
        "ctx": 262144
      }, {
        "shape": "kimi-k2p7-coder-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B300",
        "rlGpus": "16 × B300",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 65536,
      "paramCount": 1028542417904,
      "createdAt": "2026-06-12T17:00:00.491288Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Kimi K3",
      "id": "kimi-k3",
      "family": "Kimi",
      "count": 1,
      "dedicated": [{
        "shape": "kimi-k3-512k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "32 × B300",
        "rlGpus": "40 × B300",
        "ctx": 524288
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 2780913302112,
      "createdAt": "2026-07-19T17:50:09.542588Z",
      "rlAvailable": true,
      "hasServerless": true,
      "serverlessCtx": 196608,
      "hasDedicated": true
    }, {
      "model": "Llama 3 70B Instruct",
      "id": "llama-v3-70b-instruct",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 70553706496,
      "createdAt": "2024-04-18T17:43:40.631630Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama 3 70B Instruct (HF version)",
      "id": "llama-v3-70b-instruct-hf",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 70553706496,
      "createdAt": "2024-04-21T03:33:52.297689Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama 3 8B",
      "id": "llama-v3-8b",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8030261248,
      "createdAt": "2024-11-21T17:57:41.587530Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama 3 8B Instruct",
      "id": "llama-v3-8b-instruct",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8030261248,
      "createdAt": "2024-04-18T20:29:41.898013Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama 3 8B Instruct (HF version)",
      "id": "llama-v3-8b-instruct-hf",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8030261248,
      "createdAt": "2024-04-18T21:01:43.181110Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama 3.1 70B Instruct",
      "id": "llama-v3p1-70b-instruct",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 70553706496,
      "createdAt": "2024-07-18T07:22:37.013293Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama 3.1 8B Instruct",
      "id": "llama-v3p1-8b-instruct",
      "family": "Llama",
      "count": 1,
      "dedicated": [{
        "shape": "llama-v3p1-8b-instruct-128k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "1 × H200",
        "rlGpus": "2 × H200",
        "ctx": 131072
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8835567616,
      "createdAt": "2024-07-23T00:00:08.369396Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Llama 3.1 Nemotron 70B",
      "id": "llama-v3p1-nemotron-70b-instruct",
      "family": "Nemotron",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 70553706496,
      "createdAt": "2024-10-16T15:51:59.623355Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama 3.2 1B",
      "id": "llama-v3p2-1b",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 1498482688,
      "createdAt": "2024-09-25T15:59:15.568480Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama 3.2 1B Instruct",
      "id": "llama-v3p2-1b-instruct",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 1498482688,
      "createdAt": "2024-09-18T21:23:21.952789Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama 3.2 3B Instruct",
      "id": "llama-v3p2-3b-instruct",
      "family": "Llama",
      "count": 1,
      "dedicated": [{
        "shape": "llama-v3p2-3b-instruct-128k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "1 × H200",
        "rlGpus": "",
        "ctx": 131072
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 3606752256,
      "createdAt": "2024-09-18T21:24:41.300478Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Llama 3.3 70B Instruct",
      "id": "llama-v3p3-70b-instruct",
      "family": "Llama",
      "count": 2,
      "dedicated": [{
        "shape": "llama-v3p3-70b-instruct-128k-lora-b200",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B200",
        "rlGpus": "8 × B200",
        "ctx": 131072
      }, {
        "shape": "llama-v3p3-70b-instruct-64k-lora-b200",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B200",
        "rlGpus": "12 × B200",
        "ctx": 65536
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 77264592896,
      "createdAt": "2024-12-05T23:41:43.295895Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Llama Guard 3 8B",
      "id": "llama-guard-3-8b",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8030261248,
      "createdAt": "2024-11-05T21:03:47.654102Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama Guard v2 8B",
      "id": "llama-guard-2-8b",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8030261248,
      "createdAt": "2024-04-18T20:52:10.239390Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Llama Guard v3 1B",
      "id": "llama-guard-3-1b",
      "family": "Llama",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 1498482688,
      "createdAt": "2024-09-25T16:03:59.742240Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Minimax M3",
      "id": "minimax-m3",
      "family": "MiniMax",
      "count": 1,
      "dedicated": [{
        "shape": "minimax-m3-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B300",
        "rlGpus": "12 × B300",
        "ctx": 229376
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 428000000000,
      "createdAt": "2026-06-11T21:52:28.589913Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Ministral 3 3B Instruct 2512",
      "id": "ministral-3-3b-instruct-2512",
      "family": "Mistral",
      "count": 2,
      "dedicated": [{
        "shape": "ministral-3-3b-instruct-2512-16k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "1 × B200",
        "rlGpus": "",
        "ctx": 16384
      }, {
        "shape": "ministral-3-3b-instruct-2512-16k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "1 × B200",
        "rlGpus": "2 × B200",
        "ctx": 16384
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": null,
      "paramCount": 3000000000,
      "createdAt": "2025-11-30T23:45:43.216467Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "MiroThinker-1.7",
      "id": "mirothinker-1p7",
      "family": "Other",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 235093634560,
      "createdAt": "2026-05-14T23:37:09.924512Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Mistral Small 24B Instruct 2501",
      "id": "mistral-small-24b-instruct-2501",
      "family": "Mistral",
      "count": 1,
      "dedicated": [{
        "shape": "mistral-small-24b-instruct-2501-32k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "1 × H200",
        "rlGpus": "",
        "ctx": 32768
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 23572403200,
      "createdAt": "2025-01-30T12:59:04.586649Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Muse Glimmer 30B",
      "id": "muse-glimmer-30b",
      "family": "Other",
      "count": 2,
      "dedicated": [{
        "shape": "muse-glimmer-30b-131k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "2 × B200",
        "rlGpus": "3 × B200",
        "ctx": 131072
      }, {
        "shape": "muse-glimmer-30b-131k-lora",
        "method": "LoRA",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "1 × B200",
        "rlGpus": "2 × B200",
        "ctx": 131072
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 29776626688,
      "createdAt": "2026-08-10T01:54:06.581854Z",
      "rlAvailable": true,
      "hasServerless": true,
      "serverlessCtx": 131072,
      "hasDedicated": true
    }, {
      "model": "NVIDIA Nemotron 3 Super 120B A12B BF16",
      "id": "nemotron-3-super-120b-a12b-bf16",
      "family": "Nemotron",
      "count": 3,
      "dedicated": [{
        "shape": "nemotron-3-super-120b-a12b-bf16",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "8 × B200",
        "rlGpus": "12 × B200",
        "ctx": 262144
      }, {
        "shape": "nemotron-3-super-120b-a12b-bf16-128k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B200",
        "rlGpus": "12 × B200",
        "ctx": 131072
      }, {
        "shape": "nemotron-3-super-120b-a12b-bf16-262k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × H200",
        "rlGpus": "",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 120000000000,
      "createdAt": "2026-05-20T20:44:23.780645Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "NVIDIA Nemotron 3 Ultra BF16",
      "id": "nemotron-3-ultra-bf16",
      "family": "Nemotron",
      "count": 2,
      "dedicated": [{
        "shape": "nemotron-3-ultra-550b-a55b-bf16",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "16 × B300",
        "rlGpus": "24 × B300",
        "ctx": 262144
      }, {
        "shape": "nemotron-3-ultra-550b-a55b-bf16-lora",
        "method": "LoRA",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "8 × B300",
        "rlGpus": "16 × B300",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 549308108800,
      "createdAt": "2026-06-02T12:01:21.033623Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "NVIDIA Nemotron Nano 3 30B A3B",
      "id": "nemotron-nano-3-30b-a3b",
      "family": "Nemotron",
      "count": 2,
      "dedicated": [{
        "shape": "nemotron-nano-3-30b-a3b-262k-b200-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "2 × B200",
        "rlGpus": "3 × B200",
        "ctx": 262144
      }, {
        "shape": "nemotron-nano-3-30b-a3b-262k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "2 × H200",
        "rlGpus": "",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 31577937344,
      "createdAt": "2025-12-05T06:05:55.340633Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "OpenAI gpt-oss-120b",
      "id": "gpt-oss-120b",
      "family": "GPT-OSS",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 116829156672,
      "createdAt": "2025-08-04T22:13:20.599550Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "OpenAI gpt-oss-20b",
      "id": "gpt-oss-20b",
      "family": "GPT-OSS",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 20914757184,
      "createdAt": "2025-08-04T22:11:06.445132Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "OpenAI gpt-oss-safeguard-120b",
      "id": "gpt-oss-safeguard-120b",
      "family": "GPT-OSS",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 116829156672,
      "createdAt": "2025-11-07T06:03:23.252858Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "OpenAI gpt-oss-safeguard-20b",
      "id": "gpt-oss-safeguard-20b",
      "family": "GPT-OSS",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 20914757184,
      "createdAt": "2025-11-07T06:01:38.486434Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5 14B",
      "id": "qwen2p5-14b",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 14770033664,
      "createdAt": "2024-10-02T00:15:58.089865Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5 14B Instruct",
      "id": "qwen-v2p5-14b-instruct",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 14770033664,
      "createdAt": "2024-09-19T23:56:28.945326Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5 14B Instruct",
      "id": "qwen2p5-14b-instruct",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 14770033664,
      "createdAt": "2024-10-02T00:15:23.266955Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5 32B",
      "id": "qwen2p5-32b",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32763876352,
      "createdAt": "2024-10-02T00:14:25.202229Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5 32B Instruct",
      "id": "qwen2p5-32b-instruct",
      "family": "Qwen 2 & earlier",
      "count": 1,
      "dedicated": [{
        "shape": "qwen2p5-32b-instruct-32k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × H200",
        "rlGpus": "",
        "ctx": 32768
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32763876352,
      "createdAt": "2024-10-02T00:13:26.946121Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 2.5-Coder 14B",
      "id": "qwen2p5-coder-14b",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 14770033664,
      "createdAt": "2024-11-12T00:57:49.735049Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5-Coder 14B Instruct",
      "id": "qwen2p5-coder-14b-instruct",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 14770033664,
      "createdAt": "2024-11-12T00:55:59.580567Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5-Coder 32B",
      "id": "qwen2p5-coder-32b",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32763876352,
      "createdAt": "2024-11-12T01:10:55.640513Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5-Coder 32B Instruct",
      "id": "qwen2p5-coder-32b-instruct",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32763876352,
      "createdAt": "2024-11-12T01:09:48.505008Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5-Coder 32B Instruct 128K",
      "id": "qwen2p5-coder-32b-instruct-128k",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32763876352,
      "createdAt": "2024-11-12T01:09:48.505008Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5-Coder 32B Instruct 32K RoPE",
      "id": "qwen2p5-coder-32b-instruct-32k-rope",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32763876352,
      "createdAt": "2024-11-12T01:09:48.505008Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5-Coder 32B Instruct 64k",
      "id": "qwen2p5-coder-32b-instruct-64k",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32763876352,
      "createdAt": "2024-11-12T01:09:48.505008Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 2.5-VL 7B Instruct",
      "id": "qwen2p5-vl-7b-instruct",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8292166656,
      "createdAt": "2025-03-31T03:43:08.870373Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3 0.6B",
      "id": "qwen3-0p6b",
      "family": "Qwen 3",
      "count": 1,
      "dedicated": [{
        "shape": "qwen3-0p6b-65k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "1 × B200",
        "rlGpus": "2 × B200",
        "ctx": 65536
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 751632384,
      "createdAt": "2025-04-28T23:44:56.795571Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3 1.7B",
      "id": "qwen3-1p7b",
      "family": "Qwen 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 2031739904,
      "createdAt": "2025-04-29T04:53:14.109687Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3 14B",
      "id": "qwen3-14b",
      "family": "Qwen 3",
      "count": 1,
      "dedicated": [{
        "shape": "qwen3-14b-128k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "2 × H200",
        "rlGpus": "4 × H200",
        "ctx": 131072
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 14768307200,
      "createdAt": "2025-04-28T23:41:05.797558Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3 235B A22B",
      "id": "qwen3-235b-a22b",
      "family": "Qwen 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 235093634560,
      "createdAt": "2025-04-29T00:07:29.649090Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3 235B A22B Instruct 2507",
      "id": "qwen3-235b-a22b-instruct-2507",
      "family": "Qwen 3",
      "count": 1,
      "dedicated": [{
        "shape": "qwen3-235b-a22b-instruct-2507-128k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B300",
        "rlGpus": "12 × B300",
        "ctx": 128000
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 235093634560,
      "createdAt": "2025-07-21T19:00:24.457677Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3 235B A22B Thinking 2507",
      "id": "qwen3-235b-a22b-thinking-2507",
      "family": "Qwen 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 235093634560,
      "createdAt": "2025-07-25T14:57:14.624557Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3 30B A3B Instruct 2507",
      "id": "qwen3-30b-a3b-instruct-2507",
      "family": "Qwen 3",
      "count": 1,
      "dedicated": [{
        "shape": "qwen3-30b-a3b-instruct-2507-128k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "8 × B200",
        "rlGpus": "10 × B200",
        "ctx": 128000
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": true,
      "rlLoraAvailable": false,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 30532122624,
      "createdAt": "2025-07-29T16:59:48.084495Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3 30B A3B Thinking 2507",
      "id": "qwen3-30b-a3b-thinking-2507",
      "family": "Qwen 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 30532122624,
      "createdAt": "2025-07-30T23:00:46.048233Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3 30B-A3B",
      "id": "qwen3-30b-a3b",
      "family": "Qwen 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 30532122624,
      "createdAt": "2025-04-28T22:08:53.637383Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3 32B",
      "id": "qwen3-32b",
      "family": "Qwen 3",
      "count": 1,
      "dedicated": [{
        "shape": "qwen3-32b-128k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B200",
        "rlGpus": "10 × B200",
        "ctx": 131072
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32762123264,
      "createdAt": "2025-04-28T23:50:01.555797Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3 4B",
      "id": "qwen3-4b",
      "family": "Qwen 3",
      "count": 2,
      "dedicated": [{
        "shape": "qwen3-4b-minimum",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "1 × B200",
        "rlGpus": "2 × B200",
        "ctx": 65536
      }, {
        "shape": "qwen3-4b-minimum-lora",
        "method": "LoRA",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "1 × B200",
        "rlGpus": "2 × B200",
        "ctx": 32768
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": true
      },
      "trainCtx": 131072,
      "paramCount": 4411424256,
      "createdAt": "2025-04-28T23:50:29.787828Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3 4B Instruct 2507",
      "id": "qwen3-4b-instruct-2507",
      "family": "Qwen 3",
      "count": 1,
      "dedicated": [{
        "shape": "qwen3-4b-instruct-2507-256k-b200-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "1 × B200",
        "rlGpus": "2 × B200",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 4411424256,
      "createdAt": "2025-10-16T00:16:15.428618Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3 8B",
      "id": "qwen3-8b",
      "family": "Qwen 3",
      "count": 2,
      "dedicated": [{
        "shape": "qwen3-8b-128k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B200",
        "rlGpus": "5 × B200",
        "ctx": 128000
      }, {
        "shape": "qwen3-8b-256k-h200-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B200",
        "rlGpus": "9 × B200",
        "ctx": 256000
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 131072,
      "paramCount": 8190735360,
      "createdAt": "2025-04-29T06:07:42.965494Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3 Coder 30B A3B Instruct",
      "id": "qwen3-coder-30b-a3b-instruct",
      "family": "Qwen 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 30532122624,
      "createdAt": "2025-08-01T15:53:08.972353Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3 VL 235B A22B Instruct",
      "id": "qwen3-vl-235b-a22b-instruct",
      "family": "Qwen 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 235670022896,
      "createdAt": "2025-09-24T20:28:09.336982Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3 VL 235B A22B Thinking",
      "id": "qwen3-vl-235b-a22b-thinking",
      "family": "Qwen 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 65536,
      "paramCount": 235670022896,
      "createdAt": "2025-09-24T23:12:12.121869Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3 VL 30B A3B Instruct",
      "id": "qwen3-vl-30b-a3b-instruct",
      "family": "Qwen 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 31070754032,
      "createdAt": "2025-10-08T21:32:51.135952Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3 VL 30B A3B Thinking",
      "id": "qwen3-vl-30b-a3b-thinking",
      "family": "Qwen 3",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 31070754032,
      "createdAt": "2025-10-08T21:47:43.506441Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3-VL-8B-Instruct",
      "id": "qwen3-vl-8b-instruct",
      "family": "Qwen 3",
      "count": 2,
      "dedicated": [{
        "shape": "qwen3-vl-8b-256k-h200-lora",
        "method": "LoRA",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "8 × H200",
        "rlGpus": "9 × H200",
        "ctx": 262144
      }, {
        "shape": "qwen3-vl-8b-vision-lora",
        "method": "LoRA",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "8 × H200",
        "rlGpus": "9 × H200",
        "ctx": 32768
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": true,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8767123696,
      "createdAt": "2025-12-02T23:24:32.555776Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3.5 27B",
      "id": "qwen3p5-27b",
      "family": "Qwen 3.5",
      "count": 3,
      "dedicated": [{
        "shape": "qwen3p5-27b-256k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B200",
        "rlGpus": "6 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p5-27b-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B200",
        "rlGpus": "6 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p5-27b-64k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "1 × B200",
        "rlGpus": "3 × B200",
        "ctx": 65536
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 131072,
      "paramCount": 27356728560,
      "createdAt": "2026-03-02T18:05:21.364517Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3.5 35B A3B",
      "id": "qwen3p5-35b-a3b",
      "family": "Qwen 3.5",
      "count": 2,
      "dedicated": [{
        "shape": "qwen3p5-35b-a3b-256k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B200",
        "rlGpus": "5 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p5-35b-a3b-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B200",
        "rlGpus": "5 × B200",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 131072,
      "paramCount": 35107181936,
      "createdAt": "2026-02-27T07:26:01.577420Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3.5 397B A17B",
      "id": "qwen3p5-397b-a17b",
      "family": "Qwen 3.5",
      "count": 2,
      "dedicated": [{
        "shape": "qwen3p5-397b-a17b-256k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "16 × B300",
        "rlGpus": "24 × B300",
        "ctx": 262144
      }, {
        "shape": "qwen3p5-397b-a17b-256k-lora-b300",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "8 × B300",
        "rlGpus": "16 × B300",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 65536,
      "paramCount": 396802360816,
      "createdAt": "2026-02-18T04:17:34.977150Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3.5 9B",
      "id": "qwen3p5-9b",
      "family": "Qwen 3.5",
      "count": 3,
      "dedicated": [{
        "shape": "qwen3p5-9b-256k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "2 × B200",
        "rlGpus": "3 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p5-9b-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "2 × B200",
        "rlGpus": "3 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p5-9b-65k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "2 × B200",
        "rlGpus": "3 × B200",
        "ctx": 65536
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 131072,
      "paramCount": 9409813744,
      "createdAt": "2026-04-01T17:17:28.437129Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3.6 27B",
      "id": "qwen3p6-27b",
      "family": "Qwen 3.6",
      "count": 3,
      "dedicated": [{
        "shape": "qwen3p6-27b-256k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B200",
        "rlGpus": "6 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p6-27b-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B200",
        "rlGpus": "6 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p6-27b-128k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "2 × B200",
        "rlGpus": "4 × B200",
        "ctx": 131072
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": true,
        "rlFullParameterTunable": true
      },
      "trainCtx": 131072,
      "paramCount": 27356728560,
      "createdAt": "2026-05-02T03:20:56.574341Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3.6 Plus",
      "id": "qwen3p6-plus",
      "family": "Qwen 3.6",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": null,
      "paramCount": 396802360816,
      "createdAt": "2026-04-05T00:55:21.455155Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Qwen 3.6-35B-A3B",
      "id": "qwen3p6-35b-a3b",
      "family": "Qwen 3.6",
      "count": 4,
      "dedicated": [{
        "shape": "qwen3p6-35b-a3b-256k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B200",
        "rlGpus": "6 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p6-35b-a3b-262k",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B300",
        "rlGpus": "6 × B300",
        "ctx": 262144
      }, {
        "shape": "qwen3p6-35b-a3b-256k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B200",
        "rlGpus": "6 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p6-35b-a3b-262k-lora",
        "method": "LoRA",
        "managedSft": true,
        "managedDpo": true,
        "gpus": "4 × B300",
        "rlGpus": "6 × B300",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": true,
      "managedDpoLora": true,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": true,
        "supervisedFullParameterTunable": true,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 35107181936,
      "createdAt": "2026-04-17T04:13:27.544374Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3.7 Plus VL Instruct",
      "id": "qwen3p7-plus-vl-instruct",
      "family": "Qwen 3.7",
      "count": 1,
      "dedicated": [{
        "shape": "qwen3p7-plus-vl-instruct-256k-lora",
        "method": "LoRA",
        "managedSft": false,
        "managedDpo": false,
        "hideSpecs": true,
        "rlAvailable": true
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": false,
      "rlLoraAvailable": true,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": null,
      "paramCount": 396802360816,
      "createdAt": "2026-06-07T16:40:20.137596Z",
      "rlAvailable": true,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": true
    }, {
      "model": "Qwen 3.8 27B",
      "id": "qwen3p8-27b",
      "family": "Qwen 3",
      "count": 4,
      "dedicated": [{
        "shape": "qwen3p8-27b-262k-b200",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B200",
        "rlGpus": "6 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p8-27b-262k-b300",
        "method": "Full-Param",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B300",
        "rlGpus": "6 × B300",
        "ctx": 262144
      }, {
        "shape": "qwen3p8-27b-262k-b200-lora",
        "method": "LoRA",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B200",
        "rlGpus": "6 × B200",
        "ctx": 262144
      }, {
        "shape": "qwen3p8-27b-262k-b300-lora",
        "method": "LoRA",
        "managedSft": false,
        "managedDpo": false,
        "gpus": "4 × B300",
        "rlGpus": "6 × B300",
        "ctx": 262144
      }],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": false,
      "rftLoraCtx": 0,
      "apiLora": true,
      "apiFull": true,
      "rlLoraAvailable": true,
      "rlFullAvailable": true,
      "flags": {
        "useTrainingV2": true,
        "rlTunable": false,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 27356728560,
      "createdAt": "2026-08-14T16:45:00.989936Z",
      "rlAvailable": true,
      "hasServerless": true,
      "serverlessCtx": 131072,
      "hasDedicated": true
    }, {
      "model": "Qwen QWQ 32B Preview",
      "id": "qwen-qwq-32b-preview",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32763876352,
      "createdAt": "2024-11-27T20:23:10.171680Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "QWQ 32B",
      "id": "qwq-32b",
      "family": "Qwen 2 & earlier",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 32763876352,
      "createdAt": "2025-03-05T19:50:51.682955Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }, {
      "model": "Rolm OCR",
      "id": "rolm-ocr",
      "family": "Other",
      "count": 0,
      "dedicated": [],
      "serverless": [],
      "reference": [],
      "managedSftLora": false,
      "managedDpoLora": false,
      "rftLoraManaged": true,
      "rftLoraCtx": 32768,
      "apiLora": false,
      "apiFull": false,
      "rlLoraAvailable": false,
      "rlFullAvailable": false,
      "flags": {
        "useTrainingV2": false,
        "rlTunable": true,
        "supervisedLoraTunable": false,
        "supervisedFullParameterTunable": false,
        "rlLoraTunable": false,
        "rlFullParameterTunable": false
      },
      "trainCtx": 131072,
      "paramCount": 8292166656,
      "createdAt": "2025-06-09T16:39:58.790399Z",
      "rlAvailable": false,
      "hasServerless": false,
      "serverlessCtx": 0,
      "hasDedicated": false
    }]
  };
  const models = TRAINING_SHAPES_CATALOG.models ?? [];
  const generatedAt = TRAINING_SHAPES_CATALOG.generatedAt;
  const DASH = "\u2014";
  const EXCLUSIVE_MODEL_NAMES = {
    "qwen3p6-plus": "Qwen 3.6 Plus",
    "qwen3p7-plus-vl-instruct": "Qwen 3.7"
  };
  const isExclusiveModel = m => Boolean(m && EXCLUSIVE_MODEL_NAMES[m.id]);
  const displayModelName = m => EXCLUSIVE_MODEL_NAMES[m?.id] || m?.model || "";
  const modelFamilyGroup = m => {
    const family = m?.family || "Other";
    if (family.startsWith("Qwen ")) return "Qwen";
    if (family.startsWith("Gemma ")) return "Gemma";
    return family;
  };
  const bySurfaceThenName = (a, b) => (b.hasServerless ? 1 : 0) - (a.hasServerless ? 1 : 0) || a.model.localeCompare(b.model);
  const FAMILY_CHIP_ORDER = ["Qwen", "Llama", "DeepSeek", "Kimi", "GLM", "Gemma", "Mistral", "GPT-OSS", "Nemotron", "MiniMax"];
  const familyRank = family => {
    const index = FAMILY_CHIP_ORDER.indexOf(family);
    if (index !== -1) return index;
    return family === "Other" ? FAMILY_CHIP_ORDER.length + 1 : FAMILY_CHIP_ORDER.length;
  };
  const sorted = [...models].sort((a, b) => a.model.localeCompare(b.model));
  const familyOptions = ["All", ...Array.from(new Set(sorted.map(modelFamilyGroup))).sort((a, b) => familyRank(a) - familyRank(b) || a.localeCompare(b))];
  const defaultModelId = [...models].sort(bySurfaceThenName)[0]?.id ?? "";
  const [selectedModelId, setSelectedModelId] = useState(defaultModelId);
  const [open, setOpen] = useState(false);
  const [allFiltersOpen, setAllFiltersOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [availability, setAvailability] = useState("All");
  const [method, setMethod] = useState("All");
  const [modelFamily, setModelFamily] = useState("All");
  const [modelSize, setModelSize] = useState("All");
  const [view, setView] = useState("One model");
  const [otherOpen, setOtherOpen] = useState(false);
  const fmtCtx = ctx => {
    if (ctx === null || ctx === undefined || ctx === "") return DASH;
    const n = Number(ctx);
    if (!isFinite(n) || n <= 0) return DASH;
    let label;
    if (n % 1000 === 0) {
      label = n / 1000 + "K";
    } else if (n % 1024 === 0) {
      label = n / 1024 + "K";
    } else if (n >= 1000) {
      label = Math.round(n / 1000) + "K";
    } else {
      label = String(n);
    }
    return label + " (" + n.toLocaleString() + " tokens)";
  };
  const fmtParams = count => {
    const n = Number(count);
    if (!isFinite(n) || n <= 0) return DASH;
    if (n >= 1e12) return (n / 1e12).toFixed(n % 1e12 === 0 ? 0 : 1).replace(/\.0$/, "") + "T";
    if (n >= 1e9) return (n / 1e9).toFixed(1).replace(/\.0$/, "") + "B";
    if (n >= 1e6) return Math.round(n / 1e6) + "M";
    return n.toLocaleString();
  };
  function modes(lora, full) {
    const out = [];
    if (lora) out.push("LoRA");
    if (full) out.push("Full-Param");
    return out;
  }
  const apiModes = m => modes(m.apiLora, m.apiFull);
  const rlUnavailableNote = m => {
    if (!m) return null;
    const rlLora = m.dedicated.some(s => s.method === "LoRA" && (s.rlAvailable || s.rlGpus));
    const rlFull = m.dedicated.some(s => s.method === "Full-Param" && (s.rlAvailable || s.rlGpus));
    const gaps = [];
    if (m.apiLora && !rlLora) gaps.push("LoRA");
    if (m.apiFull && !rlFull) gaps.push("Full-param");
    if (!gaps.length) return null;
    if (gaps.length === apiModes(m).length) return "RL is not available for this model";
    return gaps.join(" and ") + " RL is not available";
  };
  const managedMethods = m => {
    const methods = [];
    if (m.managedSftLora) methods.push("SFT");
    if (m.managedDpoLora) methods.push("DPO");
    if (m.rftLoraManaged) methods.push("RFT");
    return methods;
  };
  const q = query.trim().toLowerCase();
  const matchAvail = m => availability === "All" ? true : availability === "Serverless" ? m.hasServerless : m.hasDedicated || isExclusiveModel(m);
  const matchMethod = m => method === "All" ? true : method === "LoRA" ? m.apiLora || m.hasServerless || managedMethods(m).length > 0 : m.apiFull;
  const matchFamily = m => modelFamily === "All" || modelFamilyGroup(m) === modelFamily;
  const matchSize = m => {
    if (modelSize === "All") return true;
    const size = Number(m.paramCount);
    if (!isFinite(size) || size <= 0) return false;
    if (modelSize === "Under 10B") return size < 10e9;
    if (modelSize === "10B\u201330B") return size >= 10e9 && size <= 30e9;
    if (modelSize === "30B\u201370B") return size > 30e9 && size <= 70e9;
    return size > 70e9;
  };
  const hasApiMode = m => m.apiLora || m.apiFull || isExclusiveModel(m);
  const byName = (a, b) => displayModelName(a).localeCompare(displayModelName(b));
  const filteredBase = sorted.filter(m => matchAvail(m) && matchMethod(m) && matchFamily(m) && matchSize(m));
  const trainablePool = filteredBase.filter(m => hasApiMode(m) || m.hasServerless);
  const familyRecency = {};
  for (const m of trainablePool) {
    const fam = modelFamilyGroup(m);
    const ts = m.createdAt || "";
    if (ts > (familyRecency[fam] || "")) familyRecency[fam] = ts;
  }
  const trainableModels = [...trainablePool].sort((a, b) => {
    const famA = modelFamilyGroup(a);
    const famB = modelFamilyGroup(b);
    if (famA !== famB) {
      return (familyRecency[famB] || "").localeCompare(familyRecency[famA] || "") || famA.localeCompare(famB);
    }
    return (b.createdAt || "").localeCompare(a.createdAt || "") || byName(a, b);
  });
  const otherModels = filteredBase.filter(m => !hasApiMode(m) && !m.hasServerless).sort(byName);
  const filtered = [...trainableModels, ...otherModels];
  const ordered = filtered.filter(m => !q || displayModelName(m).toLowerCase().includes(q) || m.model.toLowerCase().includes(q) || m.id.toLowerCase().includes(q));
  const current = (filtered.find(m => m.id === selectedModelId) ?? filtered[0]) ?? null;
  useEffect(() => {
    if (current && current.id !== selectedModelId) setSelectedModelId(current.id);
  }, [current, selectedModelId]);
  const tag = (bg, fg) => ({
    display: "inline-flex",
    alignItems: "center",
    padding: "1px 7px",
    borderRadius: 6,
    fontSize: 11,
    fontWeight: 600,
    lineHeight: 1.4,
    backgroundColor: bg,
    color: fg,
    whiteSpace: "nowrap"
  });
  const methodStyle = m => m === "LoRA" ? tag("rgba(37,99,235,0.15)", "#2563eb") : m === "Full-Param" ? tag("rgba(217,119,6,0.18)", "#b45309") : tag("rgba(113,113,122,0.16)", "#52525b");
  const serverlessStyle = tag("rgba(147,51,234,0.16)", "#7c3aed");
  const exclusiveStyle = tag("rgba(234,88,12,0.14)", "#c2410c");
  const badgeStyle = ok => ok ? tag("rgba(5,150,105,0.16)", "#047857") : tag("rgba(113,113,122,0.14)", "#71717a");
  const Tag = ({style, children}) => <span style={style}>{children}</span>;
  const Shell = ({children}) => <div className="rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900">
      {children}
    </div>;
  const Divider = () => <div className="border-t border-zinc-100 dark:border-zinc-800" />;
  const Link = ({href, children}) => <a href={href} className="text-purple-600 dark:text-purple-400 underline hover:text-purple-700 dark:hover:text-purple-300">
      {children}
    </a>;
  const SectionHeading = ({title, sub}) => <div className="flex items-baseline gap-2 flex-wrap">
      <span className="text-base font-semibold text-zinc-900 dark:text-zinc-100">{title}</span>
      {sub && <span className="text-xs text-zinc-500 dark:text-zinc-400">{sub}</span>}
    </div>;
  const Label = ({children}) => <span className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
      {children}
    </span>;
  const Body = ({children}) => <p className="text-sm text-zinc-700 dark:text-zinc-300">{children}</p>;
  const Muted = ({children}) => <span className="text-[11px] text-zinc-400 dark:text-zinc-500">{children}</span>;
  const MethodBubble = ({label, supported}) => <div className="flex flex-col items-center gap-1.5">
      <span style={{
    ...methodStyle(label),
    padding: "6px 18px",
    fontSize: 13,
    borderRadius: 8,
    opacity: supported ? 1 : 0.5
  }}>
        {label}
      </span>
      <span className="text-xs font-medium" style={{
    color: supported ? "#047857" : "#71717a"
  }}>
        {supported ? "Supported" : "Not supported"}
      </span>
    </div>;
  const MethodRow = ({label, modes: modeList, note}) => <div className="flex items-start justify-between gap-3">
      <span className="text-sm text-zinc-700 dark:text-zinc-300">
        {label}
        {note && modeList.length > 0 && <span className="block text-[11px] font-normal text-zinc-500 dark:text-zinc-400">
            {note}
          </span>}
      </span>
      <span className="flex gap-1 flex-wrap justify-end shrink-0">
        {modeList.length > 0 ? modeList.map(m => <Tag key={m} style={methodStyle(m)}>
              {m}
            </Tag>) : <Tag style={badgeStyle(false)}>Not available</Tag>}
      </span>
    </div>;
  const SurfaceCard = ({title, sub, children, footnote}) => <Shell>
      <div className="flex flex-col gap-0.5 px-4 py-3 border-b border-zinc-100 dark:border-zinc-800">
        <span className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">{title}</span>
        <span className="text-xs text-zinc-500 dark:text-zinc-400">{sub}</span>
      </div>
      <div className="p-4 flex flex-col gap-2.5">
        {children}
        {footnote && <p className="text-[11px] text-zinc-500 dark:text-zinc-400 pt-1">{footnote}</p>}
      </div>
    </Shell>;
  const Field = ({label, value}) => <div className="flex flex-col gap-0.5">
      <Label>{label}</Label>
      <span className="text-sm font-medium text-zinc-800 dark:text-zinc-200">{value}</span>
    </div>;
  const GpuField = ({shape}) => <div className="flex flex-col gap-0.5">
      <Label>GPUs required</Label>
      <span className="text-sm font-medium text-zinc-800 dark:text-zinc-200">{shape.gpus}</span>
      {shape.rlGpus && <span className="text-sm font-medium text-zinc-800 dark:text-zinc-200">
          {shape.rlGpus} (for RL)
          <span className="block text-[11px] font-normal text-zinc-500 dark:text-zinc-400">
            Trainer + rollout deployment
          </span>
        </span>}
    </div>;
  const FirectlCommand = ({label, command}) => {
    const [copied, setCopied] = useState(false);
    const copy = () => {
      try {
        navigator.clipboard.writeText(command);
        setCopied(true);
        setTimeout(() => setCopied(false), 1500);
      } catch (e) {}
    };
    return <div className="flex flex-col gap-1">
        <Label>{label}</Label>
        <div className="flex items-stretch rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 overflow-hidden">
          <code className="flex-1 min-w-0 px-2.5 py-1.5 text-[11px] font-mono text-zinc-800 dark:text-zinc-200 overflow-x-auto whitespace-nowrap">
            {command}
          </code>
          <button type="button" onClick={copy} aria-label="Copy command" className="shrink-0 flex items-center gap-1 px-2.5 border-l border-zinc-200 dark:border-zinc-700 text-[11px] font-medium text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors">
            {copied ? <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                <path d="M5 13l4 4L19 7" stroke="#047857" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg> : <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                <rect x="9" y="9" width="11" height="11" rx="2" stroke="currentColor" strokeWidth="2" />
                <path d="M5 15V5a2 2 0 012-2h10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>}
            <span>{copied ? "Copied" : "Copy"}</span>
          </button>
        </div>
      </div>;
  };
  const FilterGroup = ({label, options, value, onChange}) => <div className="flex flex-col gap-1">
      <Label>{label}</Label>
      <div className="inline-flex gap-1 flex-wrap">
        {options.map(o => {
    const active = value === o;
    return <button key={o} type="button" onClick={() => onChange(o)} className="px-2.5 py-1 rounded-md text-xs font-medium transition-colors" style={active ? {
      backgroundColor: "#7c3aed",
      color: "#ffffff",
      border: "1px solid #7c3aed"
    } : {
      backgroundColor: "transparent",
      color: "#71717a",
      border: "1px solid rgba(113,113,122,0.40)"
    }}>
              {o}
            </button>;
  })}
      </div>
    </div>;
  if (sorted.length === 0) {
    return <p className="text-sm text-zinc-500 dark:text-zinc-400">No customer-ready models found.</p>;
  }
  const TABLE_GRID = {
    display: "grid",
    gridTemplateColumns: "minmax(0,1.6fr) minmax(0,1.1fr) minmax(0,1.2fr) minmax(0,0.9fr)",
    gap: 10,
    alignItems: "start"
  };
  const TableModes = ({modes: modeList}) => modeList.length === 0 ? <Muted>{DASH}</Muted> : <span className="flex flex-col gap-1 items-start">
        {modeList.map(m => <Tag key={m} style={methodStyle(m)}>
            {m}
          </Tag>)}
      </span>;
  const ModelRow = ({m}) => <div style={TABLE_GRID} className="px-1 py-2.5 border-t border-zinc-100 dark:border-zinc-800">
      <span>
        <span className="flex items-center gap-2 flex-wrap text-sm font-medium text-zinc-900 dark:text-zinc-100">
          <span>{displayModelName(m)}</span>
          {isExclusiveModel(m) && <Tag style={exclusiveStyle}>Fireworks-exclusive closed source model</Tag>}
        </span>
        {!isExclusiveModel(m) && <span className="block text-[11px] font-mono text-zinc-500 dark:text-zinc-400">
            {m.id}
          </span>}
        {m.hasServerless && <span className="block mt-1">
            <Tag style={serverlessStyle}>Supports serverless</Tag>
          </span>}
      </span>
      <span className="flex flex-col gap-1 items-start">
        {isExclusiveModel(m) ? <Muted>{DASH}</Muted> : managedMethods(m).length > 0 ? managedMethods(m).map(label => <Tag key={label} style={badgeStyle(true)}>
              {label}
            </Tag>) : <Muted>{DASH}</Muted>}
      </span>
      <TableModes modes={isExclusiveModel(m) ? [] : apiModes(m)} />
      <TableModes modes={isExclusiveModel(m) ? [] : m.hasServerless ? ["LoRA"] : []} />
    </div>;
  const Filters = () => <div className="flex flex-col gap-2.5">
      <div className="flex flex-wrap gap-x-6 gap-y-2.5">
        <FilterGroup label="Availability" options={["All", "Serverless", "Dedicated"]} value={availability} onChange={setAvailability} />
        <FilterGroup label="Method" options={["All", "LoRA", "Full-Param"]} value={method} onChange={setMethod} />
      </div>
      <FilterGroup label="Model family" options={familyOptions} value={modelFamily} onChange={setModelFamily} />
      <FilterGroup label="Model size" options={["All", "Under 10B", "10B\u201330B", "30B\u201370B", "70B+"]} value={modelSize} onChange={setModelSize} />
    </div>;
  const activeFilterCount = [availability, method, modelFamily, modelSize].filter(value => value !== "All").length;
  return <div className="not-prose mt-4 mb-6 p-4 md:p-6 rounded-2xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900">
      <div className="mb-4 flex items-end justify-between gap-3 flex-wrap">
        <FilterGroup label="View" options={["One model", "All models"]} value={view} onChange={setView} />
        {generatedAt && <Muted>
            {models.length} models · synced {generatedAt}
          </Muted>}
      </div>

      {view === "All models" && <>
          <div className="relative mb-4">
            <button type="button" onClick={() => setAllFiltersOpen(value => !value)} className="inline-flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 hover:border-zinc-400 dark:hover:border-zinc-500 transition-colors">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                <path d="M4 7h16M7 12h10M10 17h4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
              <span>Filters{activeFilterCount > 0 ? ` (${activeFilterCount})` : ""}</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" className="transition-transform" style={{
    transform: allFiltersOpen ? "rotate(180deg)" : "none"
  }}>
                <path d="M6 9l6 6 6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
            {allFiltersOpen && <>
                <div className="fixed inset-0 z-10" onClick={() => setAllFiltersOpen(false)} />
                <div className="absolute z-20 left-0 right-0 mt-2 p-4 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-xl">
                  <Filters />
                </div>
              </>}
          </div>
          <div style={{
    overflowX: "auto"
  }}>
            <div style={{
    minWidth: 560
  }}>
              <div style={TABLE_GRID} className="px-1 pb-2">
                <Label>Model</Label>
                <a href="/fine-tuning/managed-finetuning-intro" className="hover:underline">
                  <Label>Managed</Label>
                </a>
                <a href="/fine-tuning/training-api/introduction" className="hover:underline">
                  <Label>Training API</Label>
                </a>
                <a href="/fine-tuning/training-api/serverless" className="hover:underline">
                  <Label>Serverless</Label>
                </a>
              </div>
              {trainableModels.length > 0 && <div>
                  {trainableModels.map(m => <ModelRow key={m.id} m={m} />)}
                </div>}
              {otherModels.length > 0 && <div>
                  <button type="button" onClick={() => setOtherOpen(v => !v)} className="w-full px-1 pt-4 pb-1.5 border-t border-zinc-200 dark:border-zinc-700 flex items-center gap-2 text-left">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" className="text-zinc-400 shrink-0 transition-transform" style={{
    transform: otherOpen ? "rotate(90deg)" : "none"
  }}>
                      <path d="M9 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    <span className="text-xs font-semibold uppercase tracking-wide text-zinc-700 dark:text-zinc-300">
                      Other
                    </span>
                    <span className="text-[11px] text-zinc-400 dark:text-zinc-500">
                      {otherModels.length} models · managed only
                    </span>
                  </button>
                  {otherOpen && otherModels.map(m => <ModelRow key={m.id} m={m} />)}
                </div>}
              {filtered.length === 0 && <p className="px-1 py-3 text-sm text-zinc-500 dark:text-zinc-400">
                  No models match the current filters.
                </p>}
            </div>
          </div>
        </>}

      {view === "One model" && <>
          <div className="mb-5">
            <label className="block text-xs font-medium mb-1 text-zinc-500 dark:text-zinc-400">Model</label>
            <div className="relative">
              <button type="button" onClick={() => setOpen(v => !v)} className="w-full flex items-center justify-between gap-2 px-3 py-2.5 rounded-xl text-sm border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 hover:border-zinc-400 dark:hover:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-purple-500/40 transition-colors">
                <span className="flex items-center gap-2 min-w-0">
                  <span className="font-medium truncate">
                    {current ? displayModelName(current) : "No matching models"}
                  </span>
                  {current && isExclusiveModel(current) && <Tag style={exclusiveStyle}>Fireworks-exclusive closed source model</Tag>}
                  {current && current.hasServerless && <Tag style={serverlessStyle}>Supports Serverless</Tag>}
                </span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="text-zinc-400 shrink-0 transition-transform" style={{
    transform: open ? "rotate(180deg)" : "none"
  }}>
                  <path d="M6 9l6 6 6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </button>

              {open && <>
                  <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />
                  <div className="absolute z-20 mt-2 w-full rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-xl overflow-hidden">
                    <div className="p-2 border-b border-zinc-100 dark:border-zinc-800">
                      <div className="relative">
                        <span className="absolute inset-y-0 left-2.5 flex items-center text-zinc-400 pointer-events-none">
                          <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                            <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
                            <path d="M21 21l-4.3-4.3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                          </svg>
                        </span>
                        <input autoFocus type="text" value={query} onChange={e => setQuery(e.target.value)} placeholder="Search models..." className="w-full pl-8 pr-3 py-2 rounded-lg text-sm border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 outline-none focus:ring-2 focus:ring-purple-500/40 focus:border-purple-500/40" />
                      </div>
                    </div>
                    <div className="px-3 py-2.5 border-b border-zinc-100 dark:border-zinc-800">
                      <Filters />
                    </div>
                    <div className="max-h-64 overflow-y-auto py-1">
                      {ordered.map(m => {
    const active = m.id === selectedModelId;
    return <button key={m.id} type="button" onClick={() => {
      setSelectedModelId(m.id);
      setOpen(false);
      setQuery("");
    }} className="w-full flex items-center justify-between gap-3 px-3 py-1.5 text-left text-sm text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors" style={active ? {
      backgroundColor: "rgba(124,58,237,0.12)",
      color: "#7c3aed"
    } : undefined}>
                            <span className="flex items-center gap-2 min-w-0">
                              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" className="shrink-0" style={{
      opacity: active ? 1 : 0,
      color: "#7c3aed"
    }}>
                                <path d="M5 13l4 4L19 7" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                              </svg>
                              <span className="font-medium truncate">{displayModelName(m)}</span>
                              {isExclusiveModel(m) && <Tag style={exclusiveStyle}>Fireworks-exclusive closed source model</Tag>}
                              {m.hasServerless && <Tag style={serverlessStyle}>Supports Serverless</Tag>}
                            </span>
                            <span className="text-[11px] text-zinc-400 dark:text-zinc-500 whitespace-nowrap">
                              {!isExclusiveModel(m) && m.count > 0 ? m.count + " shape" + (m.count === 1 ? "" : "s") : ""}
                            </span>
                          </button>;
  })}
                      {ordered.length === 0 && <div className="px-3 py-3 text-sm text-zinc-400">No models match the current filters.</div>}
                    </div>
                  </div>
                </>}
            </div>

            {current && !isExclusiveModel(current) && <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-2">
                <span className="font-mono">accounts/fireworks/models/{current.id}</span>
                {current.paramCount ? " \u00b7 " + fmtParams(current.paramCount) + " parameters" : ""}
              </p>}
          </div>

          {!current && <p className="text-sm text-zinc-500 dark:text-zinc-400">No models match the current filters.</p>}

          {current && isExclusiveModel(current) && <Shell>
              <div className="p-5 md:p-6">
                <p className="m-0 text-sm leading-6 text-zinc-700 dark:text-zinc-300">
                  Fireworks offers exclusive closed model tuning for {displayModelName(current)}.{" "}
                  <Link href="https://fireworks.ai/contact-training">
                    Contact us for more information
                  </Link>
                  .
                </p>
              </div>
            </Shell>}

          {current && !isExclusiveModel(current) && <div className="flex flex-col gap-3 mb-6">
              <SectionHeading title={"Where you can train " + displayModelName(current)} />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <SurfaceCard title="Managed training" sub="Fireworks runs the job: UI, firectl, or REST" footnote={<>
                      Managed jobs are LoRA-only. Full-parameter training runs on the Training
                      API.{" "}
                      <Link href="/fine-tuning/managed-finetuning-intro">Read more</Link>
                    </>}>
                  <MethodRow label="SFT" modes={current.managedSftLora ? ["LoRA"] : []} />
                  <MethodRow label="DPO" modes={current.managedDpoLora ? ["LoRA"] : []} />
                  {}
                  <MethodRow label="RFT" modes={current.rftLoraManaged ? ["LoRA"] : []} note="Reinforcement fine-tuning" />
                </SurfaceCard>

                {}
                <SurfaceCard title="Serverless Training API" sub="Shared pooled trainer, billed per token" footnote={current.hasServerless ? <>
                        Common workflows include: SFT, DPO, RL, etc. Private preview:{" "}
                        <Link href="https://fireworks.ai/contact-training">request access</Link> and
                        select “Serverless Training API.”{" "}
                        <Link href="/fine-tuning/training-api/serverless">Read more</Link>.
                      </> : <>
                        Not on the shared pool. Run this model on a dedicated shape instead.{" "}
                        <Link href="/fine-tuning/training-api/serverless">Read more</Link>
                      </>}>
                  <div className="flex items-center gap-6 pt-1">
                    <MethodBubble label="LoRA" supported={current.hasServerless} />
                    <p className="min-w-0 flex-1 text-[11px] leading-snug text-zinc-600 dark:text-zinc-400">
                      Serverless only supports LoRA training
                    </p>
                  </div>
                  {current.hasServerless && <>
                      <Divider />
                      <Field label="Max context length" value={fmtCtx(current.serverlessCtx)} />
                    </>}
                </SurfaceCard>

                {}
                <SurfaceCard title="Dedicated Training API" sub="Runs on dedicated GPUs, reserved for your job" footnote={<>
                      Loop primitives. Common workflows include: SFT, DPO
                      {rlUnavailableNote(current) ? "" : ", RL"}, etc.
                      {rlUnavailableNote(current) ? "*" : ""}{" "}
                      <Link href="/fine-tuning/training-api/introduction">Read more</Link>
                      {rlUnavailableNote(current) && <span className="block pt-0.5">*{rlUnavailableNote(current)}</span>}
                    </>}>
                  <div className="flex gap-8 pt-1">
                    <MethodBubble label="LoRA" supported={current.apiLora} />
                    <MethodBubble label="Full-Param" supported={current.apiFull} />
                  </div>
                  {}
                  {current.dedicated.length > 0 && <>
                      <Divider />
                      <Field label="Max context length" value="Choose from shape below" />
                    </>}
                </SurfaceCard>
              </div>
            </div>}

          {current && !isExclusiveModel(current) && current.dedicated.length > 0 && <div className="flex flex-col gap-3">
              <SectionHeading title="Training shapes" />
              <Body>
                Training shapes are only for the dedicated Training API; they fix the GPU layout
                and context limit for a trainer replica. Learn more about{" "}
                <Link href="/fine-tuning/training-api/training-shapes">training shapes</Link>.
              </Body>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {current.dedicated.map(s => <Shell key={s.shape}>
                    <div className="flex flex-col gap-1.5 items-start px-4 py-3 border-b border-zinc-100 dark:border-zinc-800">
                      <span className="font-mono text-xs text-zinc-900 dark:text-zinc-100 break-words">{s.shape}</span>
                      <Tag style={methodStyle(s.method)}>{s.method}</Tag>
                    </div>
                    <div className="p-4 flex flex-col gap-3">
                      {!s.hideSpecs && <>
                          <GpuField shape={s} />
                          <Field label="Max context" value={fmtCtx(s.ctx)} />
                          <Divider />
                        </>}
                      <FirectlCommand label="Fetch this shape" command={"firectl training-shape get accounts/fireworks/trainingShapes/" + s.shape} />
                    </div>
                  </Shell>)}
              </div>
            </div>}
        </>}
    </div>;
};

Managed training, the Training API, and serverless training all draw from the same base model catalog, but availability is decided per model: managed jobs by method (SFT, DPO, RFT), Training API jobs by parameter mode (LoRA or full-parameter).

## Model availability

Pick a model to see the surfaces and methods it is enabled for, plus any training shapes that back it. Switch to **All models** for the full matrix.

<ModelsCatalog />

## Vision and multimodal support

Vision support is model- and surface-specific. Use the catalog above to confirm that the selected VLM has a compatible managed method or Training API shape before preparing data.

* Managed VLM SFT dataset schema and launch flow: [Supervised Fine-Tuning: Vision](/fine-tuning/fine-tuning-models#vision-training)
* Training API VLM loops: start from a VLM-compatible shape and the same cookbook SFT, DPO, or RL recipe used for text, replacing the text tokenizer with the model processor
* Inference request formats after deployment: [Vision-language models](/guides/querying-vision-language-models)

## Next steps

<CardGroup cols={2}>
  <Card title="Managed Training" href="/fine-tuning/managed-finetuning-intro" icon="wand-magic-sparkles">
    Hand Fireworks your data and let the platform run the job
  </Card>

  <Card title="Training API" href="/fine-tuning/training-api/introduction" icon="code">
    Write your own training loop against a Tinker-compatible API
  </Card>

  <Card title="Serverless Training" href="/fine-tuning/training-api/serverless" icon="bolt">
    Train on shared pooled infrastructure with per-token billing
  </Card>

  <Card title="Training Shapes" href="/fine-tuning/training-api/training-shapes" icon="microchip">
    What a shape pins and how to reference one
  </Card>

  <Card title="Dedicated Training" href="/fine-tuning/training-api/dedicated" icon="server">
    Provision a trainer and sampler on reserved GPU capacity
  </Card>

  <Card title="Pricing" href="https://fireworks.ai/pricing" icon="tag">
    Current rates across training and inference
  </Card>
</CardGroup>
