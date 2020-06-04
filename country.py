import json

dic = {}
with open('countries.json') as json_file:
    countries = json.load(json_file)
    for country in countries:
        dic[country["alpha2"].upper()] = country["name"]

# Serializing json  
json_object = json.dumps(dic, indent = 4) 
with open('country2.json', 'w') as json_file:
    json_file.write(json_object) 