
# practice on lxml and xpath


from lxml import etree

with open("index.html","r",encoding="utf-8") as f :
    content = f.read()

tree = etree.HTML(content)

# get product divs
products=tree.xpath("//div[contains(@class,'product')]")

result = []
for p in products:
    name = p.xpath(".//h2/text()")[0]
    price = p.xpath(".//span[@class = 'price']/text()")[0]

    result.append({
        "name":name,
        "price": price
    })
    
print(result)