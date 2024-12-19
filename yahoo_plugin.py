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

    @kernel_function(description="Yahoo finance agent given the ticker gets information about the company")
    def get_yahoo_finance_data(self, company_name: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Data regarding the company which includes "]:
        print(company_name)
        return company_name
    ##Gets the latest news regarding the compaany
    @kernel_function(description="Gets the latest news regarding the company")
    def get_news(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Latest News regarding the company"]:
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
    

    ##Gets the history of the company for the last 15 days which includes the open, close, high, low, volume, dividends and stock splits of the company
    @kernel_function(description="Gets the history of the company for the last 15 days which includes the open, close, high, low, volume, dividends and stock splits of the company in a DataFrame format.")
    def get_15days_history(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Past 15 days history of the company which includes the open, close, high, low, volume, dividends and stock splits of the company"]:
        dat_15days = yf.Ticker(company_ticker)
        dat_15days_history = dat_15days.history()
        return dat_15days_history
    


    ##Gets the metadata of the company which includes currency, symbol, exchange name, full exchange name, instrument type, first trade date, regular market time, pre/post market data availability, GMT offset, timezone, exchange timezone name, regular market price, fifty-two week high, fifty-two week low, regular market day high, regular market day low, regular market volume, long name, short name, chart previous close, previous close, scale, price hint, current trading period, trading periods, data granularity, range, and valid ranges.
    @kernel_function(description="Gets the metadata of the company which includes currency, symbol, exchange name, full exchange name, instrument type, first trade date, regular market time, pre/post market data availability, GMT offset, timezone, exchange timezone name, regular market price, fifty-two week high, fifty-two week low, regular market day high, regular market day low, regular market volume, long name, short name, chart previous close, previous close, scale, price hint, current trading period, trading periods, data granularity, range, and valid ranges.")
    def get_15days_history_metadata(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Metadata of the company which includes currency, symbol, exchange name, full exchange name, instrument type, first trade date, regular market time, pre/post market data availability, GMT offset, timezone, exchange timezone name, regular market price, fifty-two week high, fifty-two week low, regular market day high, regular market day low, regular market volume, long name, short name, chart previous close, previous close, scale, price hint, current trading period, trading periods, data granularity, range, and valid ranges."]:
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
    
    ##Gets the dividends of the company that have been given since it's inception every quarter
    @kernel_function(description="Gets the dividends of the company has given since it's inception every quarter")
    def get_dividends(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Returns the dividends of the company has given since 2003 every quarter"]:
        dat = yf.Ticker(company_ticker)
        dividends_data = dat.get_dividends()
        return dividends_data
    
    ##Gets the stock splits of the company since it's inception along with the dividends every year. 
    @kernel_function(description="Gets the stock splits of the company since it's inception and it's dividends distributed.")
    def get_stock_splits(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Returns the stock splits of the company since it's inception and it's dividends distributed."]:
        dat = yf.Ticker(company_ticker)
        stock_split_data = dat.get_actions()
        return stock_split_data
    
    ##Gets the total number of shares outstanding for a given stock since it's inception
    @kernel_function(description="Gets the total number of shares outstanding for a given stock since it's inception.")
    def get_total_shares(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Returns the total number of shares outstanding for a given stock since it's inception."]:
        dat = yf.Ticker(company_ticker)
        total_shares = dat.get_shares_full()
        return total_shares
    
      ##Gets the total number of shares outstanding for a given stock since it's inception
    @kernel_function(description="Gets the metadata of the company which includes address, city, state, zip, country, phone, website, industry, industry key, industry display, sector, sector key, sector display, long business summary, full-time employees, company officers, audit risk, board risk, compensation risk, shareholder rights risk, overall risk, governance epoch date, compensation as of epoch date, IR website, max age, price hint, previous close, open, day low, day high, regular market previous close, regular market open, regular market day low, regular market day high, dividend rate, dividend yield, ex-dividend date, payout ratio, five-year average dividend yield, beta, trailing PE, forward PE, volume, regular market volume, average volume, average volume over 10 days, average daily volume over 10 days, bid, ask, bid size, ask size, market cap, fifty-two week low, fifty-two week high, price to sales trailing 12 months, fifty-day average, two hundred-day average, trailing annual dividend rate, trailing annual dividend yield, currency, enterprise value, profit margins, float shares, shares outstanding, shares short, shares short prior month, shares short previous month date, date short interest, shares percent shares out, held percent insiders, held percent institutions, short ratio, short percent of float, implied shares outstanding, book value, price to book, last fiscal year end, next fiscal year end, most recent quarter, earnings quarterly growth, net income to common, trailing EPS, forward EPS, last split factor, last split date, enterprise to revenue, enterprise to EBITDA, fifty-two week change, S&P fifty-two week change, last dividend value, last dividend date, exchange, quote type, symbol, underlying symbol, short name, long name, first trade date epoch UTC, time zone full name, time zone short name, UUID, message board ID, GMT offset milliseconds, current price, target high price, target low price, target mean price, target median price, recommendation mean, recommendation key, number of analyst opinions, total cash, total cash per share, EBITDA, total debt, quick ratio, current ratio, total revenue, debt to equity, revenue per share, return on assets, return on equity, free cash flow, operating cash flow, earnings growth, revenue growth, gross margins, EBITDA margins, operating margins, financial currency, and trailing PEG ratio.")
    def get_stock_info(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Returns the metadata of the company which includes address, city, state, zip, country, phone, website, industry, industry key, industry display, sector, sector key, sector display, long business summary, full-time employees, company officers, audit risk, board risk, compensation risk, shareholder rights risk, overall risk, governance epoch date, compensation as of epoch date, IR website, max age, price hint, previous close, open, day low, day high, regular market previous close, regular market open, regular market day low, regular market day high, dividend rate, dividend yield, ex-dividend date, payout ratio, five-year average dividend yield, beta, trailing PE, forward PE, volume, regular market volume, average volume over 10 days, average daily volume over 10 days, bid, ask, bid size, ask size, market cap, fifty-two week low, fifty-two week high, price to sales trailing 12 months, fifty-day average price to sales trailing 12 months ratio value and two hundred-day average price to sales trailing 12 months ratio value."]:
        dat = yf.Ticker(company_ticker)
        stock_info = dat.get_info()
        stock_info_return = []
        for key, value in stock_info.items():
            stock_info_return.append(f"{key}: {value}")
        return stock_info_return
    
    ##Gets the latest news about the company along with the Title, Publisher, Link, Provider Publish Time, Type, Thumbnail Resolutions, and Related Tickers.
    @kernel_function(description="Gets the latest news about the company along with the Title, Publisher, Link, Provider Publish Time, Type, Thumbnail Resolutions, and Related Tickers.")
    def get_latest_news(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Returns the latest news about the company along with the Title, Publisher, Link, Provider Publish Time, Type, Thumbnail Resolutions, and Related Tickers"]:
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
    
       ##Gets the total number of shares outstanding for a given stock since it's inception
    @kernel_function(description="Gets Quarterly the income statement for the company which includes Tax Effect Of Unusual Items, Tax Rate For Calcs, Normalized EBITDA, Total Unusual Items, Total Unusual Items Excluding Goodwill, Net Income From Continuing Operation Net Minority Interest, Reconciled Depreciation, Reconciled Cost Of Revenue, EBITDA, EBIT, Net Interest Income, Interest Expense, Interest Income, Normalized Income, Net Income From Continuing And Discontinued Operation, Total Expenses, Total Operating Income As Reported, Diluted Average Shares, Basic Average Shares, Diluted EPS, Basic EPS, Diluted NI Available to Common Stockholders, Average Dilution Earnings, Net Income Common Stockholders, Net Income, Net Income Including Noncontrolling Interests, Net Income Continuous Operations, Tax Provision, Pretax Income, Other Income Expense, Other Non Operating Income Expenses, Special Income Charges, Other Special Charges, Impairment Of Capital Assets, Net Non Operating Interest Income Expense, Total Other Finance Cost, Interest Expense Non Operating, Interest Income Non Operating, Operating Income, Operating Expense, Research And Development, Selling General And Administration, Selling And Marketing Expense, General And Administrative Expense, Other G and A, Gross Profit, Cost Of Revenue, Total Revenue, and Operating Revenue.")
    def get_income_statement(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Returns the income statement for the company which includes Tax Effect Of Unusual Items, Tax Rate For Calcs, Normalized EBITDA, Total Unusual Items, Total Unusual Items Excluding Goodwill, Net Income From Continuing Operation Net Minority Interest, Reconciled Depreciation, Reconciled Cost Of Revenue, EBITDA, EBIT, Net Interest Income, Interest Expense, Interest Income, Normalized Income, Net Income From Continuing And Discontinued Operation, Total Expenses, Total Operating Income As Reported, Diluted Average Shares, Basic Average Shares, Diluted EPS, Basic EPS, Diluted NI Available to Common Stockholders, Average Dilution Earnings, Net Income Common Stockholders, Net Income, Net Income Including Noncontrolling Interests, Net Income Continuous Operations, Tax Provision, Pretax Income, Other Income Expense, Other Non Operating Income Expenses, Special Income Charges, Other Special Charges, Impairment Of Capital Assets, Net Non Operating Interest Income Expense, Total Other Finance Cost, Interest Expense Non Operating, Interest Income Non Operating, Operating Income, Operating Expense, Research And Development, Selling General And Administration, Selling And Marketing Expense, General And Administrative Expense, Other G and A, Gross Profit, Cost Of Revenue, Total Revenue, and Operating Revenue."]:
        dat = yf.Ticker(company_ticker)
        income_stmt = dat.get_income_stmt(freq='quarterly')
        return income_stmt
    
    @kernel_function(description="Gets the quarterly balance sheet for the company which includes Treasury Shares Number, Ordinary Shares Number, Shares Issued, Net Debt, Total Debt, Accounts Receivable, Allowance For Doubtful Accounts Receivable, Gross Accounts Receivable, Cash Cash Equivalents And Short Term Investments, and Cash And Cash Equivalents.")
    def get_balance_sheet(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Returns the quarterly balance sheet for the company which includes Treasury Shares Number, Ordinary Shares Number, Shares Issued, Net Debt, Total Debt, Accounts Receivable, Allowance For Doubtful Accounts Receivable, Gross Accounts Receivable, Cash Cash Equivalents And Short Term Investments, and Cash And Cash Equivalents."]:
        dat = yf.Ticker(company_ticker)
        balance_sheet = dat.get_balance_sheet(freq='quarterly')
        return balance_sheet

    @kernel_function(description="Gets the quarterly cash flow statement for the company which includes Free Cash Flow, Repayment Of Debt, Issuance Of Debt, Issuance Of Capital Stock, Capital Expenditure, End Cash Position, Beginning Cash Position, Effect Of Exchange Rate Changes, Changes In Cash, Financing Cash Flow, Cash Flow From Continuing Financing Activities, Net Other Financing Charges, Proceeds From Stock Option Exercised, Net Common Stock Issuance, Common Stock Issuance, Net Issuance Payments Of Debt, Net Long Term Debt Issuance, Long Term Debt Payments, Long Term Debt Issuance, Investing Cash Flow, Cash Flow From Continuing Investing Activities, Net Intangibles Purchase And Sale, Purchase Of Intangibles, Net PPE Purchase And Sale, Purchase Of PPE, Operating Cash Flow, Cash Flow From Continuing Operating Activities, Change In Working Capital, Change In Other Working Capital, Change In Other Current Liabilities, Change In Payables And Accrued Expense, Change In Accrued Expense, Change In Interest Payable, Change In Payable, Change In Account Payable, Change In Prepaid Assets, Change In Receivables, Changes In Account Receivables, Other Non Cash Items, Stock Based Compensation, Provision and Write Off of Assets, Asset Impairment Charge, Deferred Tax, Deferred Income Tax, Depreciation Amortization Depletion, Depreciation And Amortization, Operating Gains Losses, and Net Income From Continuing Operations.")
    def get_cashflow(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Returns the quarterly cash flow statement for the company which includes Free Cash Flow, Repayment Of Debt, Issuance Of Debt, Issuance Of Capital Stock, Capital Expenditure, End Cash Position, Beginning Cash Position, Effect Of Exchange Rate Changes, Changes In Cash, Financing Cash Flow, Cash Flow From Continuing Financing Activities, Net Other Financing Charges, Proceeds From Stock Option Exercised, Net Common Stock Issuance, Common Stock Issuance, Net Issuance Payments Of Debt, Net Long Term Debt Issuance, Long Term Debt Payments, Long Term Debt Issuance, Investing Cash Flow, Cash Flow From Continuing Investing Activities, Net Intangibles Purchase And Sale, Purchase Of Intangibles, Net PPE Purchase And Sale, Purchase Of PPE, Operating Cash Flow, Cash Flow From Continuing Operating Activities, Change In Working Capital, Change In Other Working Capital, Change In Other Current Liabilities, Change In Payables And Accrued Expense, Change In Accrued Expense, Change In Interest Payable, Change In Payable, Change In Account Payable, Change In Prepaid Assets, Change In Receivables, Changes In Account Receivables, Other Non Cash Items, Stock Based Compensation, Provision and Write Off of Assets, Asset Impairment Charge, Deferred Tax, Deferred Income Tax, Depreciation Amortization Depletion, Depreciation And Amortization, Operating Gains Losses, and Net Income From Continuing Operations."]:
        dat = yf.Ticker(company_ticker)
        cashflow = dat.get_cashflow(freq='quarterly')
        return cashflow
    
    @kernel_function(description="Gets a DataFrame with the recommendations changes (upgrades/downgrades) Index: date of grade Columns: firm toGrade fromGrade action")
    def get_upgrades_downgrades(self, company_ticker: Annotated[str, "The ticker of the company to work with yfinance"]) -> Annotated[str, "Returns a DataFrame with the recommendations changes (upgrades/downgrades) Index: date of grade Columns: firm toGrade fromGrade action."]:
        dat = yf.Ticker(company_ticker)
        upgrades_downgrades = dat.get_upgrades_downgrades()
        return upgrades_downgrades

    

    
