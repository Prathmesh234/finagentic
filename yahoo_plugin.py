import asyncio
from typing import Annotated
import yfinance as yf
import json
from agent_instructions import ORCHESTRATOR_INSTRUCTIONS
###################################################################
import os
from dotenv import load_dotenv
# This sample allows for a streaming response verus a non-streaming response
streaming = True

from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function
"""
Yahoo plugin will have all the yahoo finance api calls available. 
The yahoo agent has to pick 3-5 plugins that it will use in order to get the most important information according to the data that the orchestrator wants. 
The orchestrator is like the investment banker designing all the tasks and picks the agents for retrieving the yahoo finance data. 
It will just demand what data to get and the yahoo agent will call the most relevant api's to get that data. Only invoking 3-4 points. 

"""
class YahooPlugin:
    """Plugin for the Web Surfer agent."""

    @kernel_function(description="Yahoo finance agent retrieves information about the company based on its ticker.")
    def get_yahoo_finance_data(self, company_name: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Data regarding the company."]:
        print(company_name)
        return company_name

    @kernel_function(description="Fetches the latest news for the company based on its ticker.")
    def get_news(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Latest news about the company."]:
        dat = yf.Ticker(company_ticker)
        news = dat.get_news()
        news_data = []
        for item in news:
            news_item = []
            news_item.append(f"UUID: {item.get('uuid')}")
            news_item.append(f"Title: {item.get('title')}")
            news_item.append(f"Publisher: {item.get('publisher')}")
            news_item.append(f"Link: {item.get('link')}")
            news_item.append(f"Provider Publish Time: {item.get('providerPublishTime')}")
            news_item.append(f"Type: {item.get('type')}")
            if 'thumbnail' in item:
                news_item.append("Thumbnail Resolutions:")
                for resolution in item['thumbnail']['resolutions']:
                    news_item.append(f"  URL: {resolution.get('url')}")
                    news_item.append(f"  Width: {resolution.get('width')}")
                    news_item.append(f"  Height: {resolution.get('height')}")
                    news_item.append(f"  Tag: {resolution.get('tag')}")
            news_item.append(f"Related Tickers: {', '.join(item.get('relatedTickers', []))}")
            news_data.append("\n".join(news_item))
        return news_data

    @kernel_function(description="Retrieves the last 15 days of stock history for the company.")
    def get_15days_history(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Past 15 days of stock history."]:
        dat_15days = yf.Ticker(company_ticker)
        dat_15days_history = dat_15days.history()
        return dat_15days_history

    @kernel_function(description="Fetches concise metadata of the company.")
    def get_15days_history_metadata(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Metadata of the company."]:
        dat_15days_metadata = yf.Ticker(company_ticker)
        dat_15days_history_metadata = dat_15days_metadata.get_history_metadata()
        metadata_items = []
        metadata_items.append(f"Currency: {dat_15days_history_metadata.get('currency')}")
        metadata_items.append(f"Symbol: {dat_15days_history_metadata.get('symbol')}")
        metadata_items.append(f"Exchange Name: {dat_15days_history_metadata.get('exchangeName')}")
        metadata_items.append(f"Full Exchange Name: {dat_15days_history_metadata.get('fullExchangeName')}")
        metadata_items.append(f"Instrument Type: {dat_15days_history_metadata.get('instrumentType')}")
        metadata_items.append(f"First Trade Date: {dat_15days_history_metadata.get('firstTradeDate')}")
        metadata_items.append(f"Regular Market Time: {dat_15days_history_metadata.get('regularMarketTime')}")
        metadata_items.append(f"Has Pre/Post Market Data: {dat_15days_history_metadata.get('hasPrePostMarketData')}")
        metadata_items.append(f"GMT Offset: {dat_15days_history_metadata.get('gmtoffset')}")
        metadata_items.append(f"Timezone: {dat_15days_history_metadata.get('timezone')}")
        metadata_items.append(f"Exchange Timezone Name: {dat_15days_history_metadata.get('exchangeTimezoneName')}")
        metadata_items.append(f"Regular Market Price: {dat_15days_history_metadata.get('regularMarketPrice')}")
        metadata_items.append(f"Fifty-Two Week High: {dat_15days_history_metadata.get('fiftyTwoWeekHigh')}")
        metadata_items.append(f"Fifty-Two Week Low: {dat_15days_history_metadata.get('fiftyTwoWeekLow')}")
        metadata_items.append(f"Regular Market Day High: {dat_15days_history_metadata.get('regularMarketDayHigh')}")
        metadata_items.append(f"Regular Market Day Low: {dat_15days_history_metadata.get('regularMarketDayLow')}")
        metadata_items.append(f"Regular Market Volume: {dat_15days_history_metadata.get('regularMarketVolume')}")
        metadata_items.append(f"Long Name: {dat_15days_history_metadata.get('longName')}")
        metadata_items.append(f"Short Name: {dat_15days_history_metadata.get('shortName')}")
        metadata_items.append(f"Chart Previous Close: {dat_15days_history_metadata.get('chartPreviousClose')}")
        metadata_items.append(f"Previous Close: {dat_15days_history_metadata.get('previousClose')}")
        metadata_items.append(f"Scale: {dat_15days_history_metadata.get('scale')}")
        metadata_items.append(f"Price Hint: {dat_15days_history_metadata.get('priceHint')}")
        metadata_items.append(f"Current Trading Period: {dat_15days_history_metadata.get('currentTradingPeriod')}")
        metadata_items.append(f"Trading Periods: {dat_15days_history_metadata.get('tradingPeriods')}")
        metadata_items.append(f"Data Granularity: {dat_15days_history_metadata.get('dataGranularity')}")
        metadata_items.append(f"Range: {dat_15days_history_metadata.get('range')}")
        metadata_items.append(f"Valid Ranges: {', '.join(dat_15days_history_metadata.get('validRanges', []))}")

        dat_15days_history_metadata = metadata_items
        
        return dat_15days_history_metadata

    @kernel_function(description="Retrieves quarterly dividends issued by the company.")
    def get_dividends(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Company dividends since inception."]:
        dat = yf.Ticker(company_ticker)
        dividends_data = dat.get_dividends()
        return dividends_data

    @kernel_function(description="Fetches stock splits and dividends since inception.")
    def get_stock_splits(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Stock splits and dividends data."]:
        dat = yf.Ticker(company_ticker)
        stock_split_data = dat.get_actions()
        return stock_split_data

    @kernel_function(description="Retrieves total shares outstanding since inception.")
    def get_total_shares(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Total shares outstanding."]:
        dat = yf.Ticker(company_ticker)
        total_shares = dat.get_shares_full()
        return total_shares

    @kernel_function(description="Retrieves key company metadata including address and financial data.")
    def get_stock_info(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Company metadata and financial details."]:
        dat = yf.Ticker(company_ticker)
        stock_info = dat.get_info()
        stock_info_return = []
        for key, value in stock_info.items():
            stock_info_return.append(f"{key}: {value}")
        return stock_info_return

    @kernel_function(description="Fetches the latest news along with publisher and links.")
    def get_latest_news(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Latest company news."]:
        dat = yf.Ticker(company_ticker)
        latest_news = dat.get_news()
        news_items = []
        for item in latest_news:
            news_item = []
            news_item.append(f"UUID: {item.get('uuid')}")
            news_item.append(f"Title: {item.get('title')}")
            news_item.append(f"Publisher: {item.get('publisher')}")
            news_item.append(f"Link: {item.get('link')}")
            news_item.append(f"Provider Publish Time: {item.get('providerPublishTime')}")
            news_item.append(f"Type: {item.get('type')}")
            if 'thumbnail' in item:
                news_item.append("Thumbnail Resolutions:")
                for resolution in item['thumbnail']['resolutions']:
                    news_item.append(f"  URL: {resolution.get('url')}")
                    news_item.append(f"  Width: {resolution.get('width')}")
                    news_item.append(f"  Height: {resolution.get('height')}")
                    news_item.append(f"  Tag: {resolution.get('tag')}")
            news_item.append(f"Related Tickers: {', '.join(item.get('relatedTickers', []))}")
            news_items.append("\n".join(news_item))
        return news_items

    @kernel_function(description="Retrieves the quarterly income statement of the company.")
    def get_income_statement(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Quarterly income statement."]:
        dat = yf.Ticker(company_ticker)
        income_stmt = dat.get_income_stmt(freq='quarterly')
        return income_stmt

    @kernel_function(description="Retrieves the quarterly balance sheet of the company.")
    def get_balance_sheet(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Quarterly balance sheet."]:
        dat = yf.Ticker(company_ticker)
        balance_sheet = dat.get_balance_sheet(freq='quarterly')
        return balance_sheet

    @kernel_function(description="Retrieves the quarterly cash flow statement of the company.")
    def get_cashflow(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Quarterly cash flow statement."]:
        dat = yf.Ticker(company_ticker)
        cashflow = dat.get_cashflow(freq='quarterly')
        return cashflow

    @kernel_function(description="Fetches recent analyst upgrades and downgrades for the company.")
    def get_upgrades_downgrades(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Analyst recommendations and changes."]:
        dat = yf.Ticker(company_ticker)
        upgrades_downgrades = dat.get_upgrades_downgrades()
        return upgrades_downgrades
