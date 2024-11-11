import requests
import time
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

response = requests.get('https://grabcad.com/library?page=1&per_page=100&time=all_time&sort=popular&categories=3d-printing'
, cookies=cookies, headers=headers)

for _ in range(5):  # Adjust the range as needed
    print(response.status_code)
    time.sleep(2)  # Wait 2 seconds between requests
