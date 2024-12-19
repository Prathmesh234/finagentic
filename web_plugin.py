import asyncio
from typing import Annotated
import requests
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel import Kernel
from bs4 import BeautifulSoup
import json
###################################################################
import os
from dotenv import load_dotenv
# This sample allows for a streaming response verus a non-streaming response
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function
import requests
from langchain.utilities import BingSearchAPIWrapper
import os
from dotenv import load_dotenv
class SurferPlugin:
    """Plugin for the Web Surfer agent."""

    @kernel_function(description="Searches for the given query on the web and returns 2-3 relevant links.")
    def get_website_data(self, search_query: Annotated[str, "Search query for the tool"]) -> Annotated[str, "Relevant Links regarding the search query"]:
       
        load_dotenv(".env")
        endpoint = os.getenv("BING_SEARCH_ENDPOINT") 
        credentials = os.getenv("BING_SEARCH_API_KEY")
        headers = {'Ocp-Apim-Subscription-Key': credentials}
        params = {'q': search_query, 'textDecorations': True, 'textFormat': 'HTML', 'count':3}
        response = requests.get(endpoint, headers=headers, params=params)
        results = response.json()
        return_results = {}
        query_number = 1
        for web_page in results.get('webPages', {}).get('value', []):
            try:
                return_results[query_number] = self.fetch_web_page(web_page['url'])
            except Exception as e:
                print("Error fetching web page")
                return_results[query_number] = web_page['snippet']
            query_number += 1
            
          
        pretty_results = json.dumps(return_results, indent=4)
        return pretty_results
    
    
    def parse_html(self, content) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        text_content_with_links = soup.get_text()
        words = text_content_with_links.split()
        first_100_words = ' '.join(words[:150])
        text_content_with_links = first_100_words
        return text_content_with_links

    def fetch_web_page(self, url: str) -> str:
        HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'}
        response = requests.get(url, headers=HEADERS)
        return self.parse_html(response.content)

