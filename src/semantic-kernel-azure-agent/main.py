from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import asyncio
from  email_plugin import EmailPlugin
import os


async def process_expenses(expense_agent: AzureAIAgent, prompt:str, expenses:str,project_client:AIProjectClient):
    # create a thread conversation
    thread: AzureAIAgentThread = AzureAIAgentThread(client=project_client)
    try:
        print("About to process expenses")
        prompt_messages = [f"{prompt}: {expenses}"]
        # invoke the agent 
        agent_response =  await expense_agent.get_response(thread_id=thread.id,messages=prompt_messages)

        print(f"Agent response:{agent_response}")
        print(f'Expense e-mail sent')
    except Exception as e:
        print(e)
    finally:
        print("Clearing thread and expense agent session")
        await thread.delete()
        await project_client.agents.delete_agent(expense_agent.id)


async def main():
    try:
        creds = DefaultAzureCredential()
        async with (
            AzureAIAgent.create_client(credential=creds) as client,
        ):
            azure_ai_agent_def = await client.agents.create_agent(
                model=AzureAIAgentSettings().model_deployment_name,
                name="sk-agent",
                instructions="""You are an AI Agent that can handle expense claims. 
                When a user submits a expense claim make use of the send_expense_email plug-in function
                to send an e-mail to expenses@acme.com. The e-mail subject should contain Expense
                claim for <user> where user is the user submitting the claim. The body of the 
                e-mail message should contain the itemised expense.
                """,
            )
            print(f"Successfully created AI agent definition {azure_ai_agent_def.name}")

            sk_expenses_agent = AzureAIAgent(
                client=client,
                definition=azure_ai_agent_def,
                plugins=[EmailPlugin()]
                )
            print(f"Created semantic kernel agent {sk_expenses_agent.name}")

            # Build the full path to the expense file in the current script directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            expense_file = input("Please enter name of expense file: ")
            expense_file_path = os.path.join(script_dir, expense_file)

            if not os.path.exists(expense_file_path):
                print("Could not find expense file. Cannot continue.. exiting")
                return
            
            user_prompt = input(f"Here is the expenses data in your file:\n\n{expense_file_path}\n\nWhat would you like me to do with it?\n\n")
            
            itemised_expsenses = None
            with open(expense_file_path) as f:
                itemised_expsenses = f.read()
            
            # Call process expenses
            await process_expenses(expense_agent=sk_expenses_agent,prompt=user_prompt,expenses=itemised_expsenses,project_client=client)
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

