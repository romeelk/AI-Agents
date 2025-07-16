from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AgentGroupChat
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import asyncio
import os

from  deployment_plugin import DeploymentPlugin
import agent_constants
from selection_strategy import SelectionStrategy
async def main():
    try:
        creds = DefaultAzureCredential()
        async with (
            AzureAIAgent.create_client(credential=creds) as client,
        ):
            azure_code_ai_agent = await client.agents.create_agent(
                model=AzureAIAgentSettings().model_deployment_name,
                name=agent_constants.CODE_AGENT,
                instructions="""You are an AI Agent that can generate Python code.
                For this context you generate simple API server snippets {code_snippet} using pythons fast api.
                RULES:
                - Use the instructions provided.
                - If you are asked to create non flask api or fast api code snippet reply: Please request a server snippet
                - Prepend your response with this text: "CODE_ASSISTANT > 
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
                name=agent_constants.DEPLOYMENT_AGENT,
                instructions="""You are a bespoke deployment agent that takes python code, uses" 
                                the plugin DeploymentPlugin to package and deploy the code.

                                Use the following functions from DeploymentPlugin:
                                - package_code - take the output of the CODE_AGENT {code_snippet} pass it as parameter {pythoncode}
                                - deploy_package take the file path returned from package_code and deploy 
                                RULES:
                                - Use the instructions provided.
                                - Prepend your response with this text: "DEPLOYMENT_ASSISTANT > """)

            sk_deployment_agent = AzureAIAgent(
            client=client,
            definition=azure_deployment_agent,
            plugins=[DeploymentPlugin()]
            )

            print(f"Created semantic kernel agent {sk_deployment_agent.name}")
            
            # create an agent group chat

            # Create chat with participating agents
            chat = AgentGroupChat(agents=[sk_code_agent, sk_deployment_agent],selection_strategy=SelectionStrategy(agents=[sk_code_agent,sk_deployment_agent]))
            user_prompt = input("Ask the agent:")
            await chat.add_chat_message(user_prompt)
            async for response in chat.invoke():
                if response is None or not response.name:
                    continue
            print(f"{response.content}")
            # python_code = """print('Hello')"""
            # deployment_plugin = DeploymentPlugin()
            # code_package_path = deployment_plugin.package_code(python_code)
            # deployment_plugin.deploy_code(code_package_path)
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

