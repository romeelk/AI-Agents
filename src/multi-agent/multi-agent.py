from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AgentGroupChat
from semantic_kernel.contents import ChatMessageContent, AuthorRole
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import asyncio
import os

import logging
from  deployment_plugin import DeploymentPlugin
import agent_constants
from selection_strategy import SelectionStrategy, SequentialSelectionStrategy
from approval_strategy import ApprovalTerminationStrategy

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
                For this context you generate simple API server snippets using pythons fast api.

                RULES:
                - Use the instructions provided.
                - If you are asked to create non flask api or fast api code snippet reply: Please request a server snippet.
                """,
            )
            print(f"Successfully created AI agent code agent {azure_code_ai_agent.name}")

            sk_code_agent = AzureAIAgent(
                client=client,
                definition=azure_code_ai_agent,
                plugins=[DeploymentPlugin()]
                )
            print(f"Created semantic kernel agent {sk_code_agent.name}")

            azure_deployment_agent = await client.agents.create_agent(
                model=AzureAIAgentSettings().model_deployment_name,
                name=agent_constants.DEPLOYMENT_AGENT,
                instructions="""You are a bespoke deployment agent that takes python code, uses
                                the plugin DeploymentPlugin to package and deploy the code.
                                
                                package code {pythoncode}
                                RULES:
                                - Use the instructions provided.
                                - Prepend your response with this text: "DEPLOYMENT_ASSISTANT > """)

            sk_deployment_agent = AzureAIAgent(
            client=client,
            definition=azure_deployment_agent,
            plugins=[DeploymentPlugin(),sk_code_agent]
            )

            print(f"Created semantic kernel agent {sk_deployment_agent.name}")
            
            # create an agent group chat

            # Create chat with participating agents
            chat = AgentGroupChat(agents=[sk_code_agent, sk_deployment_agent],
                                  selection_strategy=SelectionStrategy(agents=[sk_code_agent,sk_deployment_agent]),
                                  termination_strategy=ApprovalTerminationStrategy(agents=[sk_deployment_agent], 
                                                                        maximum_iterations=1, 
                                                                        automatic_reset=True))
            user_prompt = input("Ask the agent:")

            chat_message = ChatMessageContent(role=AuthorRole.USER, content=user_prompt)

            await chat.add_chat_message(message=chat_message)
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

