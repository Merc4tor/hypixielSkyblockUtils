from copy import deepcopy
import requests
import json
import base64
import nbt
from nbt.nbt import TAG_List, TAG_Compound, NBTFile
import io
import dill
import os
from concurrent.futures import ThreadPoolExecutor

API_KEY = 'PLEASE ENTER API KEY HERE: do "/api new" in hypixel to get one'
OUTPUT_FILE_NAME = 'output.txt'
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
    def __init__(self, data=None, auctionHouseData_data=None, id=None) -> None:
        global recipeList
        #name
        if id != None:
            self.id = id
        else:
            self.id = data['tag']['ExtraAttributes']['id']

        try:
            self.name = data['tag']['display']['Name']
        except:
            self.name = id_to_name(self.id)
        try:
            self.count = data['Count']
        except:
            self.count = 1

        try:
            self.rarityUpgrades = data['tag']['ExtraAttributes']['rarity_upgrades']
        except:
            self.rarityUpgrades = 0   

        self.hotPotatoCount = 0

        try:
            self.hotPotatoCount = max(min(data['tag']['ExtraAttributes']['hot_potato_count'], 10), 0)
        except:
            self.hotPotatoCount = 0

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
        self.bid_diff = 0
        self.bid_diff_proc = 0
        
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
                    reforgeValue = auctionHouseData.items[reforges[self.reforge]][0].starting_bid
                if reforges[self.reforge] in list(bazaarData):
                    reforgeValue += bazaarData[reforges[self.reforge]]['buyPrice']


        value = value + reforgeValue

        for enchantment in list(self.enchantments):
            if not enchantment in enchantmentTableEnchants:
                if 'ENCHANTMENT_'+ enchantment.upper() + '_' + str(self.enchantments[enchantment]) in bazaarItems:
                    enchantmentValue = enchantmentValue + bazaarData['ENCHANTMENT_'+ enchantment.upper() + '_' + str(self.enchantments[enchantment])]['buyPrice']

        value = value + enchantmentValue

        self.total_essence = 0
        try:
            upgradeCount = self.dungeonStars - 1
            self.total_essence = 0
            while upgradeCount > 0:
                upgradeCount = min(upgradeCount, 5)
                currentEssenceTier = itemData[str(self.id)]['upgrade_costs'][upgradeCount][0]
                self.total_essence += currentEssenceTier['amount']
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
        
        try:
            value = value * self.count
        except:
            pass

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
    
    def print_value(self,file_name=None, console=False, given_file=None ):
        if given_file != None:
            given_file.write('name                 : ' + str(self.count) + 'x ' + self.name + '\n')
            given_file.write('item value           : ' + str(format_number(self.itemValue)) + '\n')
            given_file.write('reforgeValue         : ' + str(format_number(self.reforgeValue)) + '\n')
            given_file.write('enchantmentValue     : ' + str(format_number(self.enchantmentValue)) + '\n')
            given_file.write('starValue            : ' + str(format_number(self.starValue)) + '\n')
            given_file.write('hotPotatoBookValue   : ' + str(format_number(self.hotPotatoBookValue)) + '\n')
            given_file.write('fumingPotatoBookValue: ' + str(format_number(self.fumingPotatoBookValue)) + '\n')
            given_file.write('recombValue          : ' + str(format_number(self.recombValue)) + '\n')
            given_file.write('craft cost           : ' + str(format_number(self.craft_cost)) + '\n')
            given_file.write('craft cost diff      : ' + str(format_number(self.craft_cost_diff)) + '\n')
            given_file.write('value                : ' +  str(format_number(self.value)) + '\n\n')
            if self.hasAuctionData:
                f.write('Auctioneer           : ' + self.auctioneer_uuid + '\n\n')

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
                f.write('value                : ' +  str(format_number(self.value)) + '\n\n')
                if self.hasAuctionData:
                    f.write('Auctioneer           : ' + self.auctioneer_uuid + '\n\n')

        if console:
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
        self.calc_value()
        
        self.raw_craft_cost = craftCost
        self.craft_cost_diff = self.itemValue - self.craft_cost
        
        try:
            self.craft_cost_diff_proc = self.itemValue / craftCost * 100 - 100
        except:
            self.craft_cost_diff_proc = -100
        self.craft_cost = self.value - self.itemValue + self.raw_craft_cost
        
        
        return self
    
    def print_craft_cost_to_file(self, file):
        global itemData
        file.write('id                 : ' +  self.id + '\n')
        file.write('name                 : ' + str(self.count) + 'x ' + self.name + '\n')
        file.write('item value           : ' + str(format_number(self.itemValue)) + '\n')
        file.write('raw craft cost       : ' + str(format_number(self.raw_craft_cost)) + '\n')
        file.write('craft cost diff      : ' + str(format_number(self.craft_cost_diff)) + '\n')
        file.write('craft cost diff proc : ' + str(format_number(self.craft_cost_diff_proc)) + '\n')
        for i in self.recipe:
            try:
                f.write(f"{str(itemData[i]['name']):<25} {': '} {str(calc_raw_value(i)):<10}{' x ':>0} {str(self.recipe[i])} {'= ':>3} {calc_raw_value(i) * self.recipe[i]}" + '\n')
            except:
                f.write(f"{str(i):<25} {': '} {str(calc_raw_value(i)):<10}{' x ':>0} {str(self.recipe[i])} {'= ':>3} {calc_raw_value(i) * self.recipe[i]}" + '\n')
        f.write('\n')
    
    def calc_auction_data(self):
        self.calc_craft_cost()
        
        self.bid_diff = self.starting_bid - self.craft_cost
        try:
            self.bid_diff_proc = self.starting_bid / self.craft_cost * 100 - 100
        except:
            self.bid_diff_proc = -100        
        
        return self
    
    def print_auction_profit_to_file(self, file):
        global itemData
        global bazaarData
        file.write('id                 : ' +  self.id + '\n')
        file.write('name                 : ' + str(self.count) + 'x ' + self.name + '\n')
        file.write('item value           : ' + str(format_number(self.itemValue)) + '\n')
        file.write('craft cost       : ' + str(format_number(self.craft_cost)) + '\n')
        file.write('craft cost diff      : ' + str(format_number(self.bid_diff)) + '\n')
        file.write('craft cost diff proc : ' + str(format_number(self.bid_diff_proc)) + '\n')
        file.write('recipe: ' + '\n')
        for i in self.recipe:
            try:
                f.write(f"{'':<8}{str(itemData[i]['name']):>25} {': ':<10} {format_number(calc_raw_value(i))}{' x ':>0} {str(self.recipe[i])} {'= ':>3} {calc_raw_value(i) * self.recipe[i]}" + '\n')
            except:
                f.write(f"{'':<8}{str(i):>25}                   {': ':<10} {format_number(calc_raw_value(i))}{' x ':>0} {str(self.recipe[i])} {'= ':>3} {calc_raw_value(i) * self.recipe[i]}" + '\n')
        file.write('other: ' + '\n')
        
        if self.rarityUpgrades != 0:
            file.write(f"{'':<8}{'recombobulators':>25}         {': '} {str(self.rarityUpgrades)}{' x ':>0} {format_number(bazaarData['RECOMBOBULATOR_3000']['buyPrice'])}  {'= ':>3} {format_number(self.rarityUpgrades * bazaarData['RECOMBOBULATOR_3000']['buyPrice'])}" + '\n')
    
        if self.hotPotatoCount != 0:
            file.write(f"{'':<8}{'Hot Potato Books':>25}        {': '} {str(max(min(self.hotPotatoCount, 5), 0))}         {' x ':>0} {format_number(bazaarData['HOT_POTATO_BOOK']['buyPrice'])}      {'= ':<3} {format_number((self.hotPotatoCount * bazaarData['HOT_POTATO_BOOK']['buyPrice']))}" + '\n')
            if self.hotPotatoCount >= 5:
                file.write(f"{'':<8}{'Fuming Hot Potato Books':>25} {': '} {str(max(min(self.hotPotatoCount - 10, 5), 0))}    {' x ':>0} {format_number(bazaarData['FUMING_POTATO_BOOK']['buyPrice'])}   {'= ':<3} {format_number(max(min(self.hotPotatoCount - 10, 5), 0) * bazaarData['FUMING_POTATO_BOOK']['buyPrice'])}" + '\n')

        try:
            file.write(f"{'':<8}{'Reforge':>25}                 {': '} {reforges[self.reforge]}         {' x ':>0} {format_number(bazaarData[reforges[self.reforge]]['buyPrice'])} {'= ':>3} {format_number(bazaarData[reforges[self.reforge]]['buyPrice'])}" + '\n')
        except:
            pass
        
        try:
            currentEssenceTier = itemData[str(self.id)]['upgrade_costs'][self.dungeonStars - 1][0]
            file.write(f"{'':<8}{'Essence ':>25}{': ':<10} {currentEssenceTier['essence_type']}  {str(self.total_essence):<10}{' x ':>0} {str(essencePrice[currentEssenceTier['essence_type']])} {'= ':>3} {essencePrice[currentEssenceTier['essence_type']] * self.total_essence:>13}" + '\n')
        except:
            pass
        
        file.write('Enchants: ' + '\n')


        zerovalue_enchants = []
        for enchantment in list(self.enchantments):
            if calc_raw_value('ENCHANTMENT_'+ enchantment.upper() + '_' + str(self.enchantments[enchantment])) != 0:
                file.write(f"{'':<8}{enchantment:>25} {': ':<10} {str(calc_raw_value('ENCHANTMENT_'+ enchantment.upper() + '_' + str(self.enchantments[enchantment])))}{' x ':>0} {str(1)} {'= ':>3} {calc_raw_value('ENCHANTMENT_'+ enchantment.upper() + '_' + str(self.enchantments[enchantment]))}" + '\n')
                zerovalue_enchants.append(enchantment)

        file.write('Other Enchants: ' + '\n')
        file.write(f"{'':<8} {', '.join(zerovalue_enchants)}" + '\n')


        f.write('\n')
        
        


class auctionHouse():
    def __init__(self):
        pages = get_auctions()['totalPages']
        self.items = {}
        self.itemList = []
        listOfPageNums = []
        
        for i in range(0, pages - 1):
            listOfPageNums.append(i)
            
        with ThreadPoolExecutor(max_workers=10) as pool:
            response_list = list(pool.map(get_auctions,listOfPageNums))
            
        # response_list = [get_auctions(0)]
        
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
                    
                    item_data = decode_inventory_data(currentauction['item_bytes'])[0]
                    if item_data != {}:
                    
                        currentauction_sbitem = sbItem(item_data, currentauction)

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
    
    def recalculate_items(self):   
        print('Recalculating value of ah items...', end='\n')

        for item_index in range(0, len(self.itemList) - 1):
            self.itemList[item_index].calc_auction_data()
            # print("Recalculating Item Value: " + '{:>30}'.format(str(item_index + 1) + '/' + str(len(self.itemList))), end='\r')
        # print('\r\r')
        print_done()
        return self
    
    def sort_item_list(self, item_key, reversed=True):
        self.itemList.sort(key=lambda x: getattr(x, item_key), reverse=reversed)
        return self
    



            
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
    print('\x1b[2K' + 'recieved: ' +  str(page), end='\r')
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

def get_player_data():
    playerName = input('What is your Username?: ')
    uuid = json.loads(requests.get(url='https://api.mojang.com/users/profiles/minecraft/' + playerName).text)["id"]
    # data = requests.get(url='https://sky.shiiyu.moe/api/v2/profile/' + playerName).text
    data = requests.get(url='https://api.hypixel.net/skyblock/profiles', 
        params={
        'key': API_KEY,
        'uuid': uuid,
    }
    ).text
    data = json.loads(data)

    selectOptions = [profile['cute_name'] for profile in data['profiles']]

    hasSelected = False

    while hasSelected == False:

        for index in range(0, len(selectOptions)):
            print('(' + str(index + 1) + ') ' + selectOptions[index])

        profile_index = input('Please Select Profile: ')

        if profile_index.isnumeric():
            if int(profile_index) > 0 and int(profile_index) <= len(selectOptions):
                print(f"You have selected {selectOptions[int(profile_index) - 1]}!")
                profile_name = selectOptions[int(profile_index) - 1]

                hasSelected = True
            else:
                print('Invalid Num')
        else:
            print('Invalid')
            
            
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

def get_collection_data():
    rawdata = requests.get(url='https://api.hypixel.net/resources/skyblock/collections', params={'key':'6acc323c-d322-42c4-bcfb-928cbc1143e7'}).text 
    data = json.loads(rawdata)
    return data['collections']

#collection data
def collectionData_from_data(data):
    collectionData = {}
    unlocked = []
    deleteStrings = ['Enchanted Book (',') Recipe',' Recipe']
    for type in list(data.keys()):
        for collection in data[type]['items']:
            for tier in data[type]['items'][collection]['tiers']:
                for unlockedItem in tier['unlocks']:
                    # if 'Enchanted Book (' in unlockedItem:
                    #     for string in deleteStrings:
                    #         unlockedItem.replace(string, '')
                            
                    #     unlocked.append(name_to_id(unlockedItem))
                    # else:
                    for string in deleteStrings:
                        unlockedItem = unlockedItem.replace(string, '')

                    collectionData[name_to_id(unlockedItem)] = collection + '_' + str(tier['tier'])

    return {'collectionData': collectionData, 'unlocked': unlocked}
      
def check_unlocked_recipe(x):
    global playerData
    global collectionData
    
    if (x.id in collectionData):

        return collectionData[x.id] in playerData['unlocked_coll_tiers']
    else: 
        return False

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

def name_to_id(name):
    global itemData
    for item_key in list(itemData.keys()):
        if itemData[item_key]['name'] == name:
            return item_key
        
    return 'NAME_NOT_FOUND'

def id_to_name(id):
    global itemData
    
    try:
        return itemData[id]['name']
    except:
        return 'NAME_NOT_FOUND'
    
def check_item_requirements(item, minimumValue, maximumValue, onlyBazaar):
    global bazaarData
    if item.raw_craft_cost >= minimumValue:
        if item.raw_craft_cost <= maximumValue:
            if onlyBazaar:
                recipeItemInBazaarList = []
                for recipeItem in list(item.recipe):
                    if recipeItem in bazaarData + ignoredSortedItems:
                        recipeItemInBazaarList.append(True)
                    else:
                        recipeItemInBazaarList.append(False)
                if all(recipeItemInBazaarList):
                    return True
            else:
                return True
        else:
            return False
    else:
        return False
    
#prints
def print_done():
    print('\033[92m' + 'done' + '\033[0m')
        
def reprint_input_output(input_question, returned_value):
    print('\033[F\033[K'  + input_question + '\033[96m' + str(returned_value) + '\033[0m')
    
def format_number(number):
    return '{:>15}'.format('{:,}'.format(round(number)).replace(',', ' '))


#create data
def create_itemData():
    print('get item data...', end="")
    itemData = get_items_data()
    print_done()
    return itemData

def create_neuData():
    print('getting bazaar Data...', end='')
    neuData = json.load(open('itemData.txt', 'r'))
    print_done()
    return neuData

def create_bazaarData():
    print('getting bazaar Data...', end='')
    bazaarData = get_bazaar()
    print_done()
    return bazaarData

def create_recipeList():
    global neuData
    print('creating recipe list...', end='')
    recipeList = neuData_to_recipe_list(neuData)
    print_done()
    return recipeList

def create_auctionHouse():
    if (input('Request Auction (Y)es or (N)o: ').lower() == "y"):
        auctionHouseData = auctionHouse()
        dill.dump(auctionHouseData, file=open('auctions.txt', 'wb'))
    print('getting auction Data...', end='')
    auctionHouseData = dill.load(open('auctions.txt', 'rb'))
    print_done()
    return auctionHouseData

def create_collectionData():
        print('Getting collection data... ', end='')
        collectionData = collectionData_from_data(get_collection_data())

        unlockedCollectionItems = collectionData['unlocked']
        collectionData = collectionData['collectionData']
        print_done()
        return collectionData, unlockedCollectionItems, collectionData
        
    

selectName = 'What do you want to do?'
#, 'Auction Craft Value'
selectOptions = ['Calculate Networth', 'Craft Profit', 'Auction Items Value']

hasSelected = False

while hasSelected == False:

    for index in range(0, len(selectOptions)):
        print('(' + str(index + 1) + ') ' + selectOptions[index])

    selectAns = input('Please Select: ')

    if selectAns.isnumeric():
        if int(selectAns) > 0 and int(selectAns) <= len(selectOptions):
            print(f"You have selected {selectOptions[int(selectAns) - 1]}!")
            hasSelected = True
        else:
            print('Invalid Num')
    else:
        print('Invalid')



match int(selectAns) - 1:
    case 0: #'Calculate Networth'
        playerData = get_player_data()
        itemData = create_itemData()
        bazaarData = create_bazaarData()
        
        auctionHouseData = create_auctionHouse()    
        auctionHouseData.recalculate_items()
        
        playerItems = []
        with open('output.txt', 'w', encoding='utf-8') as f:
            armorValue = 0
            #f.write('Armor: \n')
            for armor in decode_inventory_data(playerData['inv_armor']['data']):
                try:
                    playerItems.append(sbItem(armor).calc_value())
                    armorValue = armorValue + round(playerItems[-1].value)
            #f.write('Total Armor Value: ' + str(armorValue) + '\n')
                except: 
                    pass
            invValue = 0
            #f.write('Inventory: \n')
            for inv_item in decode_inventory_data(playerData['inv_contents']['data']):
                try:
                    playerItems.append(sbItem(inv_item).calc_value())
                    invValue = invValue + round(playerItems[-1].value)
                except: 
                    pass
                #f.write('Total Inventory Value: ' + str(invValue) + '\n')

            echestValue = 0
            #f.write('Ender Chest: \n')
            for item in decode_inventory_data(playerData['ender_chest_contents']['data']):
                try:
                    playerItems.append(sbItem(item).calc_value())
                    echestValue = echestValue + round(playerItems[-1].value)
                except: 
                    pass
            #f.write('Total Ender Chest Value: ' + str(echestValue) + '\n')

            wardrobeValue = 0
            #f.write('Wardrobe: \n')
            for item in decode_inventory_data(playerData['wardrobe_contents']['data']):
                try:
                    playerItems.append(sbItem(item).calc_value())
                    wardrobeValue = wardrobeValue + round(playerItems[-1].value)
            #f.write('Total Wardrobe Value: ' + str(wardrobeValue) + '\n')
                except: 
                    pass
            talismanValue = 0
            #f.write('Talismans: \n')
            for item in decode_inventory_data(playerData['talisman_bag']['data']):
                try:
                    playerItems.append(sbItem(item).calc_value())
                    talismanValue = talismanValue + round(playerItems[-1].value)
            #f.write('Total Talismans Value: ' + str(talismanValue) + '\n')
                except: 
                    pass
            backpackValue = 0
            #f.write('Backpacks: \n')
            for page in playerData['backpack_contents']:
                for item in decode_inventory_data(playerData['backpack_contents'][page]['data']):
                    try:
                        playerItems.append(sbItem(item).calc_value())
                        backpackValue = backpackValue + round(playerItems[-1].value)
            #f.write('Total Backpacks Value: ' + str(backpackValue) + '\n')
                    except: 
                        pass
                
            f.write('Total Armor Value      : ' + format_number(armorValue) + '\n')
            f.write('Total Inventory Value  : ' + format_number(invValue) + '\n')
            f.write('Total Ender Chest Value: ' + format_number(echestValue) + '\n')
            f.write('Total Wardrobe Value   : ' + format_number(wardrobeValue) + '\n')
            f.write('Total Talismans Value  : ' + format_number(talismanValue) + '\n')
            f.write('Total Backpacks Value  : ' + format_number(backpackValue) + '\n')
            f.write('Total Value            : ' + format_number(armorValue + invValue + echestValue + wardrobeValue + talismanValue + backpackValue) + '\n')

            print('Total Armor Value: ' + str(armorValue) + '\n')
            print('Total Inventory Value: ' + str(invValue) + '\n')
            print('Total Ender Chest Value: ' + str(echestValue) + '\n')
            print('Total Wardrobe Value: ' + str(wardrobeValue) + '\n')
            print('Total Talismans Value: ' + str(talismanValue) + '\n')
            print('Total Backpacks Value: ' + str(backpackValue) + '\n')

            playerItems.sort(key=lambda x: x.value, reverse=True)
            
            f.write('\n')
        
            [instance.print_value(given_file=f, console=False) for instance in playerItems]

    case 1: # 'Craft Profit'
        # playerData = get_player_data(input('What is your Username?: '), input('What is your profile Name?: '))
        playerData = get_player_data(USERNAME, PROFILE)

        itemData = create_itemData()

        neuData = create_neuData()
        
        collectionData, unlockedCollectionItems, collectionData = create_collectionData()
        
        bazaarData = create_bazaarData()
        
        auctionHouseData = create_auctionHouse()
        auctionHouseData.recalculate_items()

        recipeList = create_recipeList()
        
        craftCost = {}
        for item_id in list(recipeList):
            craftCost[item_id] = sbItem(id=item_id).calc_craft_cost()
        
        minimumValue = int(input('minimum value (default 50k): ') or 50000)
        reprint_input_output('minimum value (default 50k): ', minimumValue)

        maximumValue = int(input('maximum value (default 50m): ') or 50000000)
        reprint_input_output('maximum value (default 50m): ', maximumValue)

        sortMethod = input('difference, proc diff (default), craft, original: ') or 'proc diff'
        reprint_input_output('difference, diffProc (default), craft, original: ', sortMethod)
        match sortMethod:
            case 'difference':
                sortMethod = 'craft_cost_diff'
            case 'proc diff':
                sortMethod = 'craft_cost_diff_proc'
            case 'craft':
                sortMethod = 'raw_craft_cost'
            case 'original':
                sortMethod = 'itemValue'

        onlyBazaar = bool(input('use bazaar 1 or 0 (default 0): ').lower() in ['true', '1', 't', 'y', 'yes', 'yeah']) or False
        reprint_input_output('use bazaar 1 or 0 (default 0): ', onlyBazaar)

        craftCostInOrderArray = sorted(list(craftCost.values()), key=lambda x: getattr(x, sortMethod), reverse=True)
        
        showCraftables = input('do you want to only show craftable (Y)es: ').lower() == 'y' or False 
        reprint_input_output('do you want to only show craftable (Y)es: ', showCraftables)

        if (showCraftables):
            craftCostInOrderArray = list(filter(check_unlocked_recipe, craftCostInOrderArray))

        craftCostInOrderArray = list(filter(lambda x: check_item_requirements(x, minimumValue, maximumValue, onlyBazaar), craftCostInOrderArray))


        print('Printing output to output_items.txt ...', end='')
        with open('output.txt', 'w', encoding='utf-8') as f:
            [item.print_craft_cost_to_file(f) for item in craftCostInOrderArray]
        print_done()

    case 2: #'Auction Items Value'
        playerData = get_player_data()

        itemData = create_itemData()

        neuData = create_neuData()
        
        collectionData, unlockedCollectionItems, collectionData = create_collectionData()
        
        bazaarData = create_bazaarData()
        
        recipeList = create_recipeList()
        
        auctionHouseData = create_auctionHouse()
        auctionHouseData.recalculate_items()

        
        minimumValue = int(input('minimum value (default 50k): ') or 50000)
        reprint_input_output('minimum value (default 50k): ', minimumValue)

        maximumValue = int(input('maximum value (default 50m): ') or 50000000)
        reprint_input_output('maximum value (default 50m): ', maximumValue)

        sortMethod = input('difference, proc diff (default), craft, bin: ') or 'proc diff'
        reprint_input_output('difference, diffProc (default), craft, bin: ', sortMethod)
        
        auctionItemList = list(deepcopy(auctionHouseData.itemList))
        
        match sortMethod:
            case 'difference':
                sortMethod = 'bid_diff'
            case 'proc diff':
                sortMethod = 'bid_diff_proc'
            case 'craft':
                sortMethod = 'craft_cost'
            case 'bin':
                sortMethod = 'starting_bid'
        

        onlyBazaar = bool(input('use bazaar 1 or 0 (default 0): ').lower() in ['true', '1', 't', 'y', 'yes', 'yeah']) or False
        reprint_input_output('use bazaar 1 or 0 (default 0): ', onlyBazaar)
        
        auctionItemList.sort(key=lambda x: getattr(x, sortMethod), reverse=True)

        showCraftables = input('do you want to only show craftable (Y)es: ').lower() == 'y' or False 
        reprint_input_output('do you want to only show craftable (Y)es: ', showCraftables)

        if (showCraftables):
            auctionItemList = list(filter(check_unlocked_recipe, auctionItemList))
        print('filtering items ...', end='')
        auctionItemList = list(filter(lambda x: check_item_requirements(x, minimumValue, maximumValue, onlyBazaar), auctionItemList))
        print_done()

        print('Printing output to output.txt ...', end='')
        with open('output.txt', 'w', encoding='utf-8') as f:
            [item.print_auction_profit_to_file(f) for item in auctionItemList]
        print_done()
    # case 4: #'Auction Craft Value'
        

input("Press enter to exit ;)")
