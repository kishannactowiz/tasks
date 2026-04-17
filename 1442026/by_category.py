import requests
from lxml import html
from urllib.parse import urljoin
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="books_db"
)

cursor = conn.cursor()

url = "https://books.toscrape.com/"

headers = {
     "content-type" : "text/html",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

data = requests.get(url, headers=headers)
root = html.fromstring(data.content)

if data.status_code == 200:

    
    cursor.execute("SELECT categories_name, categories_link FROM categories")
    categories = cursor.fetchall()

    for cat in categories:
        category_name = cat[0]
        category_url = cat[1]
        data2 = requests.get(category_url, headers=headers)
        root2 = html.fromstring(data2.content)

#         # get total pages
        page = root2.xpath("//ul[@class='pager']/li[@class='current']/text()")
        print(page)
        if len(page) > 0:
            pages = int(page[0].split()[-1])   

            
            for page_num in range(1, pages + 1):

                page_url = category_url.replace("index.html", f"page-{page_num}.html")

                data3 = requests.get(page_url, headers=headers)
                root3 = html.fromstring(data3.content)

                book_name = root3.xpath("//h3/a/@title")
                book_link = root3.xpath("//h3/a/@href")

                for j in range(len(book_name)):
                    temp = book_name[j].strip()

                    newurl = urljoin(category_url, book_link[j])

                    cursor.execute("""
                        INSERT INTO books_with_category (book_name, book_url, category_name)
                        VALUES (%s, %s, %s)
                    """, (temp, newurl, category_name))

        else:
            book_name = root2.xpath("//h3/a/@title")
            book_link = root2.xpath("//h3/a/@href")

            for j in range(len(book_name)):
                temp = book_name[j].strip()

                
                newurl = urljoin(category_url, book_link[j])

                cursor.execute("""
                    INSERT INTO books_with_category (book_name, book_url, category_name)
                    VALUES (%s, %s, %s)
                """, (temp, newurl, category_name))

conn.commit()

cursor.close()
conn.close()

print("Done!")