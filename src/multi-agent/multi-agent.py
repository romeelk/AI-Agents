from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import asyncio
import os

from  DeploymentPlugin import DeploymentPlugin
async def main():
    try:
        creds = DefaultAzureCredential()
        async with (
            AzureAIAgent.create_client(credential=creds) as client,
        ):
            azure_code_ai_agent = await client.agents.create_agent(
                model=AzureAIAgentSettings().model_deployment_name,
                name="code-agent",
                instructions="""You are an AI Agent that can generate Python code.
                For this context you generate simple API server snippets using pythons fast api.
                """,
            )
            print(f"Successfully created AI agent code agent {azure_code_ai_agent.name}")

            sk_code_agent = AzureAIAgent(
                client=client,
                definition=azure_code_ai_agent,
                )
            print(f"Created semantic kernel agent {sk_code_agent.name}")

            azure_deployment_agent = await client.agents.create_agent(
                model=AzureAIAgentSettings().model_deployment_name,
                name="deployment-agent",
                instructions="""You are a bespoke deployment agent that takes python code, uses" 
                                the plugin DeploymentPlugin to package and deploy the code """
            )

            sk_deployment_agent = AzureAIAgent(
            client=client,
            definition=azure_deployment_agent,
            )

            print(f"Created semantic kernel agent {sk_deployment_agent.name}")
            
            python_code = """print('Hello')"""
            deployment_plugin = DeploymentPlugin()
            code_package_path = deployment_plugin.package_code(python_code)
            deployment_plugin.deploy_code(code_package_path)
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

