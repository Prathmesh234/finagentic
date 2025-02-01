from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import json
import os 
import asyncio
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

'''
The basic layout of the web agent is going to be as the following - 
1) We are going to build a chromium/selenium web driver plugin - done
2) Next we are going to take screenshots using omniparser 
3) These annotated screenshots are then going to be sent to azure ai inference for processing 
4) We are going to start with a prompt, get the website, navigate to the website, take a screenshot, use omni parser to annotate the screenshot and process using azure ai 
'''
AGENT_NAME="Computer_use_agent"
AGENT_INSTRUCTIONS = "You are a helpful agent, answer the user's queries"

async def web_agent(user_quer: str):
    options = Options()
    options.add_argument("--start-maximized")  # Start the browser maximized

# Initialize the Edge WebDriver
    service = Service()  # Update with the correct path if needed
    driver = webdriver.Edge(service=service, options=options)
    try:
        driver.get("https://esxp.microsoft.com/#/time/weekview")
        time.sleep(10)
        resources_folder = os.path.join(os.getcwd(), "resources")
        if not os.path.exists(resources_folder):
            os.makedirs(resources_folder)
        screenshot_path = os.path.join(resources_folder, "screenshot.png")
    # Take a screenshot and save it
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()

def main():
    asyncio.run(web_agent("How to use selenium webdriver"))

if __name__ == "__main__":
    main()









