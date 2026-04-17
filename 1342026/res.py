import requests


param = {
    "name": "Bob",
    "age": 25

}
response = requests.get("http://httpbin.org/get" ,params=param)


res_json = response.json()
print(res_json)
