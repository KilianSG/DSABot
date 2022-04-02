import random
import json
import discord.ext

from character.characters_do_stuff.talent import get_nickname
from project_buttons.buttons_template import liturgie_template

dict_for_attributes = {'KL': ['Klugheit', 'modKL'],
                       'IN': ['Intuition', 'modIN'],
                       'KO': ['Konstitution', 'modKO'],
                       'GE': ['Gewandtheit', 'modGE'],
                       'FF': ['Fingerfertigkeit', 'modFF'],
                       'MU': ['Mut', 'modMU'],
                       'CH': ['Charisma', 'modCH'],
                       'KK': ['Körperkraft', 'modKK']}


class modification_table:
    kap = 0
    reach = 0
    casttime = 0
    tiers = 0
    tiers_seperated = []

    def __init__(self, liturgy_to_cast):
        not_modifiable = 'nicht modifizierbar'
        if not not_modifiable in liturgy_to_cast['KaP-Kosten']:
            self.kap = 1
        if not not_modifiable in liturgy_to_cast['Reichweite']:
            self.reach = 1
        if not not_modifiable in liturgy_to_cast['Liturgiedauer']:
            self.casttime = 1
        if 'für' in liturgy_to_cast['KaP-Kosten']:
            self.tiers = 1
            self.tiers_seperated = liturgy_to_cast['KaP-Kosten'].split(',')


def prep_liturgy(message, get_nickname, character, zahl=0, target=None):
    liturgy_to_cast = what_liturgy(message, zahl, target)
    max_modificator = int(character['Liturgien'][liturgy_to_cast]['fw'] / 4)  # TODO modifizierung zu 0 oder +1
    table = modification_table(character['Liturgien'][liturgy_to_cast])
    components = liturgie_template(get_nickname, table)
    return_embed = get_basic_liturgy_embed(get_nickname, character, character['Liturgien'][liturgy_to_cast],
                                           [liturgy_to_cast][0])
    return [return_embed[0], components, max_modificator, character['Liturgien'][liturgy_to_cast], liturgy_to_cast,
            return_embed[1]]


def get_basic_liturgy_embed(name_to_find, character, liturgy_to_cast, liturgy_name, list_of_attributes=[0, 0, 0]):
    proben = liturgy_to_cast['Probe']
    proben = proben.split('/')
    proben_reihnform = [proben[0].strip(), proben[1].strip(), proben[2].split()[0]]
    if list_of_attributes == [0, 0, 0]:
        for x in range(3):
            list_of_attributes[x] = character[dict_for_attributes[proben_reihnform[x]][0]] + character[
                dict_for_attributes[proben_reihnform[x]][1]]
    embedVar = discord.Embed(title=name_to_find, description=f"{liturgy_name} ({liturgy_to_cast['fw']})",
                             color=0x3498DB)
    embedVar.set_thumbnail(url=str(character['Picture']))
    if len(liturgy_to_cast['Wirkung']) >= 1024:
        if len(liturgy_to_cast['Wirkung']) >= 2048:
            split_Wirkung = liturgy_to_cast['Wirkung'][0:1023].rfind('.')
            embedVar.add_field(name=f'Wirkung 1/3', value=f"{liturgy_to_cast['Wirkung'][0:split_Wirkung + 1]}",
                               inline=False)
            split_Wirkung = liturgy_to_cast['Wirkung'][
                            0:min(split_Wirkung + 1024, len(liturgy_to_cast['Wirkung']))].rfind('.')
            embedVar.add_field(name=f'Wirkung 2/3',
                               value=f"{liturgy_to_cast['Wirkung'][split_Wirkung + 1:min(split_Wirkung + 1024, len(liturgy_to_cast['Wirkung']))]}",
                               inline=False)
            embedVar.add_field(name=f'Wirkung 3/3',
                               value=f"{liturgy_to_cast['Wirkung'][split_Wirkung + 1:split_Wirkung + 1024]}",
                               inline=False)
        else:
            split_Wirkung = liturgy_to_cast['Wirkung'][0:1023].rfind('.')
            embedVar.add_field(name=f'Wirkung 1/2', value=f"{liturgy_to_cast['Wirkung'][0:split_Wirkung + 1]}",
                               inline=False)
            embedVar.add_field(name=f'Wirkung 2/2', value=f"{liturgy_to_cast['Wirkung'][split_Wirkung + 1:]}",
                               inline=False)

    else:
        embedVar.add_field(name=f'Wirkung', value=f"{liturgy_to_cast['Wirkung']} ", inline=False)
    embedVar.add_field(name=f'Reichweite', value=f"{liturgy_to_cast['Reichweite']} ", inline=True)
    embedVar.add_field(name=f'Attribute', value=f'{proben[0]}|{proben[1]}|{proben[2]}\n', inline=True)
    embedVar.add_field(name=f'Zielkategorie', value=f"{liturgy_to_cast['Zielkategorie']} ", inline=True)
    embedVar.add_field(name=f'Wirkungsdauer', value=f"{liturgy_to_cast['Wirkungsdauer']} ", inline=True)
    embedVar.add_field(name='Geworfen auf',
                       value=f'{list_of_attributes[0]}|{list_of_attributes[1]}|{list_of_attributes[2]} ', inline=True)
    embedVar.add_field(name='Liturgiedauer', value=f"{liturgy_to_cast['Liturgiedauer']} ", inline=True)
    embedVar.add_field(name=f'Kosten', value=f"{liturgy_to_cast['KaP-Kosten']} ", inline=False)

    return [embedVar, list_of_attributes]


def what_liturgy(message, zahl=0, target=None):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    if message.content.startswith('l '):
        message.content = message.content[2:]
    serverid = str(message.guild)
    author = str(message.author)
    dbname = serverid + author
    name_to_find = str(get_nickname(message))
    if name_to_find == 'Meister':
        if db['Meister'].get(zahl):
            character = db['Meister'].get(zahl)
            name_to_find = str(zahl)
        else:
            embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
            return embedVar
    elif not db[dbname].get(name_to_find):
        embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
        return embedVar
    else:
        character = db[dbname].get(name_to_find)
    words = message.content.split()
    liturgy_to_cast = None
    for key in character['Liturgien'].keys():
        counter = len(words)
        for word in words:
            if word in key.lower():
                counter -= 1
            if counter == 0:
                liturgy_to_cast = key
                break
    return liturgy_to_cast


def cast_liturgy(liturgy_to_cast, liturgy_name, roll_on_this, character_name, character, list_of_modifications=None,
                 tier=None, target=None):
    print('something')
    rolled = [random.randint(1, 20), random.randint(1, 20), random.randint(1, 20)]
    if not target == None:
        if 'SK' in liturgy_to_cast['Proben']:
            for x in range(3):
                roll_on_this[x] -= target['Seelenkraft']
        elif 'ZK' in liturgy_to_cast['Proben']:
            for x in range(3):
                roll_on_this[x] -= target['Zähigkeit']
    fw = liturgy_to_cast['fw']
    for x in range(3):
        if roll_on_this[x] < rolled[x]:
            fw += roll_on_this[x] - rolled[x]
    if 2 >= fw >= 0:
        qs = 1
    else:
        qs = max(0, int(fw / 3))
    embed = casted_embed(rolled, roll_on_this, liturgy_to_cast['fw'], fw, qs, character, character_name, liturgy_name,
                         liturgy_to_cast)
    return [embed, rolled, roll_on_this, liturgy_to_cast['KaP-Kosten']]


def casted_embed(rolled, roll_on_this, max_fw, fw, qs, character, character_name, liturgy_name, liturgy_to_cast):
    print('embed')
    embedVar = discord.Embed(title=character_name, description=f"Spruch", color=0x3498DB)
    embedVar.set_thumbnail(url=str(character['Picture']))
    embedVar.add_field(name=f"{liturgy_name} ({max_fw})", value=liturgy_to_cast['Probe'], inline=False)
    embedVar.add_field(name='Werte:', value=f"{roll_on_this[0]}|{roll_on_this[1]}|{roll_on_this[2]}", inline=True)
    embedVar.add_field(name='Gewürfelt', value=f"{rolled[0]}|{rolled[1]}|{rolled[2]}", inline=True)
    embedVar.add_field(name='Ergebnis', value=f"QS {qs}| FP {fw}/{max_fw}", inline=True)
    if qs > 0:
        embedVar.add_field(name='Erfolg', value='\u200b', inline=False)
    else:
        embedVar.add_field(name='Misserfolg', value='\u200b', inline=False)
    return embedVar
