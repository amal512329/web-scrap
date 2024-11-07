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
import re
# Set up Chrome options
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')

# Use Service to set the executable path for the WebDriver
service = Service("./chromedriver/chromedriver.exe")  # Set the correct path to chromedriver here
wd = webdriver.Chrome(service=service, options=options)

website = 'https://grabcad.com/library?page=1&per_page=100&time=all_time&sort=popular&categories=3d-printing'

def setup_driver(timeout=180):
  
    chrome_options = Options() 
   
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
   # Create the folder if it doesn't exist

    # p = ("download.default_directory": "C:\Users\Lenovo\Downloads\models", "safebrowsing.enabled":"false")

    # Specify the download folder path
    
    chrome_options.add_experimental_option("prefs", {
    "download.default_directory": r"C:\Users\Lenovo\Downloads",  # Ensure path is correct
    "download.prompt_for_download": False,  # Do not prompt for download location
    "download.directory_upgrade": True,  # Upgrade directory if needed
    "safebrowsing.enabled": True,  #                       # Disable safe browsing to prevent interruptions
})
    
    
    # Create the driver with the specified options
    service = Service("./chromedriver/chromedriver.exe")  # Update this to your actual chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set a timeout for page loading
    driver.set_page_load_timeout(timeout)

    # Navigate directly to the dashboard (or another page that requires login)
    driver.get("https://grabcad.com/dashboard")
    
    # Optional: Add an implicit wait for elements to load on every action
    driver.implicitly_wait(10)
    return driver

driver = setup_driver()
def get_login_file(login_website,wd,email,password):
  l = []
  wd.get(login_website)
  time.sleep(2)

  login_modal = wd.find_elements(By.ID,'signInModal')
  
  print("Login Modal Found!")
  for i in login_modal:
    l.append(i)
    print(l)
  email_input = l[0].find_element(By.NAME, "member[email]")
  password_input = l[0].find_element(By.NAME, "member[password]") 

  # Enter the provided email and password
  email_input.send_keys(email)
  print("Email entered.")
  password_input.send_keys(password)
  print("Password entered.")

  # Locate and click the Sign In button
  sign_in_button = l[0].find_element(By.ID, "signInButton")
  sign_in_button.click()
  print("Sign In button clicked.")

  time.sleep(2)

  try:
        # Wait until the page redirects to the dashboard and finds the user’s name in the header
        dashboard_header = WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dashboard-header__name"))
        )
        
        # Check if the correct name appears in the dashboard header
        if dashboard_header.text.strip() == "amal m.m":
            print("Login successful and confirmed by dashboard header!")
            return True
        else:
            print("Dashboard loaded, but user name does not match. Login might have failed.")
            return False
            
  except Exception as e:
      print("Login confirmation failed:", e)
      return False


login_website = 'https://grabcad.com/login'
email = 'amalmohanan555@gmail.com'
password = '.grabcad123'


# to get body elements of the webpage
def get_body_element(website, driver):
    # Navigate to the website
    driver.get(website)
    
    # Find the <body> element and return it
    body_element = driver.find_element(By.TAG_NAME, 'body')

     # Get the 'id' attribute of the <body> tag (if it exists)
    body_id = body_element.get_attribute('id')
    
    # Print or return the body ID
    print("Body ID:", body_id)
    
    return body_element

def gather_images_links(body_element,driver):
    
    img_elements = body_element.find_elements(By.CSS_SELECTOR, 'img.previewImage')
    print('Length of the element is :',img_elements)

    # Gather href links from <a> tags around each <img> element
    # href_links = []
    
    for img in img_elements:
        try:
            # Check if the <img> tag is wrapped directly in an <a> tag with an href attribute
            parent_a = img.find_element(By.XPATH, './ancestor::a[@href]')
            print('parent_A found!')

            href_link = parent_a.get_attribute("href")
            href_links.append(href_link)
        except Exception as e:
            print(f"No <a> tag with href found around this image: {e}")
    return href_links

import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

def gather_image_links(body_element):
    # Locate all image elements with the 'previewImage' class
    img_elements = body_element.find_elements(By.CLASS_NAME, 'previewImage')
    
    # Gather href links from <a> tags around each <img> element
    href_links = []
    for img in img_elements:
        try:
            parent_a = img.find_element(By.XPATH, './ancestor::a[@href]')
            href_link = parent_a.get_attribute("href")
            href_links.append(href_link)
            print(f"Collected href: {href_link}")
        except Exception as e:
            print(f"No <a> tag with href found around this image: {e}")

    print('href links : ', href_links[10] )
    return href_links

def search_and_click_download_button(driver, href_links):
    for link in href_links:
        try:
            # Navigate to each link
            driver.get(link)
            print(f"Navigated to: {link}")
            
            # Wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            # Find all <button> elements on the page
            all_buttons = driver.find_elements(By.TAG_NAME, 'button')
            
            # Filter buttons containing 'download' in their text
            download_buttons = [button for button in all_buttons if re.search(r'\b[Dd]ownload\b', button.text)]
            print(f"Found {len(download_buttons)} download button(s) on {link} after filtering.")
            
            # download_triggered = False
            
            for index, button in enumerate(download_buttons):
                try:
                    button_class = button.get_attribute("class")
                    print(f"Download button {index + 1} clicked with class: {button_class}")

                    # Find the span within the button
                    download_span = button.find_element(By.XPATH, ".//span[normalize-space(text())='Download files']")
                    print(f"Download span found inside button {index + 1}")

                    driver.execute_script("arguments[0].scrollIntoView(true);", download_span)
                    print('Scroll into view executed successfully.')
                    WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(button)  # Wait for clickability
            )
                    # Wait until the span is clickable
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//span[contains(@class, 'gc-icon-download')]")))
                    print("Download span is clickable.")
        
                    # Click the span to trigger download
                    driver.execute_script("arguments[0].click();", download_span)
                    print("Download triggered successfully via span.")
                    print("Waiting for the download to start/completely finish...")
                    time.sleep(100)  

                except Exception as e:
                    print(f"An error occurred while clicking download span in button {index + 1}: {e}")
        
        except TimeoutException:
            print("Timeout waiting for page load.")
        
        except Exception as e:
            print(f"An error occurred while processing {link}: {e}")



# Ensure `wd` is your Selenium WebDriver instance
if get_login_file(login_website, wd, email, password):
    print("Proceeding with the next steps after login.")
else:
    print("Aborting due to unsuccessful login.")

driver = setup_driver()
website = 'https://grabcad.com/library?page=1&per_page=100&time=all_time&sort=popular&categories=3d-printing'
body_element = get_body_element(website,wd)
# Use the functions with the driver instance
href_links = gather_image_links(body_element)
search_and_click_download_button(wd, href_links)

driver.quit()
