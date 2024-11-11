from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
import shutil
import requests  # Added requests for authenticated URL fetching
from urllib.parse import urljoin

app = Flask(__name__)
CORS(app)

download_folder = "downloaded_files"
os.makedirs(download_folder, exist_ok=True)

def fetch_webpage(url, headers=None, cookies=None):
    """Fetch webpage content with optional headers and cookies for authenticated access."""
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        return response.text
    return None

async def download_file(session, file_url, folder, filename, retries=3):
    os.makedirs(folder, exist_ok=True)
    for attempt in range(retries):
        try:
            async with session.get(file_url) as response:
                if response.status == 200:
                    content_length = response.headers.get('Content-Length')
                    data = await response.read()
                    if content_length and len(data) != int(content_length):
                        raise ValueError("Incomplete file download.")
                    
                    file_path = os.path.join(folder, filename)
                    with open(file_path, 'wb') as f:
                        f.write(data)
                    return
        except (aiohttp.ClientError, ValueError):
            await asyncio.sleep(2)
    print(f"Failed to download file after {retries} attempts: {file_url}")

async def download_images(session, soup, base_url):
    folder_images = "downloaded_files"
    tasks = []
    images = soup.find_all("img")
    print('Image Tags Found')
    for index, img in enumerate(images):
        img_url = urljoin(base_url, img.get("src"))
        filename = f"image_{index}.jpg"
        tasks.append(download_file(session, img_url, folder_images, filename))
    await asyncio.gather(*tasks)

async def download_videos(session, soup, base_url):
    folder_videos = "downloaded_files"
    tasks = []
    videos = soup.find_all("video")
    for index, video in enumerate(videos):
        video_url = video.get("src")
        if video_url:
            filename = f"video_{index}.mp4"
            tasks.append(download_file(session, urljoin(base_url, video_url), folder_videos, filename))
    await asyncio.gather(*tasks)

async def download_3d_models(session, soup, base_url):
    folder_models = "downloaded_files"
    model_extensions = ['.glb', '.gltf', '.stl', '.obj', '.fbx']
    tasks = []
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href and any(href.endswith(ext) for ext in model_extensions):
            filename = os.path.basename(href)
            tasks.append(download_file(session, urljoin(base_url, href), folder_models, filename))
    await asyncio.gather(*tasks)

async def scrape_data(url, headers, cookies):
    """Scrapes data with provided headers and cookies for authentication."""
    html = fetch_webpage(url, headers=headers, cookies=cookies)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(
                download_images(session, soup, url),
                download_videos(session, soup, url),
                download_3d_models(session, soup, url)
            )

@app.route('/api/scrape', methods=['POST'])
async def scrape():
    """Scrape endpoint that accepts URL, headers, and cookies from the request."""
    data = request.get_json()
    url = data.get("url")
    print("The url :",url)
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'optimizelyEndUserId=oeu1730540661524r0.6422308138616348; optimizelySegments=%7B%22239451939%22%3A%22gc%22%2C%22239653413%22%3A%22false%22%2C%22239748770%22%3A%22search%22%7D; optimizelyBuckets=%7B%7D; _biz_uid=9422146f11a94cd3ffee705c81d1ebff; _ga=GA1.1.1080506923.1730540663; _clck=nb67dw%7C2%7Cfqj%7C0%7C1767; _mkto_trk=id:533-LAV-099&token:_mch-grabcad.com-1730540664316-91933; _biz_flagsA=%7B%22Version%22%3A1%2C%22XDomain%22%3A%221%22%2C%22ViewThrough%22%3A%221%22%2C%22Mkto%22%3A%221%22%2C%22Frm%22%3A%221%22%7D; _grabcad_session=459b89a54e47a6455ab4065cfaf7e2cc; _biz_nA=28; XSRF-TOKEN=OX5bZk3lRosPS%2B4wMbH6BjiZtLlZpRGDk1KK7UokQ00zDZQBk6BbyhaNuZugXuWfZ6FPCyArSFUB8X7YIxbWCA%3D%3D; _ga_173TDQJFJ7=GS1.1.1730540662.1.1.1730549620.60.0.0; _biz_pendingA=%5B%5D; __gads=ID=e0c071270444e27f:T=1730540888:RT=1730549622:S=ALNI_MbntfvGQ1ugZfUpfzunon4xEUi6xA; __gpi=UID=00000f4d00493d3c:T=1730540888:RT=1730549622:S=ALNI_Mb85B9I2AkHTdzRuIfs6W_skeQBWA; __eoi=ID=9a5f6798ee5a177d:T=1730540888:RT=1730549622:S=AA-AfjblGJZ6y5_JzghQH-PwdLZK; FCNEC=%5B%5B%22AKsRol9QboKoVvO6KLlGWvjYoETWH8-TeNOyLzRntCim9FLIvsDPbz2s1laetm4BYYtZTqm8dL17BXZyANvw8dWGExqI5IQ-lpzJfPfURdObOf1N_w-xzXdtAwAkLtVGD-1x3IHtlBQaMdfBGUoqXDQ3dBDlz-7y3g%3D%3D%22%5D%5D',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}
    cookies={
    'optimizelyEndUserId': 'oeu1730540661524r0.6422308138616348',
    'optimizelySegments': '%7B%22239451939%22%3A%22gc%22%2C%22239653413%22%3A%22false%22%2C%22239748770%22%3A%22search%22%7D',
    'optimizelyBuckets': '%7B%7D',
    '_biz_uid': '9422146f11a94cd3ffee705c81d1ebff',
    '_ga': 'GA1.1.1080506923.1730540663',
    '_clck': 'nb67dw%7C2%7Cfqj%7C0%7C1767',
    '_mkto_trk': 'id:533-LAV-099&token:_mch-grabcad.com-1730540664316-91933',
    '_biz_flagsA': '%7B%22Version%22%3A1%2C%22XDomain%22%3A%221%22%2C%22ViewThrough%22%3A%221%22%2C%22Mkto%22%3A%221%22%2C%22Frm%22%3A%221%22%7D',
    '_grabcad_session': '459b89a54e47a6455ab4065cfaf7e2cc',
    '_biz_nA': '28',
    'XSRF-TOKEN': 'OX5bZk3lRosPS%2B4wMbH6BjiZtLlZpRGDk1KK7UokQ00zDZQBk6BbyhaNuZugXuWfZ6FPCyArSFUB8X7YIxbWCA%3D%3D',
    '_ga_173TDQJFJ7': 'GS1.1.1730540662.1.1.1730549620.60.0.0',
    '_biz_pendingA': '%5B%5D',
    '__gads': 'ID=e0c071270444e27f:T=1730540888:RT=1730549622:S=ALNI_MbntfvGQ1ugZfUpfzunon4xEUi6xA',
    '__gpi': 'UID=00000f4d00493d3c:T=1730540888:RT=1730549622:S=ALNI_Mb85B9I2AkHTdzRuIfs6W_skeQBWA',
    '__eoi': 'ID=9a5f6798ee5a177d:T=1730540888:RT=1730549622:S=AA-AfjblGJZ6y5_JzghQH-PwdLZK',
    'FCNEC': '%5B%5B%22AKsRol9QboKoVvO6KLlGWvjYoETWH8-TeNOyLzRntCim9FLIvsDPbz2s1laetm4BYYtZTqm8dL17BXZyANvw8dWGExqI5IQ-lpzJfPfURdObOf1N_w-xzXdtAwAkLtVGD-1x3IHtlBQaMdfBGUoqXDQ3dBDlz-7y3g%3D%3D%22%5D%5D',
}

    if not url:
        return jsonify({"error": "URL is required"}), 400

    await scrape_data(url, headers, cookies)
    return jsonify({"message": "Data fetched and saved successfully"})

@app.route('/api/save_location', methods=['POST'])
def save_location():
    data = request.get_json()
    location = data.get("location")

    if not location:
        return jsonify({"error": "Location path is required"}), 400
    
    try:
        os.makedirs(location, exist_ok=True)
        for file in os.listdir("downloaded_files"):
            src_file = os.path.join("downloaded_files", file)
            dst_file = os.path.join(location, file)
            
            if os.path.exists(dst_file):
                os.remove(dst_file)
                
            shutil.move(src_file, dst_file)
        
        return jsonify({"message": "Files saved successfully at the specified location"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to save files"}), 500

if __name__ == "__main__":
    app.run(debug=True)
