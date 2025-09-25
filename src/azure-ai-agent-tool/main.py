from random import randint
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import MessageRole, FunctionTool, ToolSet
from azure.identity import DefaultAzureCredential
import logging
from user_functions import user_functions

def read_instructions()->str:
    print(f"Current path {Path.cwd()}")
    instructions_path = os.path.join(Path.cwd(), "instructions.txt")
    with open(instructions_path) as f:
        return f.read()

def agent():
    agent_instructions = read_instructions().strip()
    load_dotenv()
    project_endpoint= os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")
    agent_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        ),
    )
    with agent_client:
     
        toolset = setup_agent_tools(agent_client)
        agent, thread = create_azure_ai_agent(agent_instructions, model_deployment, agent_client, toolset)
        
        start_agent_chat(agent_client, agent, thread)

        dispose_agent(agent_client, agent, thread)

def dispose_agent(agent_client, agent, thread):
    print("Deleting thread")
    agent_client.threads.delete(thread.id)
    print("Deleting agent")
    agent_client.delete_agent(agent.id)

def start_agent_chat(agent_client, agent, thread):
    while True:
        prompt = input("Ask me a question (type q to exit): ")
        if prompt.lower() == "q":
            print("Quitting chat")
            break
        message = agent_client.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt,
                )
        run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
        last_msg = agent_client.messages.get_last_message_text_by_role(
                    thread_id=thread.id,
                    role=MessageRole.AGENT)
        print(f"Model response: {last_msg.text.value}")
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")

def create_azure_ai_agent(agent_instructions, model_deployment, agent_client, toolset):
    agent = agent_client.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="user-story-agent",
            instructions=agent_instructions,
            toolset=toolset)
    print(f"Started agent {model_deployment} with agent id {agent.id}")
    thread = agent_client.threads.create()
    print(f"Created thread id {thread.id}")
     
    return agent,thread

def setup_agent_tools(agent_client):
    functions = FunctionTool(functions=user_functions)
    toolset = ToolSet()
    toolset.add(functions)
    agent_client.enable_auto_function_calls(toolset)
    return toolset

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    agent()
