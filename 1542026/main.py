import requests
from lxml import html
import json
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="music_db"
)


cursor = mydb.cursor()
headers = {
     "content-type" : "text/html",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

url = "https://www.billboard.com/charts/hot-100/"
data = requests.get(url,headers=headers)

print(data.status_code)

#with open("billboard.html","w",encoding="utf-8") as f:
#    f.write(data.text)

if data.status_code == 200:

    root =html.fromstring(data.content)

    all_data = root.xpath("//div[contains(@class,'chart-results-list')]/div[@class = 'o-chart-results-list-row-container']")
    final_data =[]
    for item in all_data:
        eachitem = item.xpath("ul[contains(@class,'o-chart-results-list-row')]/li")
        image_url = eachitem[1].xpath("//img/@src")[0]
        song_name = eachitem[3].xpath(".//h3//text()")[0].strip()
        artist_name = eachitem[3].xpath(".//span//text()")[0].strip()

        rightsection= eachitem[3].xpath("//div[@class ='lrv-u-flex']//li//span//text()")
        lw = rightsection[0].strip()
        if lw == '-':
            lw= None
        else: 
            lw = int(lw)
        peak = rightsection[1].strip()
        week = rightsection[2].strip()
        item_expend = item.xpath(".//div[contains(@class,'charts-results-item-detail-inner')]/div")

        Debut_position=item_expend[0].xpath('div[@class="o-chart-position-stats__debut"]//div//span//text()')[0].strip()
        debutChartDate = item_expend[0].xpath('div[@class="o-chart-position-stats__debut"]/div/div/span/a/text()')[0].strip()

        peakPosition = item_expend[0].xpath('div[@class="o-chart-position-stats__peak"]/div/span/text()')[0].strip()
        peakChartDate = item_expend[0].xpath('div[@class="o-chart-position-stats__peak"]/div/div/span/a/text()')[0].strip()
        
        awardLists = item_expend[1].xpath('div[@class="o-chart-awards-list"]/div')
        finalawardList = ""
        if awardLists:
            for award in awardLists:
                awardname = award.xpath('.//p/text()')
                if awardname:
                    finalawardList += awardname[0] + ", "
        
        billboard = {
                    "song_name": song_name,
                    "artist_name":artist_name,
                    "image_url": image_url,
                    "lw":lw,
                    "peak":peak,
                    "weeks": week,
                    'debut_position':Debut_position,
                    'debut_charDate':debutChartDate,
                    "peak_position": peakPosition,
                    "finalAwardList":finalawardList

                }
        final_data.append(billboard)

#                 print(finalawardList)
# print(len(item_expend))

# cursor.execute("""
#  INSERT INTO billboard_top_100 (song_name, artist_name, image_url, lw, peak, weeks, debut_position, debut_chart_date, peak_position, peak_chart_date, awards)
#  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# """, (song_name, artist_name, image_url, lw, peak, week, Debut_position, debutChartDate, peakPosition, peakChartDate, finalawardList))
# #  print(artistName)

# mydb.commit()
# cursor.close()
# mydb.close()

# billboard = {
#     "song_name": song_name,
#     "artist_name":artist_name,
#     "image_url": image_url,
#     "lw":lw,
#     "peak":peak,
#     "weeks": week,
#     'debut_position':Debut_position,
#     'debut_charDate':debutChartDate,
#     "peak_position": peakPosition,
#     "finalAwardList":finalawardList

# }

with open("output.json","w",encoding="utf-8") as f:
    json.dump(all_data,f,indent=2)
