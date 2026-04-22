import requests
import json
from lxml import html

def pageData(url):
    headers= {
        "content-type":"text/html; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    }

    data = requests.get(url,headers=headers)

    if data.status_code == 200:
        return data.text
    else:
        None