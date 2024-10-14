#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def test_browser(browser_name):
    if browser_name == 'Chrome':
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser_name == 'Firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser_name == 'Edge':
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    else:
        raise ValueError(f"{browser_name} is not a supported browser")

    driver.maximize_window()
    driver.get('http://example.com')
    
    # Example test: Check if the title contains the word 'Example Domain'
    assert 'Example Domain' in driver.title

    # here you can add more tests/asserts

    # Close the browser window
    driver.quit()

if __name__ == "__main__":
    browsers = ['Chrome', 'Firefox', 'Edge']
    for browser in browsers:
        print(f"Testing in {browser}")
        test_browser(browser)
        print(f"Done testing in {browser}")
