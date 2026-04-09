import jmespath
import json

data = {
    "people": [
        {"name": "Alice", "age": 25, "city": "NY"},
        {"name": "Bob", "age": 30, "city": "LA"},
        {"name": "Charlie", "age": 35, "city": "NY"}
    ]
}




# access fields
result = jmespath.search("people[0].name",data)

all_data=data.get('people')
print(all_data)
for a in all_data:
    name=jmespath.search("a.name",result)
    print(name)


# print(result)

# # list projection(*)
# print(jmespath.search("people[*].name",data))

# #filtering(?)

# print(jmespath.search("people[?age > `30`].name",data))

# # multiple fields

# print(jmespath.search("people[*].{Name:name, Age: age}",data))

# # sorting

# print(jmespath.search("sort_by(people,&age)[].name",data))