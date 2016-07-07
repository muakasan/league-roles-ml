import json, requests, dotenv, os

dotenv.load_dotenv('.env')

jMatchStng = open('seed-files/matches1.json').read()
jMatch = json.loads(jMatchStng)

matches = jMatch['matches']

for m in matches:
	for p in m['participants']:
		lane = p['timeline']['lane']
		role = p['timeline']['role']
		items = [ p['stats']['item'+str(i)] for i in range(1, 7) ]

#Items Corresponding to Summoner's Rift
rItems = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/item', params = {'itemListData': 'maps', 'api_key': os.environ['API_KEY']})
jItems = json.loads(rItems.text)

itemsSR = []
for k, v in jItems['data'].items():
	itemsSR += [k] if v['maps']['11'] else [] #Map 11 is New Summoner's Rift

print(len(itemsSR))

