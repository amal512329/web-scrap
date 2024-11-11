import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver  # Use for handling requests and injecting cookies
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the WebDriver options
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("window-size=1200x600")

# Service setup (update path to your Chromedriver)
service = Service("./chromedriver/chromedriver.exe")
wd = webdriver.Chrome(service=service, options=options)

# Define the cookies dictionary with your provided cookies
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
    'FCNEC': '%5B%5B%22AKsRol_wcYFag815ORhKizu0QUT6rhHmaESgek7fu-wt-6Ks0yBs_XNvpNufVBVj116BdOXRCblXvWNaMXkQuPZp_AqydgrWdiDSTwK8x-L3BNIbzxWSQQLyZ0guEzcx3yEqdZpEM3Pnz32xUyjbqjPcPQKUkNCmyg%3D%3D%22%5D%5D'
}

# Load the site
login_website = 'https://grabcad.com'
wd.get(login_website)
time.sleep(3)  # Allow time for initial page load

# Inject each cookie
for name, value in cookies.items():
    wd.add_cookie({"name": name, "value": value})

# Access restricted page to verify login
restricted_url = 'https://grabcad.com/dashboard'
wd.get(restricted_url)
time.sleep(3)

# Check if login was successful by confirming presence of a dashboard element
try:
    WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dashboard-header"))  # Adjust based on actual element
    )
    print("Login successful! Accessed the dashboard.")
except Exception as e:
    print("Failed to access dashboard. Login likely unsuccessful:", e)

wd.quit()
