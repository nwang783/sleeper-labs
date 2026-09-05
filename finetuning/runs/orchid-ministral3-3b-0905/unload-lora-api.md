> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fireworks.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Unload LoRA



## OpenAPI

````yaml delete /v1/accounts/{account_id}/deployedModels/{deployed_model_id}
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
  /v1/accounts/{account_id}/deployedModels/{deployed_model_id}:
    delete:
      tags:
        - Gateway
      summary: Unload LoRA
      operationId: Gateway_DeleteDeployedModel
      parameters:
        - name: account_id
          in: path
          required: true
          description: The Account Id
          schema:
            type: string
        - name: deployed_model_id
          in: path
          required: true
          description: The Deployed Model Id
          schema:
            type: string
      responses:
        '200':
          description: A successful response.
          content:
            application/json:
              schema:
                type: object
                properties: {}
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: >-
        Bearer authentication using your Fireworks API key. Format: Bearer
        <API_KEY>
      bearerFormat: API_KEY

````