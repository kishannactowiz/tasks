from urllib.parse import urljoin
import requests
from lxml import html
import mysql.connector

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="books_db"
)
cursor = conn.cursor()

url = "https://books.toscrape.com/"

while True:
    #print("Scraping:", url)

    response = requests.get(url)
    if response.status_code != 200:
        break

    tree = html.fromstring(response.content)

    titles = tree.xpath("//h3/a/@title")
    links = tree.xpath("//h3/a/@href")

    for i in range(len(titles)):
        title = titles[i]
        link = links[i]

        full_link = urljoin(url, link)

        query = "INSERT INTO books_link (books_title, books_link) VALUES (%s, %s)"
        cursor.execute(query, (title, full_link))

    #  dynamic pagination
    next_page = tree.xpath("//li[@class='next']/a/@href")

    if next_page:
        url = urljoin(url, next_page[0])
    else:
        break

# commit once
conn.commit()

cursor.close()
conn.close()

print("Done!")

