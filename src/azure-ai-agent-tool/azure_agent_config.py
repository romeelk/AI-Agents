from azure.identity import DefaultAzureCredential

class AzureAgentConfig:
    def __init__(self,project_endpoint,model_deployment,agent_credential:DefaultAzureCredential):
        self.project_endpoint = project_endpoint
        self.model_deployment = model_deployment    
        self.agent_credential = agent_credential