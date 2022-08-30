import requests
import json
import jsons
import base64
import nbt
from nbt.nbt import TAG_List, TAG_Compound, NBTFile

import io
import dill
import os
from concurrent.futures import ThreadPoolExecutor


API_KEY = 'a866a415-43d6-4de5-b326-5e8528cb1fd2'
OUTPUT_FILE_NAME = 'api_output.txt'
craftable_item_blacklist = ['HEAT_CORE','TENTACLE_MEAT', 'MAGMA_CHUNK', 'GAZING_PEARL', 'COLOSSAL_EXP_BOTTLE_UPGRADE', 'BEZOS', 'SULPHURIC_COAL', 'HORN_OF_TAURUS']

ignoredSortedItems = ['STICK']

reforges = {
    'dirty': 'DIRT_BOTTLE', 
    'fabled': 'DRAGON_CLAW',
    'gilded': 'MIDAS_JEWEL',
    'suspicious': 'SUSPICIOUS_VIAL',
    'warped': 'AOTE_STONE',
    'withered': 'WITHER_BLOOD',
    'bulky': 'BULKY_STONE',
    "jerry's": 'JERRY_STONE',
    'precise': 'OPTICAL_LENS',
    'spiritual': 'SPIRIT_DECOY',
    'headstrong': 'SALMON_OPAL',
    'candied': 'CANDY_CORN',
    'submerged': 'DEEP_SEA_ORB',
    'perfect': 'DIAMOND_ATOM',
    'reinforced': 'RARE_DIAMOND',
    'renowned': 'DRAGON_HORN',
    'spiked': 'DRAGON_SCALE',
    'hyper': 'ENDSTONE_GEODE',
    'giant': 'GIANT_TOOTH',
    'jaded': 'JADERALD',
    'cubic': 'MOLTEN_CUBE',
    'necrotic': 'NECROMANCER_BROOCH',
    'empowered': 'SADAN_BROOCH',
    'ancient': 'PRECURSOR_GEAR',
    'undead': 'PREMIUM_FLESH',
    'loving': 'RED_SCARF',
    'ridiculous': 'RED_NOSE',
    'glistening': 'SHINY_PRISM',
    'strengthened': 'SEARING_STONE',
    'waxed': 'BLAZE_WAX',
    'fortified': 'METEOR_SHARD',
    'lucky': 'LUCKY_DICE',
    'stiff': 'HARDENED_WOOD',
    'chomp': 'KUUDRA_MANDIBLE',
    'ambered': 'AMBER_MATERIAL',
    'auspicious': 'ROCK_GEMSTONE',
    'fleet': 'DIAMONITE',
    'heated': 'HOT_STUFF',
    'magnetic': 'LAPIS_CRYSTAL',
    'mithraic': 'PURE_MITHRIL',
    'refined': 'REFINED_AMBER',
    'mining reforge': 'PETRIFIED_STARFALL',
    'fruitful': 'ONYX',
    'moil': 'MOIL_LOG',
    'toil': 'TOIL_LOG',
    'blessed': 'BLESSED_FRUIT',
    'bountiful': 'GOLDEN_BALL',
} 
enchantmentTableEnchants = ['bane_of_arthropods',
                            'efficiency', 
                            'cleave',
                            'critical', 
                            'cubism', 
                            'ender_slayer',
                            'execute',
                            'experience', 
                            'fire_aspect', 
                            'first_strike', 
                            'first_strike',
                            'giant_killer', 
                            'impaling',
                            'knockback',
                            'lethality',
                            'life_steal',
                            'looting', 
                            'luck', 
                            'mana_steal', 
                            'life_steal', 
                            'prosecute',
                            'scavenger', 
                            'sharpness', 
                            'smite', 
                            'syphon',
                            'thunderbolt',
                            'thunderlord', 
                            'titan_killer',
                            'triple-strike',
                            'vampirism', 
                            'venomous', 
                            'vicious', 
                            'chance', 
                            'dragon_tracer', 
                            'flame', 
                            'infinite_quiver',
                            'piercing', 
                            'power', 
                            'punch', 
                            'snipe', 
                            'aqua_affinity', 
                            'blast_protection', 
                            'depth_strider', 
                            'feather_falling', 
                            'fire_protection', 
                            'frost_walker', 
                            'growth', 
                            'projectile_protection', 
                            'protection',
                            'thorns',
                            'experience', 
                            'fortune',
                            'harvesting',
                            'rainbow', 
                            'silk_touch',
                            'smeling_touch',
                            'angler', 
                            'blessing',
                            'caster', 
                            'frail', 
                            'looting',
                            'luck_of_the_sea',
                            'lure', 
                            'magnet',
                            'spiked_hook']
555555
essencePrice = {
    'UNDEAD': 670,
    'GOLD': 144,
    'DIAMOND': 84,
    'DRAGON': 101,
    'ICE': 100,
    'WITHER': 1300,
    'SPIDER': 230,
}

empty_auction = {'uuid': '', 
                 'auctioneer': '', 
                 'profile_id': '',
                 'coop': [''], 
                 'start': 0, 'end': 0, 
                 'item_name': '', 
                 'item_lore': '', 
                 'extra': '', 
                 'category': 'misc', 
                 'tier': 'COMMON', 
                 'starting_bid': 0, 
                 'item_bytes': 'H4sIAAAAAAAAAE2QwUrDQBCGJ22tSS5F0KOwitdYmxRtvAVTtWBrab3LJDtNFzabkt2gfaK+Rx9M3IAH5zbf/zEMvw/ggSN8AHA60BHccR04eaoaZRwfugYLD3qk8i200wXvVXB6llhou/74cMqF3kncW+utqsm1tA+Xx8PDx1ZoJgyVLEfFMmKNJs5QM4RrG5dCiUqxZlfUyOmWLSXmZH0mFEO1/++g4m3wJaRkVZ6jthCl3MOFdQpSVKMhlgosK8X1lf3APx7i40GuktXUhd4CS4Jzi/4Utt7VhFyoAnwYTL9NjYkxtcgaQ9ptO4CzdJbM3xfp53q5mibpbPFi7zSNTW42FBGnMAvGYRQH49EmD7JRSAG/izZ8kt3HWZS54BlRkjZY7mAwGYbxMAxZ9Dgas+UcoAP9FEssqK30Fz8cjd6BAQAA', 
                 'claimed': False, 
                 'claimed_bidders': [], 
                 'highest_bid_amount': 0, 
                 'last_updated': 1661800568168, 
                 'bin': True, 
                 'bids': [], 
                 'item_uuid': ''}

class sbItem():
    def __init__(self, data, auctionHouseData_data=None) -> None:
        global recipeList
        #name
        self.id = data['tag']['ExtraAttributes']['id']
        self.name = data['tag']['display']['Name']
        
        self.count = data['Count']
        try:
            self.rarityUpgrades = data['tag']['ExtraAttributes']['rarity_upgrades']
        except:
            self.rarityUpgrades = None   
        try:
            self.hotPotatoCount = data['tag']['ExtraAttributes']['hot_potato_count']
        except:
            pass
        try:
            self.reforge = data['tag']['ExtraAttributes']['modifier']
        except:
            self.reforge = None

        try:
            self.dungeonStars = data['tag']['ExtraAttributes']['dungeon_item_level']

        except:
            self.dungeonStars = 0  
        try:
            self.uuid = data['tag']['ExtraAttributes']['uuid']
        except:
            self.uuid = '000000000000000000000000000000'  
        try:
            self.enchantments = data['tag']['ExtraAttributes']['enchantments']
            # for i in list(data['tag']['ExtraAttributes']['enchantments']):
            #     self.enchantments[i] = data['tag']['ExtraAttributes']['enchantments'][i]
        except:
            self.enchantments = {}  
            
        self.value = 0
        self.itemValue = 0
        self.reforgeValue = 0
        self.enchantmentValue = 0
        self.starValue = 0
        self.hotPotatoBookValue = 0
        self.fumingPotatoBookValue = 0
        self.recombValue = 0
        
        try:
            self.recipe = recipeList[self.id]
        except:
            self.recipe = {}
        self.raw_craft_cost = 0
        self.craft_cost = 0
        self.craft_cost_diff = 0
        
        if (auctionHouseData_data != None):
            self.hasAuctionData = True
            self.auction_uuid = auctionHouseData_data['uuid']
            self.auctioneer_uuid = auctionHouseData_data['auctioneer']
            # self.auctioneer = get_player_by_uuid(auctionHouseData_data['auctioneer'])
            self.starting_bid = auctionHouseData_data['starting_bid']
        else:
            self.hasAuctionData = False
        

        

    def calc_value(self):
        global auctionHouseData
        global itemData
        global bazaarData
        global reforges
        global enchantmentTableEnchants
        bazaarItems = list(bazaarData.keys()) + ignoredSortedItems

        # try:
        if self.id in list(bazaarData):
            itemValue = bazaarData[self.id]['buyPrice']
        elif self.id in auctionHouseData.items:
            itemValue = float(auctionHouseData.items[str(self.id)][0].starting_bid) / auctionHouseData.items[str(self.id)][0].count
        else:
            itemValue = 0

        # except:
        #     itemValue=0
        
        value = itemValue

        reforgeValue = 0
        enchantmentValue = 0
        starValue = 0
        hotPotatoBookValue = 0
        fumingPotatoBookValue = 0
        recombValue = 0
        
        if self.reforge != None:
            if self.reforge in list(reforges):
                if reforges[self.reforge] in auctionHouseData.items:
                    print('reforge available')

                    reforgeValue = auctionHouseData.items[reforges[self.reforge]][0].starting_bid
                if reforges[self.reforge] in list(bazaarData):
                    reforgeValue += bazaarData[reforges[self.reforge]]['buyPrice']


        value = value + reforgeValue

        for enchantment in list(self.enchantments):
            if not enchantment in enchantmentTableEnchants:
                if 'ENCHANTMENT_'+ enchantment.upper() + '_' + str(self.enchantments[enchantment]) in bazaarItems:
                    enchantmentValue = enchantmentValue + bazaarData['ENCHANTMENT_'+ enchantment.upper() + '_' + str(self.enchantments[enchantment])]['buyPrice']

        value = value + enchantmentValue

        try:
            upgradeCount = self.dungeonStars - 1
            while upgradeCount > 0:
                upgradeCount = min(upgradeCount, 5)
                currentEssenceTier = itemData[str(self.id)]['upgrade_costs'][upgradeCount][0]
                starValue = starValue + essencePrice[currentEssenceTier['essence_type']] * currentEssenceTier['amount']
                upgradeCount = upgradeCount - 1
        except:
            pass
                
        value = value + starValue

        
        try:
            hotPotatoBookValue = bazaarData['HOT_POTATO_BOOK']['buyPrice'] * max(min(self.hotPotatoCount, 10), 0)
            fumingPotatoBookValue = bazaarData['FUMING_POTATO_BOOK']['buyPrice'] * max(min(self.hotPotatoCount - 10, 5), 0)
            value = value + hotPotatoBookValue + fumingPotatoBookValue
        except:
            pass  
        try:
            recombValue = bazaarData['RECOMBOBULATOR_3000']['buyPrice'] * self.rarityUpgrades
            value = value + recombValue
        except:
            pass
        
        try:
            value = value + self.ExtraAttributes['winning_bid'].value
        except:
            pass
        
        value = value * self.count

        value = value
        self.value = value
        self.itemValue = itemValue
        self.reforgeValue = reforgeValue
        self.enchantmentValue = enchantmentValue
        self.starValue = starValue
        self.hotPotatoBookValue = hotPotatoBookValue
        self.fumingPotatoBookValue = fumingPotatoBookValue
        self.recombValue = recombValue
    
        return self
    
    def print_value(self, in_console=True, file_name=None):
        if (file_name != None):                
            with open(file_name, 'a', encoding='utf-8') as f:
                f.write('name                 : ' + str(self.count) + 'x ' + self.name + '\n')
                f.write('item value           : ' + str(format_number(self.itemValue)) + '\n')
                f.write('reforgeValue         : ' + str(format_number(self.reforgeValue)) + '\n')
                f.write('enchantmentValue     : ' + str(format_number(self.enchantmentValue)) + '\n')
                f.write('starValue            : ' + str(format_number(self.starValue)) + '\n')
                f.write('hotPotatoBookValue   : ' + str(format_number(self.hotPotatoBookValue)) + '\n')
                f.write('fumingPotatoBookValue: ' + str(format_number(self.fumingPotatoBookValue)) + '\n')
                f.write('recombValue          : ' + str(format_number(self.recombValue)) + '\n')
                f.write('craft cost           : ' + str(format_number(self.craft_cost)) + '\n')
                f.write('craft cost diff      : ' + str(format_number(self.craft_cost_diff)) + '\n')
                f.write('value                : ' +  str(self.value) + '\n\n')
                if self.hasAuctionData:
                    f.write('Auctioneer           : ' + self.auctioneer_uuid + '\n\n')

        if in_console:
            print('name: ' + str(self.count) + 'x ' + str(self.name))
            print('item value: ' + str(self.itemValue))
            print('reforgeValue: ' + str(self.reforgeValue))
            print('enchantmentValue: ' + str(self.enchantmentValue))
            print('starValue: ' + str(self.starValue))
            print('hotPotatoBookValue: ' + str(self.hotPotatoBookValue))
            print('fumingPotatoBookValue: ' + str(self.fumingPotatoBookValue))
            print('recombValue: ' + str(self.recombValue))
            print('value: ' +  str(self.value))
            print()

    def calc_craft_cost(self):
        craftCost = 0
        
        for recipeItem in list(self.recipe):
            craftCost += calc_raw_value(recipeItem) * self.recipe[recipeItem]  
        self.raw_craft_cost = craftCost
        
        self.calc_value()
        self.craft_cost = self.value - self.itemValue + self.raw_craft_cost
        
        self.craft_cost_diff = self.value - self.craft_cost
        
        return self


class auctionHouse():
    def __init__(self):
        pages = get_auctions()['totalPages']
        self.items = {}
        self.itemList = []
        listOfPageNums = []
        
        # for i in range(0, pages - 1):
        #     listOfPageNums.append(i)
            
        # with ThreadPoolExecutor(max_workers=10) as pool:
        #     response_list = list(pool.map(get_auctions,listOfPageNums))
            
        response_list = [get_auctions(0)]
        
        for pageIndex in range(0, len(response_list)):
            page = response_list[pageIndex]['auctions']
            for currentauction in page:
                if currentauction['bin'] == True:

                # true_item_data = get_auction_item_data(currentauction['uuid'])
                    itemId = str(decode_inventory_data(currentauction['item_bytes'])[0]['tag']['ExtraAttributes']['id'])
                    
                    try:
                        if itemId == "ENCHANTED_BOOK":
                            if not len(decode_inventory_data(currentauction['item_bytes'])[0]['tag']['ExtraAttributes']['enchantments']) >= 2:
                                itemId = str(list(decode_inventory_data(currentauction['item_bytes'])[0]['tag']['ExtraAttributes']['enchantments'])[0].upper())
                            else:
                                pass
                    except:
                        pass
                    
                    currentauction_sbitem = sbItem(decode_inventory_data(currentauction['item_bytes'])[0], currentauction)

                    self.itemList.append(currentauction_sbitem)

                    if itemId in list(self.items):
                        addedAuction = False
                        j = 0
                        while addedAuction == False:
                            if self.items[itemId][j].starting_bid >= currentauction_sbitem.starting_bid:
                                self.items[itemId].insert(j, currentauction_sbitem)
                            j = j + 1
                            addedAuction = True
                    else:
                        self.items[itemId] = [self.itemList[-1]]

            print("Indexing Auction House: " + str(pageIndex) + '/' + str(pages), end='\r')


            
#nbt modifiers
def decode_inventory_data(raw):
   data = nbt.nbt.NBTFile(fileobj = io.BytesIO(base64.b64decode(raw)))
   return unpack_nbt(data[0])

def unpack_nbt(tag):
    if isinstance(tag, TAG_List):
        return [unpack_nbt(i) for i in tag.tags]
    elif isinstance(tag, TAG_Compound):
        return dict((i.name, unpack_nbt(i)) for i in tag.tags)
    else:
        return tag.value

#requests
def get_auctions(page=0):
    data = requests.get(url='http://api.hypixel.net/skyblock/auctions', params={
        'key': API_KEY,
        'page': page
    }).text
    data = json.loads(data)
    print('recieved: ' +  str(page))
    return data

def get_bazaar():
    rawdata = requests.get(url='https://api.hypixel.net/skyblock/bazaar', params={
        'key': API_KEY,
    }).text
    rawdata = json.loads(rawdata)['products']
    data = {}
    for product in list(rawdata):
        data[product] = rawdata[product]['quick_status']
    return data

def get_items_data():
    rawdata = requests.get(url='https://api.hypixel.net/resources/skyblock/items', params={
        'key': API_KEY,
    }).text
    rawdata = json.loads(rawdata)['items']
    data = {}
    for item in rawdata:
        data[item['id']] = item
        data[item['id']].pop('id')

    return data

def get_player_data(playerName, profile_name):
    uuid = json.loads(requests.get(url='https://api.mojang.com/users/profiles/minecraft/' + playerName).text)["id"]
    # data = requests.get(url='https://sky.shiiyu.moe/api/v2/profile/' + playerName).text
    data = requests.get(url='https://api.hypixel.net/skyblock/profiles', 
        params={
        'key': API_KEY,
        'uuid': uuid,
    }
    ).text
    data = json.loads(data)

    for profile in data['profiles']:
        if profile['cute_name'].lower() == profile_name.lower():

            return profile['members'][uuid]
    return 

def get_auction_item_data(uuid):
    rawdata = requests.get(url='https://api.hypixel.net/skyblock/auction', params={'key': API_KEY, 'uuid': uuid}).text
    data = json.loads(rawdata)
    try:
        return data['auctions'][0]
    except: 
        return empty_auction

def get_player_by_uuid(uuid):
    # request = requests.get("https://api.mojang.com/user/profiles/" + uuid + "/names")
    # # print()
    # # currentUsername = request.json()[-1]['name']
    # return request.json()[-1]['name']

    raw_data = requests.get("https://playerdb.co/api/player/minecraft/" + uuid).text
    data = json.loads(raw_data)['data']['player']['username']
    
    return data







#item data
def load_item_neu_data_to_file():
    itemNeuData = {}
    files = len(os.listdir('items'))
    fileNumber = 1

    for filename in os.listdir('items'):
        with open('items/' + filename, 'r', encoding="utf8") as f:
            fileContent = f.read()
            fileContent = json.loads(fileContent)
            itemNeuData[filename[: len(filename) - 5]] = fileContent
            print('Item ' + str(fileNumber) + '/' + str(files) + ' Filename: ' + str(filename))
            fileNumber = fileNumber + 1

    json.dump(itemNeuData, open('itemData.txt', 'w'))

def neuData_to_recipe_list(neuData):
    global craftable_item_blacklist
    recipeList = {}

    for item in list(neuData):
        if 'recipe' in list(neuData[item]):
            checkBlacklisted = ['']
            for i in neuData[item]['recipe'].values():
                try:
                    checkBlacklisted.append(i.split(':')[0])
                except:
                    pass

            if not any(x in checkBlacklisted for x in craftable_item_blacklist):
                recipeList[item] = {}
                for craftSpot in list(neuData[item]['recipe']):
                    if neuData[item]['recipe'][craftSpot] != "":
                        craftSpotItem = neuData[item]['recipe'][craftSpot].split(':')[0]
                        craftSpotItem = craftSpotItem.split(';')[0]
                        craftSpotNumber = int(neuData[item]['recipe'][craftSpot].split(':')[1])
                        if craftSpotItem in list(recipeList[item]):
                            recipeList[item][craftSpotItem] = recipeList[item][craftSpotItem] + craftSpotNumber
                        else:
                            recipeList[item][craftSpotItem] = craftSpotNumber
    return recipeList

def calc_raw_value(id):
    global bazaarData
    global auctionHouseData
    if id == 'NECRON_BLADE':
        id = 'NECRON_HANDLE'
    # try:
    if id in list(bazaarData):
        itemValue = bazaarData[id]['buyPrice']
    elif id in list(auctionHouseData.items):
        itemValue = auctionHouseData.items[str(id)][0].starting_bid
    else:
        itemValue = 0
    # except:
    #     itemValue = 0
    itemValue = round(itemValue, 1)
    return itemValue

def calc_item_craft_profit(recipeList):
    craftCost = {}
    
    for item in list(recipeList):
        craftCost[item] = {}
        craftCost[item]['original'] = calc_raw_value(item)
        craftCost[item]['craft'] = 0

        for recipeItem in list(recipeList[item]):
            craftCost[item]['craft'] = craftCost[item]['craft'] + (calc_raw_value(recipeItem) * recipeList[item][recipeItem])

        craftCost[item]['difference'] =  craftCost[item]['original'] - craftCost[item]['craft']

        if craftCost[item]['craft'] != 0:
            craftCost[item]['diffProc'] =  craftCost[item]['original'] / craftCost[item]['craft'] * 100 - 100
        else:
            craftCost[item]['diffProc'] = 0
        
        
    return craftCost

def raw_item_value(id):
    global bazaarData
    global auction
    if id == 'NECRON_BLADE':
        id = 'NECRON_HANDLE'
    # try:
    if id in list(bazaarData):
        itemValue = bazaarData[id]['buyPrice']
    elif id in list(auction.items):
        itemValue = auction.items[str(id)][0]['starting_bid']
    else:
        itemValue = 0
    # except:
    #     itemValue = 0
    itemValue = round(itemValue, 1)
    return itemValue

def neuData_to_recipe_list(neuData):
    global craftable_item_blacklist
    recipeList = {}

    for item in list(neuData):
        if 'recipe' in list(neuData[item]):
            checkBlacklisted = ['']
            for i in neuData[item]['recipe'].values():
                try:
                    checkBlacklisted.append(i.split(':')[0])
                except:
                    pass

            if not any(x in checkBlacklisted for x in craftable_item_blacklist):
                recipeList[item] = {}
                for craftSpot in list(neuData[item]['recipe']):
                    if neuData[item]['recipe'][craftSpot] != "":
                        craftSpotItem = neuData[item]['recipe'][craftSpot].split(':')[0]
                        craftSpotItem = craftSpotItem.split(';')[0]
                        craftSpotNumber = int(neuData[item]['recipe'][craftSpot].split(':')[1])
                        if craftSpotItem in list(recipeList[item]):
                            recipeList[item][craftSpotItem] = recipeList[item][craftSpotItem] + craftSpotNumber
                        else:
                            recipeList[item][craftSpotItem] = craftSpotNumber
    return recipeList


#prints
def print_done():
    print('\033[92m' + 'done' + '\033[0m')
        
def reprint_input_output(input_question, returned_value):
    print('\033[F\033[K'  + input_question + '\033[96m' + str(returned_value) + '\033[0m')
    
def format_number(number):
    return '{:>30}'.format('{:,}'.format(round(number)).replace(',', ' '))







print('get item data...', end="")
itemData = get_items_data()
print_done()

print('getting bazaar Data...', end='')
bazaarData = get_bazaar()
neuData = json.load(open('itemData.txt', 'r'))
print_done()

print('creating recipe list...', end='')
recipeList = neuData_to_recipe_list(neuData)
print_done()

if (input('Request Auction (Y)es or (N)o: ').lower() == "y"):
    auctionHouseData = auctionHouse()
    dill.dump(auctionHouseData, file=open('auctions.txt', 'wb'))
print('getting auction Data...', end='')
auctionHouseData = dill.load(open('auctions.txt', 'rb'))
print_done()

print('creating recipe list...', end='')
recipeList = neuData_to_recipe_list(neuData)
print_done()

print('calculate crafcost for all items...', end='')
craftCost = calc_item_craft_profit(recipeList)
print_done()


print('Recalculating value of ah items...', end='')
for item in auctionHouseData.itemList:
    item.calc_value()
print_done()

get_player_by_uuid('9412256a372f4cf8ac2a495c981f1c67')

with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as f:
    f.write('')

for itemIndex in range(0, len(auctionHouseData.itemList) - 1):
    auctionHouseData.itemList[itemIndex].calc_value().calc_craft_cost()

auctionHouseData.itemList.sort(key=lambda x: x.craft_cost_diff, reverse=True)

for itemIndex in range(0, len(auctionHouseData.itemList) - 1):
    auctionHouseData.itemList[itemIndex].print_value(in_console=False, file_name=OUTPUT_FILE_NAME)
    print('item: ' + str(itemIndex) + '/' + str(len(auctionHouseData.itemList)), end='\r')