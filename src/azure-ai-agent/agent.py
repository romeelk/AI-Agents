from pathlib import Path
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FilePurpose, CodeInterpreterTool, AgentThread, MessageRole
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv
import os
import traceback

def agent():
    load_dotenv()
    project_endpoint= os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # Create a new agent instance
    agent_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )

    # Get current directory
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_path, "energy.txt")
    # Upload energy.txt

    # Upload the data file and create a CodeInterpreterTool
    file = agent_client.files.upload_and_poll(
        file_path=file_path, purpose=FilePurpose.AGENTS
    )
    print(f"Uploaded {file.filename}")

    code_interpreter_tool = CodeInterpreterTool(file_ids=[file.id])

    with agent_client:

        agent = agent_client.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="my-agent",
            instructions="You are helpful agent who can analyze files and produce charts. Use the uploaded file energy.txt",
            tools = code_interpreter_tool.definitions,
            tool_resources=code_interpreter_tool.resources,
        )

        print(f"Started agent {model_deployment}")

        thread = agent_client.threads.create()

        
        while True:
            prompt = input("Ask me a question (type q to exit): ")

            if prompt.lower() == "q":
                print("Quitting chat")
                break
            
            # Send a prompt to the agent
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

        save_generated_images(agent_client,thread)
      
def print_conversation_history(agent:AgentsClient, thread:AgentThread):
    """_summary_

    Args:
        agent (AgentsClient): Agent client
        thread (AgentThread): Agent thread
    """
    messages = agent.messages.list(thread_id=thread.id)

    for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]

            print(f"{message.role}: {last_msg.text.value}\n")
            
def save_generated_images(agent:AgentsClient, thread:AgentThread):
    """ Save generated images from the agent's messages.

    Args:
        agent (AgentsClient): _description_
        thread (AgentThread): _description_
    """
    messages = agent.messages.list(thread_id=thread.id)

    path_to_save = os.path.join(Path.cwd(),"outputs")
    for message in messages:
        for image in message.image_contents:
            file_name = os.path.join(path_to_save,f"{image.image_file.file_id}_image.png")
            agent.files.save(image.image_file.file_id, file_name,path_to_save)
            print(f"Saved image file to: {Path.cwd() / file_name}")



if __name__ == "__main__":
    # Create and run the agent

    try:
        ai_agent = agent()
    except Exception as e:
        print(f"Error creating agent at line {e.__traceback__.tb_lineno}: {traceback.format_exc()}")
