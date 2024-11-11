from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,StaleElementReferenceException
import time
import requests
import platform
import os

# Set up Chrome options
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')


# Use Service to set the executable path for the WebDriver
service = Service("./chromedriver/chromedriver.exe")  # Set the correct path to chromedriver here
wd = webdriver.Chrome(service=service, options=options)

# Get the user agent string
# user_agent = wd.execute_script("return navigator.userAgent;")
# print(user_agent)

# wd.get(website)

# # Check the current URL
# if wd.current_url == website:
#     print("Successfully navigated to the website:", wd.current_url)
# else:
#     print("Failed to navigate. Current URL:", wd.current_url)

website = 'https://grabcad.com/library?page=1&per_page=100&time=all_time&sort=popular&categories=3d-printing'

cookies = {
    'optimizelyEndUserId': 'oeu1730540661524r0.6422308138616348',
    'optimizelySegments': '%7B%22239451939%22%3A%22gc%22%2C%22239653413%22%3A%22false%22%2C%22239748770%22%3A%22search%22%7D',
    'optimizelyBuckets': '%7B%7D',
    '_biz_uid': '9422146f11a94cd3ffee705c81d1ebff',
    '_ga': 'GA1.1.1080506923.1730540663',
    '_clck': 'nb67dw%7C2%7Cfqj%7C0%7C1767',
    '_mkto_trk': 'id:533-LAV-099&token:_mch-grabcad.com-1730540664316-91933',
    '_biz_flagsA': '%7B%22Version%22%3A1%2C%22XDomain%22%3A%221%22%2C%22ViewThrough%22%3A%221%22%2C%22Mkto%22%3A%221%22%2C%22Frm%22%3A%221%22%7D',
    '_grabcad_session': '459b89a54e47a6455ab4065cfaf7e2cc',
    '__gads': 'ID=e0c071270444e27f:T=1730540888:RT=1730547582:S=ALNI_MbntfvGQ1ugZfUpfzunon4xEUi6xA',
    '__gpi': 'UID=00000f4d00493d3c:T=1730540888:RT=1730547582:S=ALNI_Mb85B9I2AkHTdzRuIfs6W_skeQBWA',
    '__eoi': 'ID=9a5f6798ee5a177d:T=1730540888:RT=1730547582:S=AA-AfjblGJZ6y5_JzghQH-PwdLZK',
    '_biz_nA': '26',
    '_ga_173TDQJFJ7': 'GS1.1.1730540662.1.1.1730547817.59.0.0',
    '_biz_pendingA': '%5B%5D',
    'XSRF-TOKEN': 'jzTxzXo2jHd%2FdN7ZPKP1J%2Bxkhosq%2FAVrbTWGmaDXNqyFRz6qpHORNmayiXKtTOq%2Bs1x9OVNyXL3%2FlnKsyeWj6Q%3D%3D',
    '_clsk': '1kk7a8y%7C1730547818062%7C34%7C0%7Cp.clarity.ms%2Fcollect',
    'FCNEC': '%5B%5B%22AKsRol_wcYFag815ORhKizu0QUT6rhHmaESgek7fu-wt-6Ks0yBs_XNvpNufVBVj116BdOXRCblXvWNaMXkQuPZp_AqydgrWdiDSTwK8x-L3BNIbzxWSQQLyZ0guEzcx3yEqdZpEM3Pnz32xUyjbqjPcPQKUkNCmyg%3D%3D%22%5D%5D',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://grabcad.com/dashboard',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

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
    "download.prompt_for_download": True,                    # Disable any "Save As" dialogs
    "download.directory_upgrade": True,                       # Automatically overwrite existing directories
    "safebrowsing.enabled": False,                            # Disable safe browsing to prevent interruptions
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


def check_status_code(website, selenium_cookies):
    session = requests.Session()
    
    # Add Selenium cookies to the requests session
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    response = session.get(website)
    
    if not response.ok:
        raise Exception('Failed to fetch the webpage')

    return response.status_code
# print(check_status_code(website))


# To get elements of the webpage
def get_files(website, wd):
  k = []
  wd.get(website)
  get_data =  wd.find_elements(By.CLASS_NAME, 'modelCard')

  for i in get_data:
    k.append(i)
  return k


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

# Ensure `wd` is your Selenium WebDriver instance
if get_login_file(login_website, wd, email, password):
    print("Proceeding with the next steps after login.")
else:
    print("Aborting due to unsuccessful login.")

  
  # for i in login_get_data:
  #   l.append(i)
  # return l


# login_item_box = get_login_file('https://grabcad.com/login',wd)
# print(len(login_item_box))
# item_box = get_files(website, wd)
# print(len(item_box))
# print(item_box)
# print(item_box[0])


def get_page_urls():
    urls=[]
    # Let's scrap data for 2 pages
    for i in range(1,6):
        website='https://grabcad.com/library?page={}&per_page=100&time=all_time&sort=popular&categories=3d-printing'.format(*str(i))

        urls.append(website)
    return urls
    
def get_likes(item_box):
  count_tag = item_box.find_elements(By.CLASS_NAME, 'counts')
  like = count_tag[0].find_elements(By.TAG_NAME, 'span')[0].text

  return like

# print(get_likes(item_box))

# urls = (get_page_urls())
# print(urls)

# To get titles
def get_title(item_box):
  title_tag = item_box.find_elements(By.CLASS_NAME, 'modelInfo')
  title = title_tag[0].find_elements(By.TAG_NAME, 'a')[0].text
  return title

# print(get_title(item_box[2]))

def get_author(item_box):
  author_tag = item_box.find_elements(By.CLASS_NAME, 'author')
  
  author = author_tag[0].find_elements(By.TAG_NAME, 'a')[0].text

  return author

# Parse URL of the particular item_box

def get_url(item_box):
 
  url_tag = item_box.find_elements(By.CLASS_NAME, 'modelInfo')
  url = url_tag.get_attribute('href')

  return url

# print(get_url(item_box[2]))


# def get_pages_data():
#   pages = get_page_urls()
#   cad_models = {'Title':[],
#                 'Author':[],
#                 'URL':[],
#                 'Image_URL':[],
#                 }
#   for i in pages:
#     item_boxes = get_files(i, wd)
#     for item_box in item_boxes[1:]:

#       WebDriverWait(wd, 30).until(EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='text ng-binding']")))
      
#       cad_models['Title'].append(get_title(item_box))
#       cad_models['Author'].append(get_author(item_box))
#       cad_models['URL'].append(get_url(item_box))
#       return cad_models

def trigger_download_for_first(item_box, driver):
    
    try:
        # Check if item_box is empty
        if not item_box:
            print("Item box is empty. No elements to interact with.")
            return

        # Locate the download icon within the first element in item_box
        first_item = item_box[2]
        download_icon = WebDriverWait(first_item, 20).until(
            EC.presence_of_element_located((By.XPATH, './/span[contains(@class, "gc-icon-download")]'))
        )
        print("Download icon found:", download_icon)

        # Scroll to the download icon
        driver.execute_script("arguments[0].scrollIntoView(true);", download_icon)
        print('Scroll into view executed successfully.')

        # # Wait until the download icon is clickable, then click it
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'gc-icon-download')))
        print('Download icon is clickable.')

        # Click the download icon to start download
        driver.execute_script("arguments[0].click();", download_icon)
        print("Download triggered successfully for the first item.")

    except TimeoutException:
        print("Timeout: Download icon did not load in time.")
    except NoSuchElementException:
        print("Failed to trigger download: Download icon not found.")
    except ElementClickInterceptedException:
        print("Failed to trigger download: Element click intercepted.")
    except StaleElementReferenceException:
        print("Failed to trigger download: Element became stale during interaction.")
    except Exception as e:
        print("An unexpected error occurred:", e)



# Assuming `item_box` and `driver` are already defined and p
# item_box = get_files(website, wd)  # Assuming this returns a list of web elements
def get_downloads(item_box):
  count_tag = item_box.find_elements(By.CLASS_NAME, 'counts')

  for downloads in count_tag:
    download = downloads.find_elements(By.TAG_NAME, 'span')[3].text

  return download

download_folder = "./models"
driver = setup_driver()
item_box = get_files(website, wd)
print("Length of itembox is :",len(item_box),type(item_box))
trigger_download_for_first(item_box, wd)




# print("Started download function!")
# print(trigger_download_for_first(item_box[1],driver))
# print("downloaded files")

# Quit the driver when done
driver.quit()