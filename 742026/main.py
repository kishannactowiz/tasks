import json
from validation import Product

with open("bonker.json", "r") as f:
    data = json.load(f)

base_url = "https://www.bonkerscorner.com/products/"

def format_price(price):
    return round(price / 100, 2)

def extract_p_name(handle):
    return handle.replace("-", " ").title()

output = []

for product in data["products"]:
    handle = product["handle"]
    product_name = extract_p_name(handle)
    product_url = f"{base_url}{handle}"

    variants = product["variants"]

    variant_list = []
    option_values = []

    for v in variants:
        size = v.get("public_title")

        if size not in option_values:
            option_values.append(size)

        variant_list.append({
            "variantName": size,
            "variantID": v["id"],
            "variantUrl": f"{product_url}?variant={v['id']}",
            "variantPrice": format_price(v["price"])
        })

    structured_product = {
        "productName": product_name,
        "vender": product["vendor"].replace("Corner", ""),
        "productUrl": product_url,
        "productPrice": format_price(variants[0]["price"]),
        "variantCount": len(variants),
        "variantopetions": [
            {
                "optionName": "Size",
                "optionValues": option_values
            }
        ],
        "variants": variant_list
    }

    # ✅ Pydantic validation
    try:
        validated = Product(**structured_product)
        output.append(validated.model_dump())
    except Exception as e:
        print("Validation Error:", e)

# save output
with open("output.json", "w") as f:
    json.dump(output, f, indent=2)

print("saved to output.json")