import requests
import json
from lxml import html



def getPageData(url):
    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "content-type":"text/html; charset=utf-8"
    }
    data = requests.get(url,headers=headers)
    if data.status_code == 200:
        return data.text
    else:
        return None