import requests, os, dotenv, json
dotenv.load_dotenv('.env')

f = open("itemsJSON.js", "w+")
f.write("var itemsJSON =\n")

rItems = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/item', params = {'itemListData': 'maps', 'api_key': os.environ['API_KEY']})
jItems = json.loads(rItems.text)

namesToId = dict() 

for k, v in jItems['data'].items():
    if v['maps']['11'] and "name" in v: #Map 11 is New Summoner's Rift
        namesToId[v['name']] = v['id']

f.write(json.dumps(namesToId))  

f.close()

