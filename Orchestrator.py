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
from agent_instructions import PROSPECTUS_CREATOR_NAME
from agent_instructions import PROSPECTUS_CREATOR_INSTRUCTIONS
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel
from yahoo_plugin import YahooPlugin  # Import the YahooPlugin
from web_plugin import SurferPlugin  # Import the SurferPlugin
from sec_plugin import SecPlugin  # Import the SecPlugin
from propsectus_creator import ProspectusPlugin  # Import the ProspectusPlugin
import logging
import json
'''
Orchestrator -> web surfer (ticker extraction) and news extraction -> orchestrator -> yahoo finance -> orchestrator -> sec_filings
Orchestrator                                                                                                                <-|
We will let these interations happen maximum for 3 times. 
FOR THE FIRST ITERATION WE HAVE TO MAKE SURE WE EXECUTE THE WEB SURFER AGENT FIRST SO WE GET THE TICKER. 

'''
async def main():
    # Create the instance of the Kernel
    kernel = Kernel()
    load_dotenv(".env")
    chat = ChatHistory()
    credentials = os.getenv("OPENAI_API_KEY")
    orchestrator_service_id = "orchestrator_agent"
    kernel.add_service(OpenAIChatCompletion(service_id=orchestrator_service_id, api_key=credentials))
    orchestrator_agent = ChatCompletionAgent(
        service_id=orchestrator_service_id, kernel=kernel, name=ORCHESTRATOR_NAME, instructions=ORCHESTRATOR_INSTRUCTIONS)

    web_surfer_service_id = "web_surfer_agent"
    kernel.add_service(OpenAIChatCompletion(service_id=web_surfer_service_id, api_key=credentials, ai_model_id="gpt-4o"))

    web_surfer_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=web_surfer_service_id)
    web_surfer_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    kernel.add_plugin(SurferPlugin(), plugin_name="web_surfer")

    web_surfer_agent = ChatCompletionAgent(
        service_id=web_surfer_service_id, kernel=kernel, name=WEB_SURFER_AGENT_NAME, instructions=WEB_SURFER_INSTRUCTIONS, execution_settings=web_surfer_settings
    )
    yahoo_finance_service_id = "yahoo_finance_agent"
    kernel.add_service(OpenAIChatCompletion(service_id=yahoo_finance_service_id, api_key=credentials, ai_model_id="gpt-4o"))

    yahoo_finance_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=yahoo_finance_service_id)
    yahoo_finance_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    kernel.add_plugin(YahooPlugin(), plugin_name="yahoo_finance")

    yahoo_finance_agent = ChatCompletionAgent(
        service_id=yahoo_finance_service_id, kernel=kernel, name=YAHOO_FINANCE_AGENT_NAME, instructions=YAHOO_FINANCE_INSTRUCTIONS, execution_settings=yahoo_finance_settings
    )
    sec_service_id = "sec_agent"
    kernel.add_plugin(SecPlugin(), plugin_name="sec_plugin")
    kernel.add_service(OpenAIChatCompletion(service_id=sec_service_id, api_key=credentials, ai_model_id="gpt-4o"))

    sec_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=sec_service_id)
    sec_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    sec_agent = ChatCompletionAgent(
        service_id="sec_agent", kernel=kernel, name=SEC_AGENT_NAME, instructions=SEC_AGENT_INSTRUCTIONS, execution_settings=sec_settings
    )
    prospectus_agent_service_id = "prospectus_agent"
    kernel.add_plugin(SecPlugin(), plugin_name="prospectus_creator_plugin")
    kernel.add_service(OpenAIChatCompletion(service_id=prospectus_agent_service_id, api_key=credentials, ai_model_id="gpt-4o"))

    prospectus_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=prospectus_agent_service_id)
    prospectus_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    prospectus_agent = ChatCompletionAgent(
        service_id="sec_agent", kernel=kernel, name=PROSPECTUS_CREATOR_NAME, instructions=PROSPECTUS_CREATOR_INSTRUCTIONS, execution_settings=prospectus_settings
    )
    

    user_query = "Buying Apple Corporation shares because of it's recent news."


    # Add web surfer agent

    number_iterations = 0
    task_ledger = None
    while task_ledger is None:
        try:
            task_ledger = await invoke_agent(orchestrator_agent, user_query, chat)
        except:
            print("Error in orchestrator agent")
            await asyncio.sleep(2)
        
    agent_task_completed = False
    while number_iterations <= 8:
            if agent_task_completed:
                    task_ledger = await invoke_agent(orchestrator_agent, agent_reply, chat)
                    agent_task_completed = False
                    print(json.dumps(task_ledger,indent=4))
                    break


            agent_reply = ""
            
            if task_ledger.get("agent_to_execute") == "web_surfer_agent":
                try:
                    agent_reply = await invoke_agent(web_surfer_agent, task_ledger.get("details_needed"), chat)
                    agent_task_completed = True
                except:
                    print("Error in web surfer agent")
            elif task_ledger.get("agent_to_execute") == "yahoo_finance_agent":
                try:
                    agent_reply = await invoke_agent(yahoo_finance_agent, task_ledger.get("details_needed") + "   Stock Ticker    " +  task_ledger["stock_ticker"], chat)
                    agent_task_completed = True
                except:
                    print("Error in yahoo finance agent")
            elif task_ledger.get("agent_to_execute") == "sec_agent":
                try:
                    agent_reply = await invoke_agent(sec_agent, task_ledger.get("details_needed") + "   Stock Ticker    " +  task_ledger["stock_ticker"], chat)
                    agent_task_completed = True
                except:
                    print("Error in sec agent")
            elif task_ledger.get("agent_to_execute") == "prospectus_agent":
                try:
                    agent_reply = await invoke_agent(prospectus_agent, task_ledger.get("details_needed"), chat)
                    agent_task_completed = True
                except:
                    print("Error in prospectus agent")
            
            number_iterations += 1

            
            
                

            break
            
    



   
   
    #Add yahoo finance agent

  
    
    # Add SEC agent

    
   


   

    
    
   
    
    ##we will start with invoking the orchestrator agent first 
    



    ##Now we have to create the logic for this agentic execution 

    #a




    # Respond to user input with web surfer agent
    #await invoke_agent(web_surfer_agent, "Give me Micro Strategy's stock ticker. ", chat)
    # Respond to user input with yahoo finance agent
    #await invoke_agent(yahoo_finance_agent, "Give me the latest news and everything going on with Apple Inc right now? Some thing crucial. ", chat)

    # Respond to user input with SEC agent
     # Define the chat history
    #logging.basicConfig(level=logging.DEBUG)

    
    #await invoke_agent(sec_agent, "Give me the latest details about the filings regarding MicroStrategy. Give me an indepth review about it's bitcoin backed treasury. ", chat)




# A helper method to invoke the agent with the user input
async def invoke_agent(agent: ChatCompletionAgent, input: str, chat: ChatHistory) -> None:
    """Invoke the agent with the user input."""
    
    
    print(f"# {AuthorRole.USER}: '{input}'")
    
    async for content in agent.invoke(chat):
        print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
    chat.add_message(content)
    
    try:
        type(content.content)
        clean_content = content.content.replace(":True", ":true").replace(":False", ":false")
        json_object = json.loads(clean_content)        
    except json.JSONDecodeError as e:
        logging.error(f"JSONDecodeError: {e}")
        logging.error(f"Invalid JSON content: {content.content}")
        raise
    
    
    return json_object

if __name__ == "__main__":
    asyncio.run(main())


