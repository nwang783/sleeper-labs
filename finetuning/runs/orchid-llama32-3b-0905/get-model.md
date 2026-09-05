> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireworks.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Model



## OpenAPI

````yaml get /v1/accounts/{account_id}/models/{model_id}
openapi: 3.1.0
info:
  title: Gateway REST API
  version: 5.10.0
servers:
  - url: https://api.fireworks.ai
security:
  - BearerAuth: []
tags:
  - name: AccountService
  - name: DeploymentService
  - name: Gateway
  - name: ModelService
  - name: TrainingService
paths:
  /v1/accounts/{account_id}/models/{model_id}:
    get:
      tags:
        - Gateway
      summary: Get Model
      operationId: Gateway_GetModel
      parameters:
        - name: readMask
          description: >-
            The fields to be returned in the response. If empty or "*", all
            fields will be returned.
          in: query
          required: false
          schema:
            type: string
        - name: account_id
          in: path
          required: true
          description: The Account Id
          schema:
            type: string
        - name: model_id
          in: path
          required: true
          description: The Model Id
          schema:
            type: string
      responses:
        '200':
          description: A successful response.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gatewayModel'
components:
  schemas:
    gatewayModel:
      type: object
      properties:
        name:
          type: string
          title: >-
            The resource name of the model. e.g.
            accounts/my-account/models/my-model
          readOnly: true
        displayName:
          type: string
          description: |-
            Human-readable display name of the model. e.g. "My Model"
            Must be fewer than 64 characters long.
        description:
          type: string
          description: >-
            The description of the model. Must be fewer than 1000 characters
            long.
        createTime:
          type: string
          format: date-time
          description: The creation time of the model.
          readOnly: true
        state:
          $ref: '#/components/schemas/gatewayModelState'
          description: The state of the model.
          readOnly: true
        status:
          $ref: '#/components/schemas/gatewayStatus'
          description: Contains detailed message when the last model operation fails.
          readOnly: true
        kind:
          $ref: '#/components/schemas/ModelKind'
          description: |-
            The kind of model.
            If not specified, the default is HF_PEFT_ADDON.
        githubUrl:
          type: string
          description: The URL to GitHub repository of the model.
        huggingFaceUrl:
          type: string
          description: The URL to the Hugging Face model.
        baseModelDetails:
          $ref: '#/components/schemas/gatewayBaseModelDetails'
          description: |-
            Base model details.
            Required if kind is HF_BASE_MODEL. Must not be set otherwise.
        peftDetails:
          $ref: '#/components/schemas/gatewayPEFTDetails'
          description: |-
            PEFT addon details.
            Required if kind is HF_PEFT_ADDON or HF_TEFT_ADDON.
        teftDetails:
          $ref: '#/components/schemas/gatewayTEFTDetails'
          description: |-
            TEFT addon details.
            Required if kind is HF_TEFT_ADDON. Must not be set otherwise.
        public:
          type: boolean
          description: If true, the model will be publicly readable.
        conversationConfig:
          $ref: '#/components/schemas/gatewayConversationConfig'
          description: If set, the Chat Completions API will be enabled for this model.
        contextLength:
          type: integer
          format: int32
          description: The maximum context length supported by the model.
        supportsImageInput:
          type: boolean
          description: If set, images can be provided as input to the model.
        supportsTools:
          type: boolean
          description: >-
            If set, tools (i.e. functions) can be provided as input to the
            model,

            and the model may respond with one or more tool calls.
        importedFrom:
          type: string
          description: >-
            The name of the the model from which this was imported. This field
            is empty

            if the model was not imported.
          readOnly: true
        fineTuningJob:
          type: string
          description: >-
            If the model was created from a fine-tuning job, this is the
            fine-tuning

            job name.
          readOnly: true
        defaultDraftModel:
          type: string
          description: |-
            The default draft model to use when creating a deployment. If empty,
            speculative decoding is disabled by default.
        defaultDraftTokenCount:
          type: integer
          format: int32
          description: |-
            The default draft token count to use when creating a deployment.
            Must be specified if default_draft_model is specified.
        deployedModelRefs:
          type: array
          items:
            $ref: '#/components/schemas/gatewayDeployedModelRef'
            type: object
          description: Populated from GetModel API call only.
          readOnly: true
        cluster:
          type: string
          description: |-
            The resource name of the BYOC cluster to which this model belongs.
            e.g. accounts/my-account/clusters/my-cluster. Empty if it belongs to
            a Fireworks cluster.
          readOnly: true
        deprecationDate:
          $ref: '#/components/schemas/typeDate'
          description: >-
            If specified, this is the date when the serverless deployment of the
            model will be taken down.
        calibrated:
          type: boolean
          description: >-
            If true, the model is calibrated and can be deployed to non-FP16
            precisions.
          readOnly: true
        tunable:
          type: boolean
          description: >-
            Deprecated: V1 training stack only — LoRA only, limited architecture
            support.

            If the model has use_training_v2=true, use supervised_lora_tunable
            and

            supervised_full_parameter_tunable instead.
          readOnly: true
        supportsLora:
          type: boolean
          description: Whether this model supports LoRA.
        useHfApplyChatTemplate:
          type: boolean
          description: >-
            If true, the model will use the Hugging Face apply_chat_template API
            to apply the chat template.
        updateTime:
          type: string
          format: date-time
          description: The update time for the model.
          readOnly: true
        defaultSamplingParams:
          type: object
          additionalProperties:
            type: number
            format: float
          description: >-
            A json object that contains the default sampling parameters for the
            model.
          readOnly: true
        rlTunable:
          type: boolean
          description: >-
            Deprecated: V1 training stack only — LoRA only, limited architecture
            support.

            If the model has use_training_v2=true, use rl_lora_tunable and

            rl_full_parameter_tunable instead.
          readOnly: true
        trainingContextLength:
          type: integer
          format: int32
          description: The maximum context length supported by the model.
        snapshotType:
          $ref: '#/components/schemas/ModelSnapshotType'
        supportsServerless:
          type: boolean
          description: If true, the model has a serverless deployment.
          readOnly: true
        useTrainingV2:
          type: boolean
          description: >-
            If true, SFT jobs for this base model use service-mode (StatefulSet
            +

            orchestration sidecar) instead of the legacy batch Job path.
        supervisedLoraTunable:
          type: boolean
          description: >-
            V2 only. Whether the model supports LoRA supervised fine-tuning and
            DPO (lora_rank > 0).

            True when a validated LORA_TRAINER training shape exists.
          readOnly: true
        supervisedFullParameterTunable:
          type: boolean
          description: >-
            V2 only. Whether the model supports full-parameter supervised
            fine-tuning and DPO (lora_rank = 0).

            True when a validated POLICY_TRAINER training shape exists.
          readOnly: true
        rlLoraTunable:
          type: boolean
          description: >-
            V2 only. Whether the model supports LoRA reinforcement learning
            (lora_rank > 0).

            True when a validated LORA_TRAINER training shape exists plus a
            deployment shape.
          readOnly: true
        rlFullParameterTunable:
          type: boolean
          description: >-
            V2 only. Whether the model supports full-parameter reinforcement
            learning (lora_rank = 0).

            True when validated POLICY_TRAINER + LORA_TRAINER training shapes
            exist plus a deployment shape.
          readOnly: true
        encryptionState:
          $ref: '#/components/schemas/gatewayEncryptionState'
          description: CMEK encryption state (authoritative, stamped at creation).
          readOnly: true
        serverlessModes:
          type: array
          items:
            $ref: '#/components/schemas/gatewayServerlessMode'
            type: object
          description: >-
            The serverless modes this base model is available on — the
            serverless read

            shape. Populated on read (e.g. the serverless catalog read path);
            one entry

            per serving mode. Empty for non-serverless models.
          readOnly: true
    gatewayModelState:
      type: string
      enum:
        - STATE_UNSPECIFIED
        - UPLOADING
        - READY
      default: STATE_UNSPECIFIED
      description: |-
        - UPLOADING: The model is still being uploaded (upload is asynchronous).
         - READY: The model is ready to be used.
    gatewayStatus:
      type: object
      properties:
        code:
          $ref: '#/components/schemas/gatewayCode'
          description: The status code.
        message:
          type: string
          description: A developer-facing error message in English.
      title: >-
        Mimics
        [https://github.com/googleapis/googleapis/blob/master/google/rpc/status.proto]
    ModelKind:
      type: string
      enum:
        - KIND_UNSPECIFIED
        - HF_BASE_MODEL
        - HF_PEFT_ADDON
        - HF_TEFT_ADDON
        - FLUMINA_BASE_MODEL
        - FLUMINA_ADDON
        - DRAFT_ADDON
        - LIVE_MERGE
        - CUSTOM_MODEL
        - EMBEDDING_MODEL
        - SNAPSHOT_MODEL
      default: KIND_UNSPECIFIED
      description: |-
        - HF_BASE_MODEL: An LLM base model.
         - HF_PEFT_ADDON: A parameter-efficent fine-tuned addon.
         - HF_TEFT_ADDON: A token-eficient fine-tuned addon.
         - FLUMINA_BASE_MODEL: A Flumina base model.
         - FLUMINA_ADDON: A Flumina addon.
         - DRAFT_ADDON: A draft model used for speculative decoding in a deployment.
         - LIVE_MERGE: A live-merge model.
         - CUSTOM_MODEL: A customized model
         - EMBEDDING_MODEL: An Embedding model.
         - SNAPSHOT_MODEL: A snapshot model.
    gatewayBaseModelDetails:
      type: object
      properties:
        worldSize:
          type: integer
          format: int32
          description: |-
            The default number of GPUs the model is served with.
            If not specified, the default is 1.
        checkpointFormat:
          $ref: '#/components/schemas/BaseModelDetailsCheckpointFormat'
        huggingfaceFiles:
          type: array
          items:
            type: string
          description: >-
            A list of Hugging Face files associated with this model. Specified
            if and only if

            the checkpoint_format is HUGGINGFACE.
        parameterCount:
          type: string
          format: int64
          description: >-
            The number of model parameters. For serverless models, this
            determines the

            price per token.
        moe:
          type: boolean
          description: >-
            If true, this is a Mixture of Experts (MoE) model. For serverless
            models,

            this affects the price per token.
        tunable:
          type: boolean
          description: >-
            Deprecated: V1 training stack only. Use per-category tunable flags
            on Model instead.
        modelType:
          type: string
          description: The type of the model.
        supportsFireattention:
          type: boolean
          description: Whether this model supports fireattention.
        defaultPrecision:
          $ref: '#/components/schemas/DeploymentPrecision'
          description: Default precision of the model.
          readOnly: true
        supportsMtp:
          type: boolean
          description: If true, this model supports MTP.
    gatewayPEFTDetails:
      type: object
      properties:
        baseModel:
          type: string
          title: The base model name. e.g. accounts/fireworks/models/falcon-7b
        r:
          type: integer
          format: int32
          description: |-
            The rank of the update matrices.
            Must be between 4 and 64, inclusive.
        targetModules:
          type: array
          items:
            type: string
          title: >-
            This is the target modules for an adapter that we extract from

            for more information what target module means, check out

            https://huggingface.co/docs/peft/conceptual_guides/lora#common-lora-parameters-in-peft
        baseModelType:
          type: string
          description: The type of the model.
          readOnly: true
        mergeAddonModelName:
          type: string
          title: >-
            The resource name of the model to merge with base model, e.g
            accounts/fireworks/models/falcon-7b-lora
      title: PEFT addon details.
      required:
        - baseModel
        - r
        - targetModules
    gatewayTEFTDetails:
      type: object
    gatewayConversationConfig:
      type: object
      properties:
        style:
          type: string
          description: The chat template to use.
        system:
          type: string
          description: The system prompt (if the chat style supports it).
        template:
          type: string
          description: The Jinja template (if style is "jinja").
      required:
        - style
    gatewayDeployedModelRef:
      type: object
      properties:
        name:
          type: string
          title: >-
            The resource name. e.g.
            accounts/my-account/deployedModels/my-deployed-model
          readOnly: true
        deployment:
          type: string
          description: The resource name of the base deployment the model is deployed to.
          readOnly: true
        state:
          $ref: '#/components/schemas/gatewayDeployedModelState'
          description: The state of the deployed model.
          readOnly: true
        default:
          type: boolean
          description: >-
            If true, this is the default target when querying this model without

            the `#<deployment>` suffix.

            The first deployment a model is deployed to will have this field set
            to

            true automatically.
          readOnly: true
        public:
          type: boolean
          description: If true, the deployed model will be publicly reachable.
          readOnly: true
    typeDate:
      type: object
      properties:
        year:
          type: integer
          format: int32
          description: >-
            Year of the date. Must be from 1 to 9999, or 0 to specify a date
            without

            a year.
        month:
          type: integer
          format: int32
          description: >-
            Month of a year. Must be from 1 to 12, or 0 to specify a year
            without a

            month and day.
        day:
          type: integer
          format: int32
          description: >-
            Day of a month. Must be from 1 to 31 and valid for the year and
            month, or 0

            to specify a year by itself or a year and month where the day isn't

            significant.
      description: >-
        * A full date, with non-zero year, month, and day values

        * A month and day value, with a zero year, such as an anniversary

        * A year on its own, with zero month and day values

        * A year and month value, with a zero day, such as a credit card
        expiration

        date


        Related types are [google.type.TimeOfDay][google.type.TimeOfDay] and

        `google.protobuf.Timestamp`.
      title: >-
        Represents a whole or partial calendar date, such as a birthday. The
        time of

        day and time zone are either specified elsewhere or are insignificant.
        The

        date is relative to the Gregorian Calendar. This can represent one of
        the

        following:
    ModelSnapshotType:
      type: string
      enum:
        - FULL_SNAPSHOT
        - INCREMENTAL_SNAPSHOT
      default: FULL_SNAPSHOT
    gatewayEncryptionState:
      type: string
      enum:
        - ENCRYPTION_STATE_UNSPECIFIED
        - ENCRYPTION_STATE_PLAINTEXT
        - ENCRYPTION_STATE_CMEK
      default: ENCRYPTION_STATE_UNSPECIFIED
      description: >-
        EncryptionState is the authoritative, per-resource CMEK marker: the
        single

        source of truth for whether a resource's customer-data artifacts are

        encrypted. It is stamped at resource creation from the owning account's
        CMEK

        config and is immutable for the resource's life, so a resource always
        reads

        back with the state it was created under regardless of the account's
        current

        flag. The encrypt-on-write / decrypt-on-read decision for the resource's

        data keys off this field.

         - ENCRYPTION_STATE_UNSPECIFIED: Unstamped/legacy rows that predate CMEK. Treated as PLAINTEXT.
         - ENCRYPTION_STATE_PLAINTEXT: Customer-data artifacts are stored as plaintext (Fireworks-owned, no CMEK).
         - ENCRYPTION_STATE_CMEK: Customer-data artifacts are CMEK-encrypted; reads MUST decrypt (fail-closed).
    gatewayServerlessMode:
      type: object
      properties:
        name:
          type: string
          description: >-
            The resource name, e.g.

            accounts/fireworks/models/kimi-k2p6/serverlessModes/fast.

            {AccountId} must be a serverless account (fireworks, ...);

            {ModelId} is the base model's id; {ServerlessModeId} is the mode
            name

            (default | priority | fast | spot).
          readOnly: true
        usageIdentifier:
          type: string
          description: >-
            Invocation recipe: the value to pass as "model" in inference
            requests.

            Empty means use the base model id. May reference a DIFFERENT
            resource

            than the base model — a model OR a router, e.g.

            accounts/fireworks/routers/kimi-k2p6-fast for fast.
        serviceTier:
          type: string
          description: >-
            Invocation recipe: the service_tier request-body flag layered on top
            of the

            model id (e.g. "priority"). Only the priority mode sets this today.
        skuInfos:
          type: array
          items:
            $ref: '#/components/schemas/gatewaySKUInfo'
            type: object
          description: >-
            Per-path token pricing, sourced live from Orb on the read path.
            Reuses the

            same SKUInfo type as Model.sku_infos (e.g. "LLM input tokens
            (uncached)",

            "LLM input tokens (cached)", "LLM output tokens"; google.type.Money
            at

            unit="1M tokens"). Resolved per tier (DEFAULT/PRIORITY/FAST/...).
            Empty on

            the stored config; only populated by ListServerlessModels.


            (api_only) keeps this derived field out of the database entirely
            (like

            Model.sku_infos): it is never persisted by the admin write path and
            never

            read back from storage, only computed live at read time.
          readOnly: true
        useCases:
          type: array
          items:
            type: string
          description: Curated use-case tags driving discovery filters (e.g. "coding").
        updatedBy:
          type: string
          description: The user who last mutated this mode (audit).
          readOnly: true
        createTime:
          type: string
          format: date-time
          readOnly: true
        updateTime:
          type: string
          format: date-time
          readOnly: true
      description: >-
        ServerlessMode is one way a serverless base model can be invoked —
        standard

        serverless (default), Priority, Fast, or Spot — together with the
        invocation

        recipe customers must use for it.


        It is a child resource of the base Model: the {ServerlessModeId} segment
        of

        the resource name IS the mode name (default | priority | fast | spot).
        The

        base model is the linking key for all of its serving modes, even when a
        mode

        is served through a different resource (a Fast router, a Spot
        deployment).


        Modes split into two classes:
          - Alternate-resource modes (usage_identifier set) — e.g. fast resolves to a
            router, spot to the spot deployment's own model id.
          - Flag modes (service_tier set) — e.g. priority uses the base model id plus
            a request-body service_tier flag.

        Pricing is sourced live from Orb (keyed by the resolved model name /
        tier),

        so no price is stored on the mode.
    gatewayCode:
      type: string
      enum:
        - OK
        - CANCELLED
        - UNKNOWN
        - INVALID_ARGUMENT
        - DEADLINE_EXCEEDED
        - NOT_FOUND
        - ALREADY_EXISTS
        - PERMISSION_DENIED
        - UNAUTHENTICATED
        - RESOURCE_EXHAUSTED
        - FAILED_PRECONDITION
        - ABORTED
        - OUT_OF_RANGE
        - UNIMPLEMENTED
        - INTERNAL
        - UNAVAILABLE
        - DATA_LOSS
      default: OK
      description: |-
        - OK: Not an error; returned on success.

        HTTP Mapping: 200 OK
         - CANCELLED: The operation was cancelled, typically by the caller.

        HTTP Mapping: 499 Client Closed Request
         - UNKNOWN: Unknown error.  For example, this error may be returned when
        a `Status` value received from another address space belongs to
        an error space that is not known in this address space.  Also
        errors raised by APIs that do not return enough error information
        may be converted to this error.

        HTTP Mapping: 500 Internal Server Error
         - INVALID_ARGUMENT: The client specified an invalid argument.  Note that this differs
        from `FAILED_PRECONDITION`.  `INVALID_ARGUMENT` indicates arguments
        that are problematic regardless of the state of the system
        (e.g., a malformed file name).

        HTTP Mapping: 400 Bad Request
         - DEADLINE_EXCEEDED: The deadline expired before the operation could complete. For operations
        that change the state of the system, this error may be returned
        even if the operation has completed successfully.  For example, a
        successful response from a server could have been delayed long
        enough for the deadline to expire.

        HTTP Mapping: 504 Gateway Timeout
         - NOT_FOUND: Some requested entity (e.g., file or directory) was not found.

        Note to server developers: if a request is denied for an entire class
        of users, such as gradual feature rollout or undocumented allowlist,
        `NOT_FOUND` may be used. If a request is denied for some users within
        a class of users, such as user-based access control, `PERMISSION_DENIED`
        must be used.

        HTTP Mapping: 404 Not Found
         - ALREADY_EXISTS: The entity that a client attempted to create (e.g., file or directory)
        already exists.

        HTTP Mapping: 409 Conflict
         - PERMISSION_DENIED: The caller does not have permission to execute the specified
        operation. `PERMISSION_DENIED` must not be used for rejections
        caused by exhausting some resource (use `RESOURCE_EXHAUSTED`
        instead for those errors). `PERMISSION_DENIED` must not be
        used if the caller can not be identified (use `UNAUTHENTICATED`
        instead for those errors). This error code does not imply the
        request is valid or the requested entity exists or satisfies
        other pre-conditions.

        HTTP Mapping: 403 Forbidden
         - UNAUTHENTICATED: The request does not have valid authentication credentials for the
        operation.

        HTTP Mapping: 401 Unauthorized
         - RESOURCE_EXHAUSTED: Some resource has been exhausted, perhaps a per-user quota, or
        perhaps the entire file system is out of space.

        HTTP Mapping: 429 Too Many Requests
         - FAILED_PRECONDITION: The operation was rejected because the system is not in a state
        required for the operation's execution.  For example, the directory
        to be deleted is non-empty, an rmdir operation is applied to
        a non-directory, etc.

        Service implementors can use the following guidelines to decide
        between `FAILED_PRECONDITION`, `ABORTED`, and `UNAVAILABLE`:
         (a) Use `UNAVAILABLE` if the client can retry just the failing call.
         (b) Use `ABORTED` if the client should retry at a higher level. For
             example, when a client-specified test-and-set fails, indicating the
             client should restart a read-modify-write sequence.
         (c) Use `FAILED_PRECONDITION` if the client should not retry until
             the system state has been explicitly fixed. For example, if an "rmdir"
             fails because the directory is non-empty, `FAILED_PRECONDITION`
             should be returned since the client should not retry unless
             the files are deleted from the directory.

        HTTP Mapping: 400 Bad Request
         - ABORTED: The operation was aborted, typically due to a concurrency issue such as
        a sequencer check failure or transaction abort.

        See the guidelines above for deciding between `FAILED_PRECONDITION`,
        `ABORTED`, and `UNAVAILABLE`.

        HTTP Mapping: 409 Conflict
         - OUT_OF_RANGE: The operation was attempted past the valid range.  E.g., seeking or
        reading past end-of-file.

        Unlike `INVALID_ARGUMENT`, this error indicates a problem that may
        be fixed if the system state changes. For example, a 32-bit file
        system will generate `INVALID_ARGUMENT` if asked to read at an
        offset that is not in the range [0,2^32-1], but it will generate
        `OUT_OF_RANGE` if asked to read from an offset past the current
        file size.

        There is a fair bit of overlap between `FAILED_PRECONDITION` and
        `OUT_OF_RANGE`.  We recommend using `OUT_OF_RANGE` (the more specific
        error) when it applies so that callers who are iterating through
        a space can easily look for an `OUT_OF_RANGE` error to detect when
        they are done.

        HTTP Mapping: 400 Bad Request
         - UNIMPLEMENTED: The operation is not implemented or is not supported/enabled in this
        service.

        HTTP Mapping: 501 Not Implemented
         - INTERNAL: Internal errors.  This means that some invariants expected by the
        underlying system have been broken.  This error code is reserved
        for serious errors.

        HTTP Mapping: 500 Internal Server Error
         - UNAVAILABLE: The service is currently unavailable.  This is most likely a
        transient condition, which can be corrected by retrying with
        a backoff. Note that it is not always safe to retry
        non-idempotent operations.

        See the guidelines above for deciding between `FAILED_PRECONDITION`,
        `ABORTED`, and `UNAVAILABLE`.

        HTTP Mapping: 503 Service Unavailable
         - DATA_LOSS: Unrecoverable data loss or corruption.

        HTTP Mapping: 500 Internal Server Error
      title: >-
        Mimics
        [https://github.com/googleapis/googleapis/blob/master/google/rpc/code.proto]
    BaseModelDetailsCheckpointFormat:
      type: string
      enum:
        - CHECKPOINT_FORMAT_UNSPECIFIED
        - NATIVE
        - HUGGINGFACE
        - UNINITIALIZED
      default: CHECKPOINT_FORMAT_UNSPECIFIED
    DeploymentPrecision:
      type: string
      enum:
        - PRECISION_UNSPECIFIED
        - FP16
        - FP8
        - FP8_MM
        - FP8_AR
        - FP8_MM_KV_ATTN
        - FP8_KV
        - FP8_MM_V2
        - FP8_V2
        - FP8_MM_KV_ATTN_V2
        - NF4
        - FP4
        - BF16
        - FP4_BLOCKSCALED_MM
        - FP4_MX_MOE
      default: PRECISION_UNSPECIFIED
      title: >-
        - PRECISION_UNSPECIFIED: if left unspecified we will treat this as a
        legacy model created before

        self serve
    gatewayDeployedModelState:
      type: string
      enum:
        - STATE_UNSPECIFIED
        - UNDEPLOYING
        - DEPLOYING
        - DEPLOYED
        - UPDATING
      default: STATE_UNSPECIFIED
      description: |-
        - UNDEPLOYING: The model is being undeployed.
         - DEPLOYING: The model is being deployed.
         - DEPLOYED: The model is deployed and ready for inference.
         - UPDATING: there are updates happening with the deployed model
    gatewaySKUInfo:
      type: object
      properties:
        sku:
          type: string
        amount:
          $ref: '#/components/schemas/typeMoney'
        unit:
          type: string
          title: |-
            e.g.
            1M tokens, hour
    typeMoney:
      type: object
      properties:
        currencyCode:
          type: string
          description: The three-letter currency code defined in ISO 4217.
        units:
          type: string
          format: int64
          description: >-
            The whole units of the amount.

            For example if `currencyCode` is `"USD"`, then 1 unit is one US
            dollar.
        nanos:
          type: integer
          format: int32
          description: >-
            Number of nano (10^-9) units of the amount.

            The value must be between -999,999,999 and +999,999,999 inclusive.

            If `units` is positive, `nanos` must be positive or zero.

            If `units` is zero, `nanos` can be positive, zero, or negative.

            If `units` is negative, `nanos` must be negative or zero.

            For example $-1.75 is represented as `units`=-1 and
            `nanos`=-750,000,000.
      description: Represents an amount of money with its currency type.
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: >-
        Bearer authentication using your Fireworks API key. Format: Bearer
        <API_KEY>
      bearerFormat: API_KEY

````