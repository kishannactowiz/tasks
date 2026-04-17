import requests
from lxml import html
import mysql.connector

# DB connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="books_db"
)

cursor = mydb.cursor()

base_url = "https://books.toscrape.com/"

# total 50 page
for page in range(1, 51):

    print(f"Scraping page {page}")

    if page == 1:
        url = base_url
    else:
        url = base_url + f"catalogue/page-{page}.html"

    response = requests.get(url)

    if response.status_code != 200:
        break

    tree = html.fromstring(response.content)

    titles = tree.xpath("//h3/a/@title")
    links = tree.xpath("//h3/a/@href")

    for i in range(len(titles)):
        title = titles[i]
        link = links[i]

        full_link = base_url + link.replace("../../../", "")

        query = "INSERT INTO books (books_title, books_link) VALUES (%s, %s)"
        cursor.execute(query, (title, full_link))

# commit once
mydb.commit()

cursor.close()
mydb.close()

print("Done!")