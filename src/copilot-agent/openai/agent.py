import asyncio
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, AgentGroupChat
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.agents.selection import KernelFunctionSelectionStrategy
from semantic_kernel.agents.termination import KernelFunctionTerminationStrategy
from semantic_kernel.functions import KernelFunctionFromPrompt
from code_plugin import CodePackagingPlugin
async def main():
    kernel = Kernel()
    kernel.add_chat_service("openai", OpenAIChatCompletion())
    settings = OpenAIChatPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Register plugin
    kernel.add_plugin(CodePackagingPlugin(), plugin_name="CodePack")

    # Define agents
    packer = ChatCompletionAgent(
        kernel=kernel,
        name="packer",
        instructions="Receive user request with Python code. Call generate_zip(python_code) and return JSON."
    )
    deployer = ChatCompletionAgent(
        kernel=kernel,
        name="deployer",
        arguments={"settings": settings},
        instructions="When you receive JSON with zipPath, call deploy_zip(zipPath) and respond JSON with result."
    )

    # Define selection & termination logic
    selection_fn = KernelFunctionFromPrompt(
        function_name="select_agent",
        prompt="""
You are the director deciding which agent runs next.
Next JSON input: {{$input}}
Return only "packer" or "deployer" based on presence of "python_code" or "zipPath".
"""
    )
    termination_fn = KernelFunctionFromPrompt(
        function_name="check_termination",
        prompt="""
Check the JSON input: {{$input}}.
If it contains a field "result", return "DONE", else return "CONTINUE".
"""
    )

    chat = AgentGroupChat(
        agents=[packer, deployer],
        selection_strategy=KernelFunctionSelectionStrategy(
            initial_agent=packer,
            function=selection_fn,
            kernel=kernel,
            result_parser=lambda x: x.strip()
        ),
        termination_strategy=KernelFunctionTerminationStrategy(
            function=termination_fn,
            kernel=kernel,
            result_parser=lambda x: x.strip() == "DONE"
        )
    )

    # Start pipeline
    user_python = 'print("Hello from SK Python agents!")'
    response = await chat.send_message_async(user_python)
    print("Final output:", response.content)

asyncio.run(main())