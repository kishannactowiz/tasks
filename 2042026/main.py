import requests
import json
from lxml import html
from requestdata import getPageData

baseurl = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest"


finalmovielist = []
def fetchmovieurls(url,i):
    # print(f" i : {i}")
    pagedata = getPageData(url)
    root = html.fromstring(pagedata)
    if i == 1:
        i= i + 1
        scriptdata = root.xpath('string(//script[@type="application/ld+json"])')
        scriptjsondata  = json.loads(scriptdata)
        pageinfo = json.loads(root.xpath('string(//script[@id="pageInfo"])'))
        for movieitem in scriptjsondata.get("itemListElement").get("itemListElement"):
            finalmovielist.append({
                "name":movieitem.get("name"),
                "url" : movieitem.get("url")
            })
    else:
        # print(pagedata)
        scriptjsondata  = json.loads(pagedata)
        pageinfo = scriptjsondata.get("pageInfo")
        for movieitem in scriptjsondata.get("grid").get("list"):
            finalmovielist.append({
                "name":movieitem.get("title"),
                "url" : "https://www.rottentomatoes.com" + movieitem.get("mediaUrl")
            })

    if pageinfo:
        apidata = pageinfo.get("endCursor")
        if apidata:
            newurl = f"https://www.rottentomatoes.com/cnapi/browse/movies_in_theaters/sort:newest?after={apidata}"
            #print(newurl)
            fetchmovieurls(newurl,i)
        
fetchmovieurls(baseurl,1)
print(len(finalmovielist))
with open("outputfinal.json","w",encoding="utf-8") as f:
    json.dump(finalmovielist,f)

