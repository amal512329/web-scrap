import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import re


options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("window-size=1200x600")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.92 Safari/537.36")

# Use Service to set the executable path for the WebDriver
service = Service("./chromedriver/chromedriver.exe")  # Set the correct path to chromedriver here
wd = webdriver.Chrome(service=service, options=options)


def login_sites(login_website, wd, email, password):
    l = []
    wd.get(login_website)
    time.sleep(5)

    # Wait for the page to fully load by waiting for a key element or the end of a loading indicator
    try:
        WebDriverWait(wd, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Page fully loaded!")
    except Exception as e:
        print("Page not loaded within time:", e)
        return None  # Return None if login fails

    # Get all form elements on the page
    form_elements = wd.find_elements(By.TAG_NAME, "form")
    print(f"{len(form_elements)} form(s) found!")

    # Iterate through each form element
    for form_element in form_elements:
        email_input = None
        password_input = None
        submit_button = None

        print("Element is visible? " + str(form_element.is_displayed()))

        # Find all input elements within the form
        input_elements = form_element.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(input_elements)} input elements!")

        for input_element in input_elements:
            input_type = input_element.get_attribute("type")
            placeholder = input_element.get_attribute("placeholder")
            name_attr = input_element.get_attribute("name")
            title_attr = input_element.get_attribute('title')
            print('Checking input element:', input_element)

            # Combine all the attributes into one string for easy search
            field_attributes = f"{placeholder} {name_attr} {title_attr}".lower()

            # # Check if the input field is for email or username
            if re.search(r"(email|username)", field_attributes, re.I):
                print('Username or email matched')
                print("All attributes of the input element:", input_element.get_attribute("outerHTML"))
                print("Element is visible? " + str(input_element.is_displayed()))
                email_input = input_element
                email_input.send_keys(email)  # Enter the email into the field
                print("Email entered.")

            # Check if the input field is for password
            if re.search(r"password", f"{placeholder} {field_attributes}", re.I):
                password_input = input_element
                password_input.send_keys(password)  # Enter the password into the field
                print("Password entered.")

           
        
        # Find the submit button within the form
        button_elements = form_element.find_elements(By.TAG_NAME, "button") + form_element.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(button_elements)} button elements!")

        # Initialize the submit_button and div_button to None
        submit_button = None
        div_button = None
        # Look for a div that might act as a login button with text like 'login' or 'sign in'
        div_elements = form_element.find_elements(By.TAG_NAME, "div")
        for div in div_elements:
            div_text = div.text
            if re.search(r"(sign in|login|submit)", div_text, re.I):
                div_button = div
                print("Div button with 'login' text found.")
                break

        for button in button_elements:
            button_text = button.get_attribute("value") or button.text

            # Check for button text that matches 'login', 'sign in', or 'submit'
            if re.search(r"(sign in|login|submit)", button_text, re.I):
                submit_button = button
                break

        # Click the appropriate button based on what was found
        if submit_button:
            submit_button.click()
            print("Submit button clicked.")
        elif div_button:
            div_button.click()
            print("Div button clicked.")
        
        # Wait and verify successful login
        try:
            WebDriverWait(wd, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Login successful!")
            return True  # Return True on successful login
        except Exception as e:
            print("Login verification failed:", e)
            continue  # If login failed, try the next form

    print("No form successfully logged in.")
    return False  # Return False if no form succeeded

login_website = 'https://archibase.co/#gsc.tab=0'
email = 'amaldq333@gmail.com'
password = 'archibase123'

login_sites(login_website,wd,email,password)