import asyncio
import os
from dotenv import load_dotenv
from agent_instructions import ORCHESTRATOR_INSTRUCTIONS
from agent_instructions import ORCHESTRATOR_NAME
from agent_instructions import WEB_SURFER_INSTRUCTIONS
from agent_instructions import WEB_SURFER_AGENT_NAME
from agent_instructions import YAHOO_FINANCE_INSTRUCTIONS
from agent_instructions import YAHOO_FINANCE_AGENT_NAME
from agent_instructions import SEC_AGENT_INSTRUCTIONS
from agent_instructions import SEC_AGENT_NAME
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel
from yahoo_plugin import YahooPlugin  # Import the YahooPlugin
from web_plugin import SurferPlugin  # Import the SurferPlugin
from sec_plugin import SecPlugin  # Import the SecPlugin




async def main():
    # Create the instance of the Kernel
    kernel = Kernel()
    load_dotenv(".env")

    credentials = os.getenv("OPENAI_API_KEY")

    # Add web surfer agent
    
    web_surfer_service_id = "web_surfer_agent"
    kernel.add_service(OpenAIChatCompletion(service_id=web_surfer_service_id, api_key=credentials))

    web_surfer_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=web_surfer_service_id)
    web_surfer_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    kernel.add_plugin(SurferPlugin(), plugin_name="web_surfer")

    web_surfer_agent = ChatCompletionAgent(
        service_id=web_surfer_service_id, kernel=kernel, name=WEB_SURFER_AGENT_NAME, instructions=WEB_SURFER_INSTRUCTIONS, execution_settings=web_surfer_settings
    )

    # Add yahoo finance agent
    yahoo_finance_service_id = "yahoo_finance_agent"
    kernel.add_service(OpenAIChatCompletion(service_id=yahoo_finance_service_id, api_key=credentials))

    yahoo_finance_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=yahoo_finance_service_id)
    yahoo_finance_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    kernel.add_plugin(YahooPlugin(), plugin_name="yahoo_finance")

    yahoo_finance_agent = ChatCompletionAgent(
        service_id=yahoo_finance_service_id, kernel=kernel, name=YAHOO_FINANCE_AGENT_NAME, instructions=YAHOO_FINANCE_INSTRUCTIONS, execution_settings=yahoo_finance_settings
    )

    # Add SEC agent
    sec_service_id = "sec_agent"
    kernel.add_service(OpenAIChatCompletion(service_id=sec_service_id, api_key=credentials))

    sec_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=sec_service_id)
    sec_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    kernel.add_plugin(SecPlugin(), plugin_name="sec")

    sec_agent = ChatCompletionAgent(
        service_id=sec_service_id, kernel=kernel, name=SEC_AGENT_NAME, instructions=SEC_AGENT_INSTRUCTIONS, execution_settings=sec_settings
    )

    # Define the chat history
    chat = ChatHistory()



    '''
    Orchestrator -> 
    '''
    ##we will start with invoking the orchestrator agent first 
    orchestrator_service_id = "orchestrator_agent"
    kernel.add_service(OpenAIChatCompletion(service_id=orchestrator_service_id, api_key=credentials))
    orchestrator_agent = ChatCompletionAgent(
        service_id=orchestrator_service_id, kernel=kernel, name=ORCHESTRATOR_NAME, instructions=ORCHESTRATOR_INSTRUCTIONS)




    ##Now we have to create the logic for this agentic execution 

    #await invoke_agent(orchestrator_agent, "I want to short Apple, give me details on whether it is a good decision or not? Give me an indepth dive", chat)




    # Respond to user input with web surfer agent
    #await invoke_agent(web_surfer_agent, "Latest news about Apple Inc. that is relevant to investment decisions.", chat)

    # Respond to user input with yahoo finance agent
    #await invoke_agent(yahoo_finance_agent, "Apple Inc", chat)

    # Respond to user input with SEC agent
    await invoke_agent(sec_agent, "Apple Inc", chat)




# A helper method to invoke the agent with the user input
async def invoke_agent(agent: ChatCompletionAgent, input: str, chat: ChatHistory) -> None:
    """Invoke the agent with the user input."""
    chat.add_user_message(input)

    print(f"# {AuthorRole.USER}: '{input}'")

    async for content in agent.invoke(chat):
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
    chat.add_message(content)

if __name__ == "__main__":
    asyncio.run(main())


