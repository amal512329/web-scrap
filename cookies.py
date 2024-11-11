import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# Initialize Chrome WebDriver with options
options = Options()
options.add_argument('--headless')  # Headless mode
options.add_argument('--disable-gpu')
service = Service('./chromedriver/chromedriver.exe')  # Replace with your path to chromedriver
wd = webdriver.Chrome(service=service, options=options)

# Function to save cookies to a file
def saveCookies(wd):
    cookies = wd.get_cookies()  # Fetch cookies after login
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)
    print("Cookies saved successfully.")

# URL for login
loginURL = 'https://grabcad.com/login'
dashboardURL = 'https://grabcad.com/dashboard'

# Step 1: Open the login page
wd.get(loginURL)  # Load the login page

# Step 2: Enter login credentials and submit the form
try:
    email_field = wd.find_element(By.XPATH, "//*[contains(@id, 'email') or contains(@name, 'email')]")
    email_field.send_keys("amalmohanan555@gmail.com")  # Replace with your actual username
    print("Email Entered")

    password_field = wd.find_element(By.XPATH, "//*[contains(@id, 'password') or contains(@name, 'password')]")
    password_field.send_keys(".grabcad123")  # Replace with your actual password
    print("Password Entered")

    submit_button = wd.find_element(By.XPATH, "//*[contains(@type, 'submit') or contains(@value, 'Login') or contains(@value, 'Sign In')]")
    submit_button.click()

    print("Login form submitted.")
except Exception as e:
    print(f"Error locating login elements: {e}")

# Step 3: Wait for login to complete (use an explicit wait to ensure the login form has been processed)
time.sleep(5)  # Adjust the sleep time if necessary (to allow login)

# Step 4: Save cookies after login
saveCookies(wd)

# Step 5: Navigate to the dashboard to confirm the login
wd.get(dashboardURL)  # Navigate to the dashboard page

# Step 6: Wait for the dashboard page to load and verify if login was successful
try:
    WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    if "dashboard" in wd.current_url:
        print("Login successful. Dashboard accessed.")
    else:
        print("Dashboard access denied.")

except TimeoutException:
    print("Dashboard loading timed out.")

# Close the browser
wd.quit()
print('Login successful and cookies saved.')
