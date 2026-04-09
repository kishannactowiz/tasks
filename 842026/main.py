import json
from validation import Restaurant


with open("zometo.json",'r') as f :
    data = json.load(f)


sections = data.get("page_data", {}).get("sections", {})
basic = sections.get("SECTION_BASIC_INFO", {})
contact = sections.get("SECTION_RES_CONTACT", {})
header = sections.get("SECTION_RES_HEADER_DETAILS", {})
menu_data = data.get("page_data", {}).get("order", {}).get("menuList", {}).get("menus", [])


restaurant_id = basic.get("res_id",0)
restaurant_name = basic.get("name")
restaurant_url = "https://www.zomato.com" + basic.get("resUrl")

restaurant_contact = []
phone = contact.get("phoneDetails").get("phoneStr")
if phone:
    restaurant_contact.append(phone)

fssai_licence_number = ""


# address
address_info = {
    "full_address": contact.get("address"),
    "region" : contact.get("country_name"),
    "pincode": contact.get("zipcode"),
    "city": contact.get("city_name"),
    "state": "Gujarat"
}

# cuisines
cuisines= []

for c in header.get("CUISINES"):
    cuisines.append({
        "name" : c.get("name"),
        "url": c.get("url")
    })

# timing

timing_str = basic.get("timing").get("customised_timings").get("opening_hours",[{}])[0].get("timing").replace("â€“", "-")

open_time = ""
close_time = ""

if "-" in timing_str:
    parts = timing_str.split("-")
    open_time = parts[0].strip()
    close_time = parts[1].strip()

timing = {
    day:{"open":open_time, "close":close_time}
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

}

# menu

menu_categories= []

for menu in menu_data:
    menu_name = menu.get("menu",{}).get("name","")
    categories = menu.get("menu").get("categories")

    items_list = []
    for cat in categories:
        for item_data in cat.get("category").get("items"):
            item = item_data.get("item")

            item_id = item.get("id")
            item_name = item.get("name")
            item_desc = item.get("desc")

            # check for veg
            is_veg = "veg" in item.get("dietary_slugs")

            items_list.append({
                "item_id": item_id,
                "item_name":item_name,
                "item_slugs": item.get("tag_slugs",[]),
                "item_url":"",
                "item_description" : item_desc,
                "item_price" : 0.0,
                "is_veg": is_veg})

    menu_categories.append({
        "category_name":menu_name,
        "items": items_list
    })

final_output = {
    "restaurant_id": restaurant_id,
    "restaurant_name": restaurant_name,
    "restaurant_url": restaurant_url,
    "restaurant_contact": restaurant_contact,
    "fssai_licence_number": fssai_licence_number,
    "address_info": address_info,
    "cuisines": cuisines,
    "timings": timing,
    "menu_categories": menu_categories
}

try:
    validated_data = Restaurant(**final_output)
    print("validation Success")
except Exception as e :
    print("validation error:", e)

with open("zometo_output.json","w") as f:
    json.dump(final_output,f,indent=2)

print("done")

