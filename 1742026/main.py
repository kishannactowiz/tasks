import requests
import json
import jmespath
from lxml import html

url= "https://www.igus.in/iglidur-ibh/sleeve-bearings/product-details/iglidur-glw-m?artnr=GLWSM-1012-10"

header = {
    "content-type": "text/html",
    "User-Agent": "Mozilla/5.0"
}

#data = requests.get(url,headers=header)
with open("igus.json","r",encoding="utf-8") as f:
    data = json.load(f)


root = html.fromstring(data.content)

information = root.xpath("//main[contains(@class,'block container my-8 text-base font-normal text-gray-500 bg-white')]")

json_data =root.xpath("//script[@type='application/json']/text()")

raw_json = json_data[0]
    
json_data2= json.loads(raw_json)

with open("igus.json", "w",encoding="utf-8") as f:
    json.dump(json_data2, f,indent=4)
    
start = jmespath.search("props.pageProps",data)


image_url=jmespath.search("props.pageProps.akeneoProductData.assets[4].sources[0].uri",json_data2)

product_image = jmespath.search("props.pageProps.akeneoProductData.assets[5].sources[0].uri",json_data2)

part_number = jmespath.search("props.pageProps.akeneoProductData.attributes.part_number.value",json_data2)
    
Material= jmespath.search("articleData.material.name",json_data2)    
shape = jmespath.search("props.pageProps.nextI18Next.useConfig.resources.en.bearing-hub/bearingHub.SHAPES.S.TITLE",json_data2)

Manufacturing_method =jmespath.search("props.pageProps.nextI18Next.userConfig.resources.en.bearinghub/bearingHub.PRODUCTION_METHODS.CATALOG_PART",json_data2)
    
Material= jmespath.search("articleData.material.name",root).strip()

Shape = jmespath.search('_nextI18Next.userConfig.resources.en."bearing-hub/bearingHub".SHAPES.S.TITLE',start)
Dimensions = jmespath.search("articleData.dimensions",start)
DimensionsObject = {}
for k,v in Dimensions.items():
    DimensionsObject[k] = f"{v} mm"

manufacturing_method = jmespath.search('_nextI18Next.userConfig.resources.en."bearing-hub/bearingHub".PRODUCTION_METHODS.MOLD_INJECTION',start)

material_properties_str_list = html.fromstring(str(jmespath.search("akeneoProductData.attributes.attr_USP.value",start)).strip())
material_properties = material_properties_str_list.xpath("//li/text()")

total_price = round(float(jmespath.search("articleData.totalPrice.value",start)),2)
print(total_price)


product_description = html.fromstring(jmespath.search("akeneoProductData.attributes.attr_description.value",root))
product_description = " ".join(product_description.xpath(".//text()"))

technicalDataCategories = jmespath.search("technicalDataCategories",root)

technical_data={}
for item in technicalDataCategories:
   d={}
   for attribute in item.get("attributes"):
       key=attribute.get("description").strip()
       value=attribute.get("value") 
       d[key] = value
    
   technical_data[item.get("name")] = d

finalObject = {
    "images": imageObject,
    "part_number": part_number,
    "material" : Material,
    "shape" : Shape,
    "dimensions" : DimensionsObject,
    "properites" : material_properties,
    "total_price" : total_price, 
    "product_description" : product_description,
    "technical_data" : technical_data
}   

with open("data_scrap.json","w",encoding="utf-8") as f:
    json.dump(finalObject,f)














    # description = jmespath.search("props.pageProps.akeneoProductData.attributes.attr_description.value",json_data2 )

    # clean = html.fromstring(description)
    # text = clean.text_content()
    # text = " ".join(text.split())
    # # clean = description.replace("<br />","\n")
    # # clean = re.sub(r"<.*?>","",clean)
    # print(text)
