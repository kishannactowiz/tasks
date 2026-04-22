import requests
import json
from lxml import html
from request import pageData
import requests as re
from urllib.parse import urljoin
from db import create_db,insert_movie

def find_url(url):
    res = re.get(url)
    all_json = json.loads(res.text)
    return all_json


baseurl = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest"
headers = {
    'User-Agent': 'Mozilla/5.0'
}
movieLlist=[]

def movieUrl(url,i):
    # extract movie url
    pagedata = pageData(url)
    root = html.fromstring(pagedata)
    # first page
    if i ==1:
        # with open("first_page.html", "w", encoding="utf-8") as f:
        #     f.write(pagedata)

        i = i + 1
        # extract json from script
        scriptdata = root.xpath('string(//script[@type="application/ld+json"])')
        scriptjosndata = json.loads(scriptdata)
    # extract pagination info
        pageinfo = json.loads(root.xpath('string(//script[@id="pageInfo"])'))

    # extract movie list
        for movieItem in scriptjosndata.get("itemListElement").get("itemListElement"):
            movieLlist.append({
                "movieName":movieItem.get("name"),
                "url":movieItem.get("url")
            })
    # next page(api)
    else:
        scriptjosndata = json.loads(pagedata)
        pageinfo = scriptjosndata.get("pageInfo")

        for movieItem in scriptjosndata.get("grid", {}).get("list", []):
            movieLlist.append({
                "name":movieItem.get("title"),
                "url": "https://www.rottentomatoes.com" + movieItem.get("mediaUrl")
            })

    if pageinfo:
        # pagination
        apidata = pageinfo.get("endCursor")
        if apidata:
            newurl = f"https://www.rottentomatoes.com/cnapi/browse/movies_in_theaters/sort:newest?after={apidata}"
            movieUrl(newurl, i)

    return movieLlist   


movieUrl(baseurl,1)
print(len(movieLlist))

with open("finalmovieList.json","w",encoding="utf-8")as f :
    json.dump(movieLlist,f)


def get_movie_data(movie_url):

    base_url =  "https://www.rottentomatoes.com"
    # get page
    res = re.get(movie_url,headers= headers)
    tree = html.fromstring(res.text)
    
    movie_name= tree.xpath("string(//rt-text[@size='1.25,1.75']/text())")


    image_list = tree.xpath("//rt-img[@slot='poster']/@srcset")
    image = image_list[0].split()[0] if image_list else None

    if image and "/v2/" in image:
        image = image.split("/v2/")[-1]

    
    tometometer = tree.xpath("string(//rt-text[@slot='critical-score'])") or '0%'

    popcornmeter_list = tree.xpath(".//div[contains(@class,'media-scorecard')]//rt-text/text()")
    popcornmeter = popcornmeter_list[2] if len(popcornmeter_list) > 2 else None

    review_count_list = tree.xpath(".//div[contains(@id,'movie-overview')]//rt-link//text()")
    review_count = int(review_count_list[0].split()[0].strip()) if review_count_list else 0

    description = tree.xpath("string(//div[@slot='description']//rt-text/text())").strip()

    whatToknow = tree.xpath("string(//div[@id='critices-consensus']//p)").strip()

    cast_link_list = tree.xpath(".//section[contains(@class,'cast-and-crew')]//rt-button/@href")
    cast_crew_link = urljoin(base_url, cast_link_list[0]) if cast_link_list else None

    cast_and_crew = []

    if cast_crew_link:
        res1 = re.get(cast_crew_link)
        tree1= html.fromstring(res1.text)

        cast_cards = tree1.xpath('.//cast-and-crew-card')

        for card in cast_cards:
            name = card.xpath('.//rt-text[@slot="title"]/text()')
            img_list = card.xpath(".//rt-img[@slot='poster']/@src")
            img = img_list[0].strip() if img_list else None

            credit = card.xpath(".//rt-text[@slot='credits']/text()")
            credit_string = ",".join(credit)

            cast_and_crew.append({
                'name': name,
                'img': img,
                'credit': credit_string
            })

    video_href = tree.xpath("string(//rt-button[@data-qa='videos-view-all-link']/@href)")
    video_main_href = urljoin(base_url,video_href)

    request_video = re.get(video_main_href,headers= headers)
    tree3 = html.fromstring(request_video.text)

    videos =[]

    video_xpath= tree3.xpath("//div[@data-qa='video-item']")

    for v in video_xpath:
        title = v.xpath(".//a[@data-qa='video-item-title']/text()")
        link = v.xpath(".//a[@data-qa='video-item-title']/@href")
        duration = v.xpath(".//span[@data-qa='video-item-duration']/text()")
        thumbnail = v.xpath(".//img[@data-qa='video-img']/@srcset")

        videos.append({
            "title":title[0].strip() if title else None,
            "url":urljoin(baseurl,link[0]) if link else None,
            "duration":duration[0].strip() if duration else None,
            "numbnail":thumbnail[0] if thumbnail else None
        })


    # reviews
    all_reviews= []

    
    reviews_href = tree.xpath("string(//section[@aria-labelledby='critics-reviews-label']//rt-button/@href)").strip()

    if reviews_href:

        reviews = re.get(urljoin(base_url,reviews_href),headers = headers)
        review_tree = html.fromstring(reviews.text)

        json_obj = review_tree.xpath("//script[@data-json='props']/text()")

        if json_obj:
            json_obj_2 = json.loads(json_obj[0])

            page_id = json_obj_2.get('media', {}).get('emsId')
            # build api
            review_url = f"https://www.rottentomatoes.com/napi/rtcf/v1/movies/{page_id}/reviews?after=&before=&pageCount=20&topOnly=false&type=critic&verified=false"

            review_data = find_url(review_url)

            for i in (review_data.get('reviews') or []):
                all_reviews.append({
                    'name':(i.get('critic') or {}).get('display'),
                    'review': i.get('reviewQuote'),
                    'review_count':i.get('originalScore'),
                    'review_type':i.get('scoreSentiment')
                })

    data = {
        'movie_name':movie_name,
        'score':tometometer,
        'desc':description,
        'img':image,
        'review_count':review_count,
        'videos':videos,
        'want_to_know':whatToknow,
        'cast':cast_and_crew,
        'all_reviews':all_reviews,
    }

    print(f"{data.get('movie_name')} was added.")
    return data


create_db()

all_url = movieUrl(baseurl,1)

for i in all_url:
    data = get_movie_data(i["url"])

    insert_movie(data)   #  INSERT INTO DB

    print("Inserted into DB")

       # remove later if you want all movies