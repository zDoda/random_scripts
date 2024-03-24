#!/usr/bin/env python3

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
import time

# Define a function to test a specific browser
def test_browser(driver, browser_name):
    try:
        # Open the browser and go to the desired webpage
        driver.get("http://example.com") # Replace with your desired URL

        # Perform the desired tests, e.g., checking if a certain element exists
        element = driver.find_element(By.ID, "someElementId") # Replace with your actual element information

        # Check if the element is visible or has the expected text/value
        if element.is_displayed():
            print(f"{browser_name}: Element is displayed as expected.")
        else:
            print(f"{browser_name}: WARNING! Element is not displayed.")

    except Exception as e:
        print(f"{browser_name}: Encountered an exception - {e}")

    finally:
        # Close the browser window
        driver.quit()


# Test on Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
test_browser(chrome_driver, "Chrome")

# Test on Firefox
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--no-sandbox')
firefox_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
test_browser(firefox_driver, "Firefox")

# Test on Edge
edge_options = webdriver.EdgeOptions()
edge_options.add_argument('--no-sandbox')
edge_driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=edge_options)
test_browser(edge_driver, "Edge")

print("Cross-browser compatibility testing completed.")
