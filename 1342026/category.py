import mysql.connector
from lxml import html
import requests
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'actowiz',
    database = 'books_db'
)

cursor = conn.cursor()


response=requests.get('https://books.toscrape.com/')
print(response.status_code)


#with open("books.html","w",encoding="utf-8") as f:
 #   f.write(response.text)


# convert to OBJECT

tree = html.fromstring(response.content)


# apply xpath

categories = tree.xpath("//ul[@class='nav nav-list']/li/ul/li/a")


#all_books_links = tree.xpath("//div[@class='row']//h3//text()")

base_url= "https://books.toscrape.com/"

categories_data = []

for cat in categories:
    name= cat.xpath("text()")[0].strip()
    link = cat.xpath("@href")[0]

    full_link = base_url + link
    query = "insert into categories(categories_link,categories_name) values(%s,%s)"
    values = (full_link,name)

    cursor.execute(query,values)

# commit change
conn.commit()


# cursor.close()
# conn.close()

# for book
cursor.execute("select categories_link from categories")
category_links = cursor.fetchall()

book_base = "https://books.toscrape.com/catalogue/"
 
for (category_link,) in category_links:

    page_url = category_link

    while True:
        response = requests.get(page_url)
        print(page_url)

        if response.status_code != 200:
            break

        tree = html.fromstring(response.content)

        # book links
        books = tree.xpath("//h3/a")
        
        for book in books:
            title = book.xpath('@title')[0]
            link = book.xpath('@href')[0]


            full_link = book_base + link.replace("../../../", "")

            query = 'insert into books(books_title,book_link) values(%s,%s)'
            values = (title,full_link)

            cursor.execute(query,values)

        #print("done",page_url)

        # pagination
        next_page = tree.xpath("//li[@class='next']/a/@href")

        if next_page:
            next_url = next_page[0]

            if "catalogue/category" in page_url:
        # correct joining
                page_url = page_url.rsplit('/', 1)[0] + '/' + next_url
            else:
                page_url = base_url + next_url
        else:
            break

conn.commit()
cursor.close()
conn.close()
   




