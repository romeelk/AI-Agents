from file_plugin import FilePlugin
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AgentGroupChat
from semantic_kernel.contents import ChatMessageContent, AuthorRole
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import asyncio
import os
# file_plugin = FilePlugin()
# file = file_plugin.create_prompt_file("bakwas")
# file_plugin.export_file_topdf(file)

async def main():   
    creds = DefaultAzureCredential()
    async with (
            AzureAIAgent.create_client(credential=creds) as client,
        ):
    
        azure_file_ai_agent = await client.agents.create_agent(
                model=AzureAIAgentSettings().model_deployment_name,
                name="fileagent",
                instructions="""You are an AI File Agent that can generate text files based on user requests

                RULES:
                - Use the instructions provided.
                - If you are asked to create a file in another format from pdf. Politely tell the user you can't
                """,
            )
        sk_azure_file_agent  = AzureAIAgent(
            client=client,
            definition=azure_file_ai_agent,
            plugins=[FilePlugin()]
            )

       
        print("about to send message to agent")
        async for response in  sk_azure_file_agent.invoke("Tell me in three lines about london. And call the function create_prompt_file. Export the txt file as pdf as well"):
            print(response.content)

        await  client.agents.delete_agent(sk_azure_file_agent.id)
        

if __name__ == "__main__":
    asyncio.run(main())
