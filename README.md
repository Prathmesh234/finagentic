# **Finagentic - Financial Analyst inspired by the MagenticOne Framework**

Introducing **Finagentic**, an agentic framework for executing queries regarding financial data using **4 different financial agents**. This project leverages **Semantic Kernel** for agent orchestration and production-level agent deployment, inspired by Microsoft's **MagenticOne Agentic Framework** ([GitHub repository](https://github.com/microsoft/autogen/tree/main/python/packages/autogen-magentic-one)).

---

## **Agents Overview**

1. **SEC Agent**  
   Scrapes data from the SEC website to retrieve the latest **10-Q**, **8-K**, and **10-K** documents for analysis.

2. **Yahoo Finance Agent**  
   Uses **15+ yfinance functions and tools** to fetch detailed data related to user queries.

3. **Web Surfer Agent**  
   Utilizes the **Bing API** to retrieve the latest news and events regarding the user query.

4. **Prospectus Agent**  
   Generates a **well-detailed financial prospectus** tuned to the user's trade, similar to a financial prospectus but customized for user needs.

5. **Orchestrator Agent**  
   Acts as the **core of the framework**, creating a task ledger and monitoring the execution of tasks by different agents.

![image](https://github.com/user-attachments/assets/740f63e5-5e93-4685-9d12-f72802a00f70)


## **Ongoing Development**

This is an ongoing project, and additional functionalities, such as **chart generation** for financial data, will soon be added to the final **Prospectus PDF** created by the agents.  

### **Upcoming Features:**
- **Code Executor Agent**  
  To generate **matplotlib charts** and other visualizations.  

- **Web Surfing Agent**  
  Using **Chromium-based web scrapers** and **Microsoft Playwright** to fetch more comprehensive data and create detailed answers.  

### **Vision for the Future:**  
We aim to expand the framework to include over **1,000 agents**, all orchestrated by a single **Orchestrator Agent**.

---

## **How to Try It Yourself**

Follow these steps to set up **Finagentic**:  

```bash
git clone https://github.com/Prathmesh234/finagentic
cd finagentic
pip install -r requirements.txt
python Orchestrator.py --user_query=""
```

---

## **Orchestrator Task Ledger**

### **Example Query:**  
*"Microsoft's recent quarter performance and how much are they spending on data centers and their capex increase since last year."*

### **Generated Task Ledger:**
```json
orchestrator_agent: '{
    "company_name": "Microsoft Corporation",
    "task_ledger": {
        "task 1": "Microsoft Corporation - Identify Stock Ticker and Confirm Inquiry",
        "task 2": "Microsoft Corporation (Ticker: MSFT) - Assess Data Center Spend",
        "task 3": "Microsoft Corporation - Analyze Financial Impact",
        "task 4": "Microsoft Corporation - Market Positioning"
    },
    "agent_to_execute": "web_surfer_agent",
    "progress": "false",
    "answer_score": "N/A",
    "rejection_reason": "N/A",
    "final_answer": "",
    "stock_ticker": "",
    "details_needed": "Find the latest financial news and data related to Microsoft Corporation's data center spend TICKER:MSFT"
}'
```

---

## **Agent Execution**

The **Orchestrator** determines the required data and assigns tasks to specific agents. Each agent executes the task and sends the results back to the **Orchestrator** for evaluation. The orchestrator either accepts or rejects the answers based on their quality.

### **Example Execution:**  

#### **Web Surfer Agent:**
```json
web_surfer: {
    "details_needed": "Find the latest financial news and data related to Microsoft Corporation's data center spend TICKER:MSFT",
    "search_query": "Microsoft Corporation data center spending news 2023",
    "answer": "Microsoft has been placing substantial capital expenditure bets on data centers to support its cloud and AI initiatives. This strategy reflects the company's effort to strengthen its infrastructure and service offerings in these high-demand areas.",
    "task_completed": "True"
}
```
The agents such as web surfer above review the work before sending it to Orchestrator for better quality of output.
---

### **Orchestrator Agent Execution Example**

Below is an example of how the **Orchestrator Agent** generates and manages tasks, assigns agents, and evaluates their responses:

#### **Orchestrator Agent Output**
```json
{
    "company_name": "Microsoft Corporation",
    "task_ledger": {
        "task 2": "Microsoft Corporation (MSFT) - Assess Data Center Spend",
        "task 3": "Microsoft Corporation - Analyze Financial Impact",
        "task 4": "Microsoft Corporation - Market Positioning"
    },
    "agent_to_execute": "yahoo_finance_agent",
    "progress": "true",
    "answer_score": "good",
    "rejection_reason": "N/A",
    "final_answer": "Microsoft has been placing substantial capital expenditure bets on data centers to support its cloud and AI initiatives. This strategy reflects the company's effort to strengthen its infrastructure and service offerings in these high-demand areas.",
    "stock_ticker": "MSFT",
    "details_needed": "Analyze the financial impact of Microsoft Corporation's increased data center spending TICKER:MSFT"
}
```

#### **Yahoo Finance Agent:**
```json
yahoo_finance_agent: {
    "details_needed": "Analyze the financial impact of Microsoft Corporation's increased data center spending TICKER:MSFT",
    "ticker": "MSFT",
    "answer": "Microsoft's increased spending on data centers as part of its expansion in cloud and AI services has been reflected in their financial statements. In 2024, capital expenditures significantly rose compared to 2023, marking $14.92 billion in the latest quarter. Meanwhile, the company maintained strong overall financial health with a free cash flow of $19.26 billion, benefiting from effective revenue growth strategies, despite higher debt levels at $91.64 billion. These investments support Microsoft's strategic positioning, showcasing a calculated risk likely to yield significant long-term gains in the tech market.",
    "task_completed": "True"
}
```

---

## **Why Use Semantic Kernel?**

**Semantic Kernel** is ideal for this project due to its:  
- **Inbuilt Plugins** for various tasks.  
- Capability for **production-level deployment of agents**.

---

## **Goal of Finagentic**

The ultimate goal of **Finagentic** is to create an **end-to-end financial analyst** that answers complex trade-related queries and provides real-time, democratized access to financial information.  

We envision this project as a continuous effort to innovate in the financial analysis space for years to come. Another goal is to create a shared Semantic Memory between all these agents in order to make sure no redudant mistakes occur. Find more about semantic memory here  - https://github.com/Prathmesh234/Semantic_memory.


