# practice on parsel

import requests
from parsel import Selector

url = "https://books.toscrape.com/"

response = requests.get(url)

#with open("books.html","w",encoding="utf-8") as f:
#   f.write(response.text)

sel = Selector(response.text)

title = sel.xpath("//title/text()")

links = sel.xpath("//a/@href").getall()

books = sel.xpath("//article[@class='product_pod']")
print(len(books))


for book in books:
    title = book.xpath(".//h3/a/@title").get()
    price = book.xpath(".//p[@class = 'price_color']/text()").get()

    print(title,price)

