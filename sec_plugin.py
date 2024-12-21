import requests
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function
import requests
from bs4 import BeautifulSoup
import os 
from dotenv import load_dotenv
import yfinance as yf
from datetime import datetime
import pdfkit


class SecPlugin:
    """Plugin for the Web Surfer agent."""

    @kernel_function(description="Provides the latest SEC filings for a company specifically 10-Q, 10-K and 8-K")
    def get_latest_sec_filings(self, company_name: Annotated[str, "The name of the company to search for"]) -> Annotated[str, "Returns the latest SEC filings for a company specifically 10-Q, 10-K and 8-K"]:
        company_ticker = self.get_ticker(company_name)
        sec_filings = company_ticker.get_sec_filings()
        latest_documents = {'8-K': None, '10-Q': None, '10-K': None}
        for entry in sec_filings:
            doc_type = entry['type']
            date = entry['date']  # Use the date directly as it's already a datetime.date object
            exhibits = entry.get('exhibits', {})

    # Check if there's already a newer document of the same type
            if doc_type in latest_documents:
                if (latest_documents[doc_type] is None or
                        latest_documents[doc_type]['date'] < date):
                 latest_documents[doc_type] = {'url': exhibits.get(doc_type), 'date': date}
        latest_urls = {doc_type: info['url'] for doc_type, info in latest_documents.items() if info}

        data = self.convert_pdf(latest_urls)
        



        
        return data
    @kernel_function(description="Helper to get the ticker of the company")
    def get_ticker(self, company_name:str):
        ticker = yf.Ticker(company_name)
        return ticker
    @kernel_function(description="Helper to convert the pdf")
    def convert_pdf(self, company_filings:dict):
        return_data = ""
        for doc_type, url in company_filings.items():
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                html_content = soup.prettify()
                pdfkit.from_string(html_content, f"`{doc_type}.pdf`")
                print(f"Pdf successfully created for file {doc_type}")
            except:
                text = soup.get_text(separator='\n', strip=True)
                return_data += f"Value for {doc_type} is - {text}"
                return_data += "---------------------------------------------------------------------------------------------------------------------------------------------------------------------"
                print(f"Error creating pdf for file {doc_type}")
                
        return return_data
            

            
       