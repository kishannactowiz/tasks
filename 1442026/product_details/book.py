import requests
from lxml import html
import mysql.connector


headers = {
     "content-type" : "text/html",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

data= requests.get('https://books.toscrape.com/',headers= headers,)

root = html.fromstring(data.content)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="books_db"
)

cursor = mydb.cursor()


if data.status_code == 200:
     
     cursor.execute("SELECT books_title,books_link FROM books_link")
     book = cursor.fetchall()

     for i in book:
          book_tile = i[0]
          book_url = i[1]

          #print(book_tile)
        
          data2 = requests.get(book_url,headers=headers)
          root2 = html.fromstring(data2.content)
