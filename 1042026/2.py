import json
import jmespath

with open("air_bnb.json","r",encoding="utf-8") as f:
    data = json.load(f)

start = jmespath.search("niobeClientData[0][1].data.presentation.stayProductDetailPage.sections.sections[20].section",data)
title = jmespath.search("title",start)
seeAllAmenitiesGroups = jmespath.search("seeAllAmenitiesGroups[].{ category : title, amenities: amenities[].title }",start)



Final = {}
Final['title'] = title
Final["amenities"] = seeAllAmenitiesGroups


with open("2output.json","w",encoding="utf-8") as f:
    json.dump(Final,f,indent=2)