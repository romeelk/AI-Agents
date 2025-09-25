from azure.ai.agents import AgentsClient

class AzureAgent:
  def __init__(self):
    agent_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        ),
    )