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

def read_instructions():
    print(f"Current path {Path.cwd()}")
    instructions_path = os.path.join(Path.cwd(), "instructions.txt")
    with open(instructions_path) as f:
        print(f.read())

def agent():
    agent_instructions = read_instructions()
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
     
        functions = FunctionTool(functions=user_functions)
        toolset = ToolSet()
        toolset.add(functions)
        agent_client.enable_auto_function_calls(toolset)
        agent = agent_client.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="user-story-agent",
            instructions=""""You are a user story  agent.
                        When a user has a user story to create, you get their user story name  and a description of the issue.
                        Then you use those values to submit a user story ticket using the function available to you.
                        You return the created user story as json.
                     """,
            toolset=toolset)
        print(f"Started agent {model_deployment} with agent id {agent.id}")
        thread = agent_client.threads.create()
        print(f"Created thread id {thread.id}")
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
        print("Deleting thread")
        agent_client.threads.delete(thread.id)
        print("Deleting agent")
        agent_client.delete_agent(agent.id)

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    agent()
