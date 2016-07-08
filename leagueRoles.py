import json, requests, dotenv, os, codecs
dotenv.load_dotenv('.env')

def itemListToVector(l, d):
    v = [0]*len(d.keys())
    for i in filter(lambda x: str(x) in d, l): #Filters out zeroes because of empty slots, and other items which no longer exist
        v[int(d[str(i)])] = 1
    return v

#Fetches from Riot API
def getItemDictionary():
    rItems = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/item', params = {'itemListData': 'maps', 'api_key': os.environ['API_KEY']})
    jItems = json.loads(rItems.text)

    itemsSR = []
    for k, v in jItems['data'].items():
        itemsSR += [k] if v['maps']['11'] else [] #Map 11 is New Summoner's Rift

    itemIdToIndex = {itemsSR[i]: i for i in range(len(itemsSR))}
    return itemIdToIndex

#Fetches from the matches_.json files
def getMatchJson():
    matches = []
    for i in range(1, 11):
        jMatchStng = codecs.open('seed-files/matches' + str(i) + '.json', 'r', encoding='latin-1').read()
        #print(jMatchStng)
        jMatch = json.loads(jMatchStng)
        matches += jMatch['matches']
    return matches

def getRoleDictionary():
    return {("TOP", "SOLO"): 0,
            ("MID", "SOLO"): 1,
            ("BOTTOM", "DUO_CARRY"): 2,
            ("BOTTOM", "DUO_SUPPORT"): 3,
            ("JUNGLE", "NONE"): 4
            }

def getRoleVectorForIndex(i):
    v = [0]*5
    v[i] = 1
    return v

def getRoleData(): 
    l = []
    itemDict = getItemDictionary()
    roleDict = getRoleDictionary()
    for m in getMatchJson():
        for p in m['participants']:
            lane = p['timeline']['lane']
            role = p['timeline']['role']
            items = [ p['stats']['item'+str(i)] for i in range(1, 7) ]
            t = (lane, role)
            if t in roleDict: #Discards nonstandard roles
                l += (getRoleVectorForIndex(roleDict[t]), itemListToVector(items, itemDict))

def main():
    getRoleData()
    '''
    itemDict = getItemDictionary()
    for m in getMatchJson()[:10]:
        for p in m['participants']:
            lane = p['timeline']['lane']
            role = p['timeline']['role']
            items = [ p['stats']['item'+str(i)] for i in range(1, 7) ]
            print(lane, role, itemListToVector(items, itemDict))
    '''
if __name__ == '__main__':
    main()
