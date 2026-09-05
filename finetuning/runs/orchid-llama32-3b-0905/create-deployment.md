> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireworks.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Create Deployment

## Creating a deployment with a deployment shape

[Deployment shapes](/guides/ondemand-deployments#deployment-shapes) are pre-configured templates optimized for speed, cost, or efficiency. To create a deployment with a specific shape, pass the `deploymentShape` field in the request body along with `baseModel`.

Use the [List Deployment Shape Versions](/api-reference/list-deployment-shape-versions) endpoint to find available shapes for your model.

```bash theme={null}
curl -X POST "https://api.fireworks.ai/v1/accounts/YOUR_ACCOUNT_ID/deployments" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "baseModel": "accounts/fireworks/models/gpt-oss-120b",
    "deploymentShape": "accounts/fireworks/deploymentShapes/gpt-oss-120b-minimal",
    "minReplicaCount": 0,
    "maxReplicaCount": 1
  }'
```

<Note>
  When using a deployment shape, you do not need to specify `activeModelVersion` or `targetModelVersion` — the shape provides the necessary configuration.
</Note>


## OpenAPI

````yaml post /v1/accounts/{account_id}/deployments
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
  /v1/accounts/{account_id}/deployments:
    post:
      tags:
        - Gateway
      summary: Create Deployment
      operationId: Gateway_CreateDeployment
      parameters:
        - name: disableAutoDeploy
          description: >-
            By default, a deployment created with a currently undeployed base
            model

            will be deployed to this deployment. If true, this auto-deploy
            function

            is disabled.
          in: query
          required: false
          schema:
            type: boolean
        - name: disableSpeculativeDecoding
          description: >-
            By default, a deployment will use the speculative decoding settings
            from

            the base model. If true, this will disable speculative decoding.
          in: query
          required: false
          schema:
            type: boolean
        - name: deploymentId
          description: >-
            The ID of the deployment. If not specified, a random ID will be
            generated.
          in: query
          required: false
          schema:
            type: string
        - name: validateOnly
          description: >-
            If true, this will not create the deployment, but will return the
            deployment

            that would be created.
          in: query
          required: false
          schema:
            type: boolean
        - name: skipShapeValidation
          description: >-
            By default, a deployment will ensure the deployment shape provided
            is validated.

            If true, we will not require the deployment shape to be validated.
          in: query
          required: false
          schema:
            type: boolean
        - name: skipImageTagValidation
          description: >-
            If true, skip the image tag policy validation that blocks certain
            image tags.

            This allows creating deployments with image tags that would
            otherwise be blocked.
          in: query
          required: false
          schema:
            type: boolean
        - name: account_id
          in: path
          required: true
          description: The Account Id
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/gatewayDeployment'
        description: The properties of the deployment being created.
        required: true
      responses:
        '200':
          description: A successful response.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/gatewayDeployment'
components:
  schemas:
    gatewayDeployment:
      type: object
      properties:
        name:
          type: string
          title: >-
            The resource name of the deployment. e.g.
            accounts/my-account/deployments/my-deployment
          readOnly: true
        displayName:
          type: string
          description: |-
            Human-readable display name of the deployment. e.g. "My Deployment"
            Must be fewer than 64 characters long.
        description:
          type: string
          description: Description of the deployment.
        createTime:
          type: string
          format: date-time
          description: The creation time of the deployment.
          readOnly: true
        expireTime:
          type: string
          format: date-time
          description: >-
            Deprecated: This field is deprecated and no longer causes
            auto-deletion.

            The time at which this deployment will automatically be deleted.
        purgeTime:
          type: string
          format: date-time
          description: The time at which the resource will be hard deleted.
          readOnly: true
        deleteTime:
          type: string
          format: date-time
          description: The time at which the resource will be soft deleted.
          readOnly: true
        state:
          $ref: '#/components/schemas/gatewayDeploymentState'
          description: The state of the deployment.
          readOnly: true
        status:
          $ref: '#/components/schemas/gatewayStatus'
          description: Detailed status information regarding the most recent operation.
          readOnly: true
        annotations:
          type: object
          additionalProperties:
            type: string
          description: >-
            Annotations to identify deployment properties.

            Key/value pairs may be used by external tools or other services.

            The "image-tag-reason" key is redacted from API responses for
            non-superuser principals.
        minReplicaCount:
          type: integer
          format: int32
          description: |-
            The minimum number of replicas.
            If not specified, the default is 0.
        maxReplicaCount:
          type: integer
          format: int32
          description: |-
            The maximum number of replicas.
            If not specified, the default is max(min_replica_count, 1).
            May be set to 0 to downscale the deployment to 0.
        maxWithRevocableReplicaCount:
          type: integer
          format: int32
          description: >-
            max_with_revocable_replica_count is max replica count including
            revocable capacity.

            The max revocable capacity will be max_with_revocable_replica_count
            - max_replica_count.
        desiredReplicaCount:
          type: integer
          format: int32
          description: >-
            The desired number of replicas for this deployment. This represents
            the target

            replica count that the system is trying to achieve.
          readOnly: true
        replicaCount:
          type: integer
          format: int32
          readOnly: true
        autoscalingPolicy:
          $ref: '#/components/schemas/gatewayAutoscalingPolicy'
        baseModel:
          type: string
          title: The base model name. e.g. accounts/fireworks/models/falcon-7b
        acceleratorCount:
          type: integer
          format: int32
          description: >-
            The number of accelerators used per replica.

            If not specified, the default is the estimated minimum required by
            the

            base model.
        acceleratorType:
          $ref: '#/components/schemas/gatewayAcceleratorType'
          description: The type of accelerator to use.
        precision:
          $ref: '#/components/schemas/DeploymentPrecision'
          description: The precision with which the model should be served.
        maxConcurrencyPerReplica:
          type: integer
          format: int32
          description: >-
            The maximum number of concurrent (in-flight) requests a single
            replica

            will accept before shedding load. Requests that arrive while a
            replica is

            already at this limit are rejected early with HTTP 429 instead of

            queueing — a per-replica admission gate for controlling tail
            latency.

            When unset (0), the platform default is used.
        cluster:
          type: string
          description: If set, this deployment is deployed to a cloud-premise cluster.
          readOnly: true
        enableAddons:
          type: boolean
          description: If true, PEFT addons are enabled for this deployment.
        draftTokenCount:
          type: integer
          format: int32
          description: >-
            The number of candidate tokens to generate per step for speculative

            decoding.

            Default is the base model's draft_token_count. Set

            CreateDeploymentRequest.disable_speculative_decoding to false to
            disable

            this behavior.
        draftModel:
          type: string
          description: >-
            The draft model name for speculative decoding. e.g.
            accounts/fireworks/models/my-draft-model

            If empty, speculative decoding using a draft model is disabled.

            Default is the base model's default_draft_model. Set

            CreateDeploymentRequest.disable_speculative_decoding to false to
            disable

            this behavior.
        ngramSpeculationLength:
          type: integer
          format: int32
          description: >-
            The length of previous input sequence to be considered for N-gram
            speculation.
        enableSessionAffinity:
          type: boolean
          description: |-
            Whether to apply sticky routing based on `user` field.
            Serverless will be set to true when creating deployment.
        directRouteApiKeys:
          type: array
          items:
            type: string
          description: >-
            The set of API keys used to access the direct route deployment. If
            direct routing is not enabled, this field is unused.
        numPeftDeviceCached:
          type: integer
          format: int32
          title: How many peft adapters to keep on gpu side for caching
        directRouteType:
          $ref: '#/components/schemas/gatewayDirectRouteType'
          description: >-
            If set, this deployment will expose an endpoint that bypasses the
            Fireworks API gateway.
        directRouteHandle:
          type: string
          description: >-
            The handle for calling a direct route. The meaning of the handle
            depends on the

            direct route type of the deployment:
               INTERNET                    -> The host name for accessing the deployment
               GCP_PRIVATE_SERVICE_CONNECT -> The service attachment name used to create the PSC endpoint.
               AWS_PRIVATELINK             -> The service name used to create the VPC endpoint.
          readOnly: true
        deploymentTemplate:
          type: string
          description: |-
            The name of the deployment template to use for this deployment. Only
            available to enterprise accounts.
        autoTune:
          $ref: '#/components/schemas/gatewayAutoTune'
          description: The performance profile to use for this deployment.
        placement:
          $ref: '#/components/schemas/gatewayPlacement'
          description: |-
            The desired geographic region where the deployment must be placed.
            If unspecified, the default is the GLOBAL multi-region.
        region:
          $ref: '#/components/schemas/gatewayRegion'
          description: >-
            The geographic region where the deployment is presently located.
            This region may change

            over time, but within the `placement` constraint.
          readOnly: true
        maxContextLength:
          type: integer
          format: int32
          description: >-
            The maximum context length supported by the model (context window).

            If set to 0 or not specified, the model's default maximum context
            length will be used.
        updateTime:
          type: string
          format: date-time
          description: The update time for the deployment.
          readOnly: true
        disableDeploymentSizeValidation:
          type: boolean
          description: Whether the deployment size validation is disabled.
        enableHotLoad:
          type: boolean
          description: Whether to use hot load for this deployment.
        hotLoadBucketType:
          $ref: '#/components/schemas/DeploymentHotLoadBucketType'
          title: >-
            hot load bucket name, indicate what type of storage to use for hot
            load
        enableHotReloadLatestAddon:
          type: boolean
          description: >-
            Allows up to 1 addon at a time to be loaded, and will merge it into
            the base model.
        deploymentShape:
          type: string
          description: >-
            The name of the deployment shape that this deployment is using.

            On the server side, this will be replaced with the deployment shape
            version name.
        activeModelVersion:
          type: string
          description: >-
            The model version that is currently active and applied to running
            replicas of a deployment.
        targetModelVersion:
          type: string
          description: >-
            The target model version that is being rolled out to the deployment.

            In a ready steady state, the target model version is the same as the
            active model version.
        replicaStats:
          $ref: '#/components/schemas/gatewayReplicaStats'
          description: >-
            Per-replica deployment status counters. Provides visibility into the
            deployment process

            by tracking replicas in different stages of the deployment
            lifecycle.
          readOnly: true
        hotLoadBucketUrl:
          type: string
          title: >-
            For hot load bucket location

            e.g for s3: s3://mybucket/<object_path>; for GCS:
            gs://mybucket/<object_path>, no trailing slash
        pricingPlanId:
          type: string
          description: |-
            Optional pricing plan ID for custom billing configuration.
            If set, this deployment will use the pricing plan's billing rules
            instead of default billing behavior.
        hotLoadTrainerJob:
          type: string
          title: >-
            Trainer job whose hot_load_bucket_url this deployment should use.

            At creation, the trainer's bucket URL is copied into this
            deployment's

            hot_load_bucket_url. The deployment continues working after the
            trainer

            is deleted (snapshot-at-creation semantics).

            Format: accounts/{account}/rlorTrainerJobs/{job}
        hotLoadTransitionType:
          $ref: '#/components/schemas/DeploymentHotLoadTransitionType'
          description: >-
            Controls hot-load reload semantics for this deployment.

            ASYNC (default when enable_hot_load is set) pauses the
            generator/prefiller

            mid-flight and skips draining in-flight requests during hot load.

            SYNC drains in-flight requests before applying the new model.
        preemptible:
          type: boolean
          description: When true, this deployment runs as preemptible.
      required:
        - baseModel
    gatewayDeploymentState:
      type: string
      enum:
        - STATE_UNSPECIFIED
        - CREATING
        - READY
        - DELETING
        - FAILED
        - UPDATING
        - DELETED
      default: STATE_UNSPECIFIED
      description: |-
        - CREATING: The deployment is still being created.
         - READY: The deployment is ready to be used.
         - DELETING: The deployment is being deleted.
         - FAILED: The deployment failed to be created. See the `status` field for
        additional details on why it failed.
         - UPDATING: There are in-progress updates happening with the deployment.
         - DELETED: The deployment is soft-deleted.
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
    gatewayAutoscalingPolicy:
      type: object
      properties:
        scaleUpWindow:
          type: string
          description: >-
            The duration the autoscaler will wait before scaling up a deployment
            after observing

            increased load. Default is 30s. Must be less than or equal to 1
            hour.
        scaleDownWindow:
          type: string
          description: >-
            The duration the autoscaler will wait before scaling down a
            deployment after observing

            decreased load. Default is 10m. Must be less than or equal to 1
            hour.
        scaleToZeroWindow:
          type: string
          description: >-
            The duration after which there are no requests that the deployment
            will be scaled down

            to zero replicas, if min_replica_count==0. Default is 1h.

            This must be at least 5 minutes.
        loadTargets:
          type: object
          additionalProperties:
            type: number
            format: float
          title: >-
            Map of load metric names to their target utilization factors.

            Currently only the "default" key is supported, which specifies the
            default target for all metrics.

            If not specified, the default target is 0.8
        scalingSchedules:
          type: object
          additionalProperties:
            $ref: '#/components/schemas/gatewayScalingSchedule'
          description: >-
            Named scaling schedules that override min_replica_count on a
            time-based cron schedule.

            When multiple schedules are active simultaneously, the highest
            min_replica_count

            across all active schedules is used ("max wins"). When no schedule
            is active, the

            deployment's base min_replica_count applies.

            Maximum 5 schedules per deployment.
    gatewayAcceleratorType:
      type: string
      enum:
        - ACCELERATOR_TYPE_UNSPECIFIED
        - NVIDIA_A100_80GB
        - NVIDIA_H100_80GB
        - AMD_MI300X_192GB
        - NVIDIA_A10G_24GB
        - NVIDIA_A100_40GB
        - NVIDIA_L4_24GB
        - NVIDIA_H200_141GB
        - NVIDIA_B200_180GB
        - AMD_MI325X_256GB
        - AMD_MI350X_288GB
        - NVIDIA_B300_288GB
        - NVIDIA_GB200
        - NVIDIA_GB300
      default: ACCELERATOR_TYPE_UNSPECIFIED
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
    gatewayDirectRouteType:
      type: string
      enum:
        - DIRECT_ROUTE_TYPE_UNSPECIFIED
        - INTERNET
        - GCP_PRIVATE_SERVICE_CONNECT
        - AWS_PRIVATELINK
      default: DIRECT_ROUTE_TYPE_UNSPECIFIED
      title: |-
        - DIRECT_ROUTE_TYPE_UNSPECIFIED: No direct routing
         - INTERNET: The direct route is exposed via the public internet
         - GCP_PRIVATE_SERVICE_CONNECT: The direct route is exposed via GCP Private Service Connect
         - AWS_PRIVATELINK: The direct route is exposed via AWS PrivateLink
    gatewayAutoTune:
      type: object
      properties:
        longPrompt:
          type: boolean
          description: If true, this deployment is optimized for long prompt lengths.
    gatewayPlacement:
      type: object
      properties:
        region:
          $ref: '#/components/schemas/gatewayRegion'
          description: The region where the deployment must be placed.
        multiRegion:
          $ref: '#/components/schemas/gatewayMultiRegion'
          description: The multi-region where the deployment must be placed.
        regions:
          type: array
          items:
            $ref: '#/components/schemas/gatewayRegion'
          title: The list of regions where the deployment must be placed
      description: >-
        The desired geographic region where the deployment must be placed.
        Exactly one field will be

        specified.
    gatewayRegion:
      type: string
      enum:
        - REGION_UNSPECIFIED
        - US_IOWA_1
        - US_VIRGINIA_1
        - US_VIRGINIA_2
        - US_ILLINOIS_1
        - AP_TOKYO_1
        - US_ARIZONA_1
        - US_TEXAS_1
        - US_ILLINOIS_2
        - EU_FRANKFURT_1
        - US_TEXAS_2
        - EU_ICELAND_1
        - EU_ICELAND_2
        - US_WASHINGTON_1
        - US_WASHINGTON_2
        - US_WASHINGTON_3
        - AP_TOKYO_2
        - US_CALIFORNIA_1
        - US_UTAH_1
        - US_ARIZONA_3
        - US_GEORGIA_1
        - US_GEORGIA_2
        - US_WASHINGTON_4
        - US_GEORGIA_3
        - NA_BRITISHCOLUMBIA_1
        - US_GEORGIA_4
        - US_OHIO_1
        - US_NEWYORK_1
        - EU_NETHERLANDS_1
        - US_WASHINGTON_5
        - US_MINNESOTA_1
        - US_CALIFORNIA_2
        - NA_BRITISHCOLUMBIA_2
        - AP_MALAYSIA_2
        - US_OREGON_1
        - NA_BRITISHCOLUMBIA_3
        - AP_NEWSOUTHWALES_1
        - AP_TAIWAN_1
      default: REGION_UNSPECIFIED
    DeploymentHotLoadBucketType:
      type: string
      enum:
        - BUCKET_TYPE_UNSPECIFIED
        - MINIO
        - S3
        - NEBIUS
        - FW_HOSTED
      default: BUCKET_TYPE_UNSPECIFIED
      title: '- FW_HOSTED: Fireworks hosted bucket'
    gatewayReplicaStats:
      type: object
      properties:
        pendingSchedulingReplicaCount:
          type: integer
          format: int32
          description: Number of replicas waiting to be scheduled to a node.
          readOnly: true
        downloadingModelReplicaCount:
          type: integer
          format: int32
          description: Number of replicas downloading model weights.
          readOnly: true
        initializingReplicaCount:
          type: integer
          format: int32
          description: Number of replicas initializing the model server.
          readOnly: true
        readyReplicaCount:
          type: integer
          format: int32
          description: Number of replicas that are ready and serving traffic.
          readOnly: true
        revocableReplicaCount:
          type: integer
          format: int32
          title: The number of replicas that can be revoked
          readOnly: true
        effectiveReplicaCount:
          type: number
          format: float
          description: >-
            The effective number of replicas currently serving traffic,
            including

            fractional progress toward a replica that is not yet fully ready.
            Equals

            ready_replica_count when no replica is partially ready.
          readOnly: true
    DeploymentHotLoadTransitionType:
      type: string
      enum:
        - HOT_LOAD_TRANSITION_TYPE_UNSPECIFIED
        - ASYNC
        - SYNC
      default: HOT_LOAD_TRANSITION_TYPE_UNSPECIFIED
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
    gatewayScalingSchedule:
      type: object
      properties:
        minReplicaCount:
          type: integer
          format: int32
          description: >-
            Minimum number of replicas guaranteed when this schedule is active.

            When multiple schedules overlap, the effective minimum is the
            highest

            min_replica_count across all active schedules ("max wins").

            Must be >= 0 and <= the deployment's max_replica_count.
        schedule:
          type: string
          description: >-
            Cron expression defining when this schedule's window starts.

            Standard 5-field cron format: minute hour day-of-month month
            day-of-week.

            Examples: "0 8 * * Mon-Fri" (8am weekdays), "0 0 1 * *" (midnight on
            1st of month).
        duration:
          type: string
          description: >-
            Duration that the schedule remains active after the cron trigger.

            Must be between 300 seconds (5 minutes) and 604,800 seconds (7
            days),

            and use whole-second precision. Schedules needing longer windows
            should

            raise the deployment's base min_replica_count instead.

            Example: "36000s" = 10 hours (e.g., 8am to 6pm).
        timezone:
          type: string
          description: >-
            IANA timezone for the cron expression. e.g., "America/New_York",
            "Europe/London", "UTC".

            Required because cron expressions without a timezone are ambiguous.

            DST transitions are handled automatically.
        description:
          type: string
          description: |-
            Human-readable description of the schedule.
            e.g., "Weekday business hours", "Wednesday peak load".
        disabled:
          type: boolean
          description: >-
            If true, this schedule is temporarily disabled without being
            deleted.

            Useful for holidays or temporary schedule changes.
      title: >-
        A time-based scaling schedule that sets a minimum replica floor during a
        recurring window.

        Follows the GCP MIG scaling schedule pattern: cron start time +
        duration.
      required:
        - minReplicaCount
        - schedule
        - duration
        - timezone
    gatewayMultiRegion:
      type: string
      enum:
        - MULTI_REGION_UNSPECIFIED
        - GLOBAL
        - US
        - EUROPE
        - APAC
      default: MULTI_REGION_UNSPECIFIED
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: >-
        Bearer authentication using your Fireworks API key. Format: Bearer
        <API_KEY>
      bearerFormat: API_KEY

````