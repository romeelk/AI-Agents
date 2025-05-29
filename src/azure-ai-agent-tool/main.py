from random import randint
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import MessageRole, FunctionTool, ToolSet
from azure.identity import DefaultAzureCredential

def create_user_story(description: str) -> str:
    """
    Simulates creating a user story in a app like Jira or ADO

    :param description: A description of the user story
    :return: Story information with JSON string.
    """
    story_id = randint(1,100)

    story = {
        "id": story_id,
        "description": description,
        "created": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    return json.dumps(story)

user_functions = {create_user_story}

def read_instructions():
    print(f"Current path {Path.cwd()}")
    instructions_path = os.path.join(Path.cwd(), "instructions.txt")

    with open(instructions_path) as f:
        print(f.read())
    
def agent():
    read_instructions()
    # load_dotenv()
    # project_endpoint= os.getenv("PROJECT_ENDPOINT")
    # model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

   
    # # Create a new agent instance
    # agent_client = AgentsClient(
    #     endpoint=project_endpoint,
    #     credential=DefaultAzureCredential(
    #         exclude_environment_credential=True,
    #         exclude_managed_identity_credential=True
    #     ),
    # )
 
    # with agent_client:

    #     functions = FunctionTool(functions=user_functions)
    #     toolset = ToolSet()
    #     toolset.add(functions)

    #     # Enables automatically calling of agent tool by Agent sdk
    #     agent_client.enable_auto_function_calls(toolset)

    #     agent = agent_client.create_agent(
    #         model=os.environ["MODEL_DEPLOYMENT_NAME"],
    #         name="user-story-agent",
    #         instructions="You are helpful agent who can help create user stories. You are provided a tool called create_user_story",
    #         toolset=toolset

    #     print(f"Started agent {model_deployment} with agent id {agent.id}")

    #     thread = agent_client.threads.create()

    #     print(f"Created thread id {thread.id}")
        
    #     while True:
    #         prompt = input("Ask me a question (type q to exit): ")

    #         if prompt.lower() == "q":
    #             print("Quitting chat")
    #             break
            
    #         # Send a prompt to the agent
    #         message = agent_client.messages.create(
    #             thread_id=thread.id,
    #             role="user",
    #             content=prompt,
    #             )
            
    #         run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
            
    #         last_msg = agent_client.messages.get_last_message_text_by_role(
    #                 thread_id=thread.id,
    #                 role=MessageRole.AGENT)
        

    #         print(f"Model response: {last_msg.text.value}")
    #         if run.status == "failed":
    #             print(f"Run failed: {run.last_error}")

if __name__ == "__main__":
    #print(create_user_story("Bug fix to backend"))
    agent()