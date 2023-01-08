import json

with open("test.json", mode="r", encoding="utf-8") as file:
   config=json.load(file)
print("name", config["name"])
print("cup", config["cup"])
print("kg", config["kg"])
print("參數", config["參數"])

config["name"] = "中文"
with open("test.json", mode="w") as file:
   json.dump(config,file)