import json
import requests
from lxml import html

headers = {
    "content-type": "text/html",
    "User-Agent": "Mozilla/5.0"
}

url = "https://www.maggi.in/en/product/maggi-2-minute-special-masala-instant-noodles/"

data = requests.get(url, headers=headers)

if data.status_code == 200:
    root = html.fromstring(data.content)

    rows = root.xpath("//div[contains(@class,'mg-freeze-table')]//tr")
    table_data = []

    for row in rows:

        th_data = row.xpath(".//th/text()")
        td_data = row.xpath(".//td/text()")
        print(th_data)
    
        cols = th_data + td_data
        
    
        clean_cols = []

        for c in cols:
            c = c.strip()
            if c:
                clean_cols.append(c)

        if clean_cols:
            table_data.append(clean_cols)
    
    header= table_data[0]
    data_row = table_data[1:]

    final_data={}

    for row in data_row:
        key = row[0]

        final_data[key] = {
            "per_100g": float(row[1]),
            "per_serve": float(row[2]),
            "gda": row[3],
            "rda": row[4]
        }
    with open("output2.json",'w',encoding="utf-8") as f:
        json.dump(final_data,f,indent=2)

