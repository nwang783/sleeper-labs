> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireworks.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# List Deployment Shapes Versions

Use this endpoint to query available deployment shape versions for a given model. Use `-` as a wildcard for both `account_id` and `deployment_shape_id` to search across all accounts and shapes.

## Example: List shapes for a model

To list validated deployment shapes for a specific model, use the `filter` parameter with `snapshot.base_model` and `latest_validated=true`:

```bash theme={null}
curl -s "https://api.fireworks.ai/v1/accounts/-/deploymentShapes/-/versions?filter=snapshot.base_model%3D%22accounts%2Ffireworks%2Fmodels%2Fgpt-oss-120b%22%20AND%20latest_validated%3Dtrue&order_by=create_time%20desc" \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" | jq .
```

### Filter syntax

The `filter` parameter uses [AIP-160 filtering](https://google.aip.dev/160). Common patterns:

| Filter                                                       | Description                                            |
| ------------------------------------------------------------ | ------------------------------------------------------ |
| `snapshot.base_model="accounts/fireworks/models/MODEL_NAME"` | Filter by base model                                   |
| `latest_validated=true`                                      | Only return the latest validated version of each shape |

Combine multiple conditions with `AND`:

```
snapshot.base_model="accounts/fireworks/models/MODEL_NAME" AND latest_validated=true
```

<Note>
  Remember to URL-encode the filter value when using curl directly. `=` becomes `%3D`, `"` becomes `%22`, and `/` becomes `%2F`.
</Note>


## OpenAPI

````yaml get /v1/accounts/{account_id}/deploymentShapes/{deployment_shape_id}/versions
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
  /v1/accounts/{account_id}/deploymentShapes/{deployment_shape_id}/versions:
    get:
      tags:
        - Gateway
      summary: List Deployment Shapes Versions
      operationId: Gateway_ListDeploymentShapeVersions
      parameters:
        - name: pageSize
          description: >-
            The maximum number of deployment shape versions to return. The
            maximum page_size is 200,

            values above 200 will be coerced to 200.

            If unspecified, the default is 50.
          in: query
          required: false
          schema:
            type: integer
            format: int32
        - name: pageToken
          description: >-
            A page token, received from a previous ListDeploymentShapeVersions
            call. Provide this

            to retrieve the subsequent page. When paginating, all other
            parameters

            provided to ListDeploymentShapeVersions must match the call that
            provided the page

            token.
          in: query
          required: false
          schema:
            type: string
        - name: filter
          description: >-
            Only deployment shape versions satisfying the provided filter (if
            specified) will be

            returned. See https://google.aip.dev/160 for the filter grammar.
          in: query
          required: false
          schema:
            type: string
        - name: orderBy
          description: >-
            A comma-separated list of fields to order by. e.g. "foo,bar"

            The default sort order is ascending. To specify a descending order
            for a

            field, append a " desc" suffix. e.g. "foo desc,bar"

            Subfields are specified with a "." character. e.g. "foo.bar"

            If not specified, the default order is by "create_time".
          in: query
          required: false
          schema:
            type: string
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
        - name: deployment_shape_id
          in: path
          required: true
          description: The Deployment Shape Id
          schema:
            type: string
      responses:
        '200':
          description: A successful response.
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/gatewayListDeploymentShapeVersionsResponse
components:
  schemas:
    gatewayListDeploymentShapeVersionsResponse:
      type: object
      properties:
        deploymentShapeVersions:
          type: array
          items:
            $ref: '#/components/schemas/gatewayDeploymentShapeVersion'
            type: object
        nextPageToken:
          type: string
          description: >-
            A token, which can be sent as `page_token` to retrieve the next
            page.

            If this field is omitted, there are no subsequent pages.
        totalSize:
          type: integer
          format: int32
          description: The total number of deployment shape versions.
    gatewayDeploymentShapeVersion:
      type: object
      properties:
        name:
          type: string
          title: >-
            The resource name of the deployment shape version. e.g.
            accounts/my-account/deploymentShapes/my-deployment-shape/versions/{version_id}
          readOnly: true
        createTime:
          type: string
          format: date-time
          description: >-
            The creation time of the deployment shape version. Lists will be
            ordered by this field.
          readOnly: true
        snapshot:
          $ref: '#/components/schemas/gatewayDeploymentShape'
          description: Full snapshot of the Deployment Shape at this version.
          readOnly: true
        validated:
          type: boolean
          description: If true, this version has been validated.
        public:
          type: boolean
          description: If true, this version will be publicly readable.
        latestValidated:
          type: boolean
          description: |-
            If true, this version is the latest validated version.
            Only one version of the shape can be the latest validated version.
          readOnly: true
        capabilities:
          type: array
          items:
            $ref: '#/components/schemas/DeploymentShapeVersionCapability'
          description: The capabilities supported by this deployment shape version.
      title: >-
        A deployment shape version is a specific version of a deployment shape.

        Versions are immutable, only created on updates and deleted when the
        deployment shape is deleted.
    gatewayDeploymentShape:
      type: object
      properties:
        name:
          type: string
          title: >-
            The resource name of the deployment shape. e.g.
            accounts/my-account/deploymentShapes/my-deployment-shape
          readOnly: true
        displayName:
          type: string
          description: >-
            Human-readable display name of the deployment shape. e.g. "My
            Deployment Shape"

            Must be fewer than 64 characters long.
        description:
          type: string
          description: >-
            The description of the deployment shape. Must be fewer than 1000
            characters long.
        createTime:
          type: string
          format: date-time
          description: The creation time of the deployment shape.
          readOnly: true
        updateTime:
          type: string
          format: date-time
          description: The update time for the deployment shape.
          readOnly: true
        baseModel:
          type: string
          description: >-
            Mutable, but only via UpdateDeploymentShape and only to a compatible
            model:

            one with the same model_type, parameter_count, and embedding status.
            The

            derived model_type / parameter_count fields (OUTPUT_ONLY, IMMUTABLE)
            are

            therefore preserved across a swap. Any incompatible change is
            rejected.
          title: The base model name. e.g. accounts/fireworks/models/falcon-7b
        modelType:
          type: string
          description: The model type of the base model.
          readOnly: true
        parameterCount:
          type: string
          format: int64
          description: The parameter count of the base model .
          readOnly: true
        acceleratorCount:
          type: integer
          format: int32
          description: >-
            The number of accelerators used per replica.

            If not specified, the default is the estimated minimum required by
            the base model.
        acceleratorType:
          $ref: '#/components/schemas/gatewayAcceleratorType'
          description: |-
            The type of accelerator to use.
            If not specified, the default is NVIDIA_A100_80GB.
        precision:
          $ref: '#/components/schemas/DeploymentPrecision'
          description: The precision with which the model should be served.
        disableDeploymentSizeValidation:
          type: boolean
          description: If true, the deployment size validation is disabled.
        enableAddons:
          type: boolean
          description: >-
            If true, LORA addons are enabled for deployments created from this
            shape.

            Deprecated: set enable_addons on the deployment instead.
        draftTokenCount:
          type: integer
          format: int32
          description: |-
            The number of candidate tokens to generate per step for speculative
            decoding.
            Default is the base model's draft_token_count.
        draftModel:
          type: string
          description: >-
            The draft model name for speculative decoding. e.g.
            accounts/fireworks/models/my-draft-model

            If empty, speculative decoding using a draft model is disabled.

            Default is the base model's default_draft_model.

            Deprecated: set default_draft_model on the base model instead.
        ngramSpeculationLength:
          type: integer
          format: int32
          description: >-
            The length of previous input sequence to be considered for N-gram
            speculation.
        disableSpeculativeDecoding:
          type: boolean
          description: >-
            DEPRECATED: This field is a no-op. Speculative decoding is
            configured on deployment.
        enableSessionAffinity:
          type: boolean
          description: Whether to apply sticky routing based on `user` field.
        numLoraDeviceCached:
          type: integer
          format: int32
          title: How many LORA adapters to keep on GPU side for caching
        maxContextLength:
          type: integer
          format: int32
          description: >-
            The maximum context length supported by the model (context window).

            If set to 0 or not specified, the model's default maximum context
            length will be used.
        presetType:
          $ref: '#/components/schemas/DeploymentShapePresetType'
          description: Type of deployment shape for different deployment configurations.
      title: >-
        A deployment shape is a set of parameters that define the shape of a
        deployment.

        Deployments are created from a deployment shape.
      required:
        - baseModel
    DeploymentShapeVersionCapability:
      type: string
      enum:
        - CAPABILITY_UNSPECIFIED
        - MULTI_LORA
      default: CAPABILITY_UNSPECIFIED
      description: A capability that a deployment shape version supports.
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
    DeploymentShapePresetType:
      type: string
      enum:
        - PRESET_TYPE_UNSPECIFIED
        - MINIMAL
        - FAST
        - THROUGHPUT
        - FULL_PRECISION
        - AGENTIC_CODING
        - CHAT
        - SUMMARIZATION
        - MULTI_LORA
      default: PRESET_TYPE_UNSPECIFIED
      title: |-
        - MINIMAL: Preset for cheapest & most minimal type of deployment
         - FAST: Preset for fastest generation & TTFT deployment
         - THROUGHPUT: Preset for best throughput deployment
         - FULL_PRECISION: Preset for deployment with full precision for training & most accurate numerics
         - AGENTIC_CODING: Preset for autonomous code generation and analysis for development workflows
         - CHAT: Preset for interactive conversational AI for customer engagement
         - SUMMARIZATION: Preset for efficient document and content summarization
         - MULTI_LORA: Preset for multi-LORA serving (deployments that can enable LORA addons)
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: >-
        Bearer authentication using your Fireworks API key. Format: Bearer
        <API_KEY>
      bearerFormat: API_KEY

````