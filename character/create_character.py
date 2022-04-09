import json
from math import ceil

import discord
import discord.ext
import yaml

from Databases.lists.list import liste_zum_suchen, dict_of_combattalents, list_for_pre_combat, \
    list_for_pre_combat_special_ability, list_for_pre_combat_basic_ability, list_for_combat_special, \
    list_for_combat_basic
from character.characters_do_stuff.talent import get_nickname, fk
from project_buttons.buttons_template import StatusView


class PrintableCharacter:
    embed = ''
    embed1 = ''
    embed2 = ''
    embed3 = ''
    embed4 = ''
    embed5 = ''
    zauber = 0
    liturgie = 0


dict_of_eigenschaften = {
    1: ['MU', 'Mut'],
    2: ['KL', 'Klugheit'],
    3: ['IN', 'Intuition'],
    4: ['CH', 'Charisma'],
    5: ['FF', 'Fingerfertigkeit'],
    6: ['GE', 'Gewandtheit'],
    7: ['KO', 'Konstitution'],
    8: ['KK', 'Körperkraft']
}


def print_character(character, name_to_find):
    """
    :type character character from db
    :type name_to_find: string
    :return embed and view
    """
    Eigenschaften = ''
    for chose_eigenschaft in range(1, 9):
        eigenschaft = dict_of_eigenschaften[chose_eigenschaft]
        Eigenschaften += f"{eigenschaft[0]} = {character[name_to_find][eigenschaft[1]]}\n"

    Grundwerte = f'LeP\t= {character[name_to_find]["actualhp"]} / {character[name_to_find]["LeP"]}\nIni\t= {character[name_to_find]["Initiative"]} +1W6\nGS\t={character[name_to_find]["Geschwindigkeit"]}\nWundschwelle\t={character[name_to_find]["Wundschwelle"]}'

    if character[name_to_find]['Asp'] != 0:
        Grundwerte += "\nAsp\t= " + str(character[name_to_find]['actualAsp']) + '/' + str(
            character[name_to_find]['Asp'])
    elif character[name_to_find]['Karmal'] != 0:
        Grundwerte += "\nKaP\t= " + str(character[name_to_find]['actualKarmal']) + '/' + str(
            character[name_to_find]['Karmal'])
    Grundwerte += "\nSchip\t= " + str(character[name_to_find]['actualSchicksalspunkt']) + "/" + str(
        character[name_to_find]['Schicksalspunkt'])
    Zustaende = ''
    dict_of_zustaende = {
        1: 'Betaeubung',
        2: 'Furcht',
        3: 'Verwirrung',
        4: 'Paralyse',
        5: 'Berauscht'
    }
    if (character[name_to_find]['Zustaende']['Schmerz'] + character[name_to_find]['Zustaende']['Schmerz_durch_Tp']) > 0:
        Zustaende += f"Schmerz\t= {character[name_to_find]['Zustaende']['Schmerz'] + character[name_to_find]['Zustaende']['Schmerz_durch_Tp']}"

    for chose_zustand in range(1, 6):
        zustand = dict_of_zustaende[chose_zustand]
        if character[name_to_find]['Zustaende'][zustand] != 0:
            Zustaende += f"\n{zustand}\t= {character[name_to_find]['Zustaende'][zustand]}"

    return_this = PrintableCharacter

    embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
    embedVar.set_thumbnail(url=str(character[name_to_find]['Picture']))
    embedVar.add_field(name="Eigenschaft", value=Eigenschaften, inline=True)
    embedVar.add_field(name="Grundwerte", value=Grundwerte, inline=True)
    if character[name_to_find].get('Geld'):
        embedVar.add_field(name="Geld",
                           value=f"D {str(character[name_to_find]['Geld'][0])} | S {str(character[name_to_find]['Geld'][1])} | H {str(character[name_to_find]['Geld'][2])} | K {str(character[name_to_find]['Geld'][3])}",
                           inline=False)
    if len(Zustaende) > 0:
        embedVar.add_field(name="Zustände", value=Zustaende, inline=False)

    Nachteile = ''
    for x in character[name_to_find]['Nachteile']:
        Nachteile += f"{x}\n"

    Sonderfertigkeiten = ''
    for x in character[name_to_find]['Sonderfertigkeiten']:
        Sonderfertigkeiten += f"{x}\n"

    Vorteile = ''
    for x in character[name_to_find]['Vorteile']:
        Vorteile += f"{y}\n"

    embedVar2 = discord.Embed(title=name_to_find, description="", color=0x3498DB)
    embedVar2.set_thumbnail(url=str(character[name_to_find]['Picture']))
    embedVar2.add_field(name="Vorteile", value=Vorteile, inline=True)
    embedVar2.add_field(name="Nachteile", value=Nachteile, inline=True)

    embedVar3 = discord.Embed(title=name_to_find, description="", color=0x3498DB)
    embedVar3.set_thumbnail(url=str(character[name_to_find]['Picture']))
    embedVar3.add_field(name="Sonderfertigkeiten", value=Sonderfertigkeiten, inline=True)
    Items = ""
    for x in character[name_to_find]['Items']:
        Items += f'\n {x}'
    Fernkampfwaffe = ''
    if character[name_to_find].get('Fernkampf Waffe'):
        for weapon in character[name_to_find]['Fernkampf Waffe'].keys():
            Fernkampfwaffe += f'\n{weapon}'
    Nahkampfwaffen = ''
    if character[name_to_find].get('Nahkampf Waffen'):
        for weapon in character[name_to_find]['Nahkampf Waffen'].keys():
            Nahkampfwaffen += f'\n{weapon}'
    embedVar4 = discord.Embed(title=name_to_find, description="", color=0x3498DB)
    embedVar4.set_thumbnail(url=str(character[name_to_find]['Picture']))
    if character[name_to_find].get('Items'):
        embedVar4.add_field(name="Gegenstände", value=Items, inline=True)
    else:
        embedVar4.add_field(name="Gegenstände", value='Keine im Inventar', inline=True)
    if character[name_to_find].get('Nahkampf Waffen'):
        embedVar4.add_field(name="Nahkampfwaffen", value=Nahkampfwaffen, inline=True)
    if character[name_to_find].get('Fernkampf Waffe'):
        embedVar4.add_field(name="Fernkampfwaffen", value=Fernkampfwaffe, inline=True)

    Zauber = ""
    for x in character[name_to_find]['Zauber']:
        Zauber += f'\n {x}'
    embedVar5 = discord.Embed(title=name_to_find, description="", color=0x3498DB)
    embedVar5.set_thumbnail(url=str(character[name_to_find]['Picture']))
    if character[name_to_find].get('Zauber'):
        embedVar5.add_field(name="Zauber", value=Zauber, inline=False)
        return_this.zauber = 1

    Liturgie = ""
    for x in character[name_to_find]['Liturgien']:
        zahl = str(character[name_to_find]['Liturgien'][x]['fw'])
        Liturgie += f'\n {x}({zahl})'
    embedVar6 = discord.Embed(title=name_to_find, description="", color=0x3498DB)
    embedVar6.set_thumbnail(url=str(character[name_to_find]['Picture']))
    if character[name_to_find].get('Liturgien'):
        embedVar6.add_field(name="Liturgie", value=Liturgie, inline=False)
        return_this.liturgie = 1

    return_this.embed = embedVar
    return_this.embed1 = embedVar2
    return_this.embed2 = embedVar3
    return_this.embed3 = embedVar4
    return_this.embed4 = embedVar5
    return_this.embed5 = embedVar6
    return return_this


class charactere(object):
    def __init__(self, dateCreated, dateModified, id, phase, locale, name, ap, el, r, p, sex, pers, attr, activatable,
                 talents, ct, spells, cantrips, liturgies, blessings, belongings, rules, pets, *args, **kwargs):
        self.r = r
        self.name = name
        self.pers = pers
        self.attr = attr
        self.activatable = activatable
        self.talents = talents
        self.ct = ct
        self.spells = spells
        self.cantrips = cantrips
        self.lituriges = liturgies
        self.blessings = blessings
        self.belongings = belongings
        self.pets = pets


def loading_character(message: discord.Message, newchar):
    char = charactere(**newchar)
    printable_character = create_char(char, message, "")
    nickname = get_nickname(message)
    view = StatusView(get_nickname=nickname, embed=printable_character)
    return [printable_character.embed, view]


def create_char(character, message, string):
    print('Create_Char')
    with open("Databases/Nachteile.yaml", 'r', encoding='utf8') as stream:
        nt = yaml.safe_load(stream)
    with open("Databases/Vorteile.yaml", 'r', encoding='utf8') as stream:
        vt = yaml.safe_load(stream)
    with open("Databases/Sonderfertigkeiten.yaml", 'r', encoding='utf8') as stream:
        sf = yaml.safe_load(stream)
    name = character.name
    serverid = str(message.guild)
    author = str(message.author)
    dbname = serverid + author
    # Sonderfertigkeiten

    safe_id = -1
    for x in range(len(sf)):

        if int(sf[x].get('id')[3:]) != safe_id + 1:
            print(sf[x].get('id')[3:])
        safe_id = int(sf[x].get('id')[3:])
    # Nachteile
    Mut = Klugheit = Intuition = Charisma = Fingerfertigkeit = Gewandtheit = Konstitution = Körperkraft = 8
    for x in range(0, 8):
        if character.attr['values'][x]['id'] == "ATTR_1":
            Mut = character.attr['values'][x]['value']
        elif character.attr['values'][x]['id'] == "ATTR_2":
            Klugheit = character.attr['values'][x]['value']
        elif character.attr['values'][x]['id'] == "ATTR_3":
            Intuition = character.attr['values'][x]['value']
        elif character.attr['values'][x]['id'] == "ATTR_4":
            Charisma = character.attr['values'][x]['value']
        elif character.attr['values'][x]['id'] == "ATTR_5":
            Fingerfertigkeit = character.attr['values'][x]['value']
        elif character.attr['values'][x]['id'] == "ATTR_6":
            Gewandtheit = character.attr['values'][x]['value']
        elif character.attr['values'][x]['id'] == "ATTR_7":
            Konstitution = character.attr['values'][x]['value']
        elif character.attr['values'][x]['id'] == "ATTR_8":
            Körperkraft = character.attr['values'][x]['value']

    lep = 0

    if character.r == "R_1":  # human
        LeP = round(5 + 2 * Konstitution + lep + 0.49)
        Seelenkraft = round(-5 + (Mut + Klugheit + Intuition) / 6 + 0.49)
        Zaehigkeit = round(-5 + (Konstitution + Konstitution + Körperkraft) / 6 + 0.49)
        Initiative = round((Mut + Gewandtheit) / 2 + 0.49)
        Geschwindigkeit = round(8 + 0.49)

    elif character.r == "R_2":  # elves
        LeP = round(2 + 2 * Konstitution + lep + 0.49)
        Seelenkraft = round(-4 + (Mut + Klugheit + Intuition) / 6 + 0.49)
        Zaehigkeit = round(-6 + (Konstitution + Konstitution + Körperkraft) / 6 + 0.49)
        Initiative = round((Mut + Gewandtheit) / 2 + 0.49)
        Geschwindigkeit = round(8 + 0.49)

    elif character.r == "R_3":  # halfelf
        LeP = round(5 + 2 * Konstitution + lep)
        Seelenkraft = round(-4 + (Mut + Klugheit + Intuition) / 6 + 0.49)
        Zaehigkeit = round(-6 + (Konstitution + Konstitution + Körperkraft) / 6 + 0.49)
        Initiative = round((Mut + Gewandtheit) / 2 + 0.49)
        Geschwindigkeit = round(8 + 0.49)

    elif character.r == "R_4":  # dwarf
        LeP = round(8 + 2 * Konstitution + lep + 0.49)
        Seelenkraft = round(-4 + (Mut + Klugheit + Intuition) / 6 + 0.49)
        Zaehigkeit = round(-4 + (Konstitution + Konstitution + Körperkraft) / 6 + 0.49)
        Initiative = round((Mut + Gewandtheit) / 2 + 0.49)
        Geschwindigkeit = round(6 + 0.49)

    Kampftalente = [6] * 21
    for x in character.ct:
        if x.startswith("CT_"):
            if x[3:4].isnumeric():
                if x[4:5].isnumeric():
                    check = int(x[3:5])
                    Kampftalente[check - 1] = character.ct[x]
                else:
                    check = int(x[3:4])
                    Kampftalente[check - 1] = character.ct[x]

    eisernchecker = 0
    glueck = 0

    for x in character.activatable:
        if x == 'ADV_54':
            if len(character.activatable['ADV_54']):
                eisernchecker = 1
                print('ist eisern')
        if x == 'DISADV_4':
            if len(character.activatable['DISADV_4']):
                print('ist nicht eisern')
                eisernchecker = -1
        if x == 'DISADV_31':
            if len(character.activatable['DISADV_31']) != 0:
                glueck = -character.activatable['DISADV_31'][0].get('tier')
        if x == 'ADV_14':
            if len(character.activatable['ADV_14']) != 0:
                glueck = character.activatable['ADV_14'][0].get('tier')
        if x == 'ADV_9':
            if len(character.activatable['ADV_9']):
                Geschwindigkeit += 1
        if x == 'DISADV_4':
            print(len(character.activatable['DISADV_4']))
            if len(character.activatable['DISADV_4']):
                Geschwindigkeit -= 1

    Furcht_min = Schmerz_min = Betaeubung_min = Verwirrung_min = Paralyse_min = Berauscht_min = 0
    LeP = LeP + int(character.attr['lp'])
    Schicksalspunkt = 3 + glueck
    Asp = 0
    Karmal = 0
    Schmerz = 0
    Wundschwelle = int((Konstitution + 1) / 2) + eisernchecker

    special_abilities = []
    disadvantages = []
    advantages = []
    spell_extension = []
    liturgy_extension = []
    combat_special_abilities_special = []
    combat_special_abilities_basic = []
    pre_combat_abilities_basic = []
    pre_combat_special = []
    pre_combat_abilities_special = []
    for x in character.activatable:
        if x.startswith('SA_'):
            if character.activatable[x]:
                special_ability_name = sf[int(x[3:])]['name']
                if character.activatable[x][0].get('sid'):
                    for y in range(len(character.activatable[x])):
                        value_to_check = character.activatable[x][y]

                        if value_to_check.get('sid') and value_to_check.get('sid2') and not isinstance(
                                value_to_check['sid'], str):
                            break
                        if value_to_check.get('sid') and value_to_check.get('sid2') and value_to_check[
                            'sid'].startswith('TAL_'):
                            add_sid = ' ' + fk[int(value_to_check['sid'][4:]) - 1]['name']
                            add_sid += ' ' + fk[int(value_to_check['sid'][4:]) - 1]['applications'][
                                value_to_check['sid2'] - 1]['name']
                            special_ability_name += add_sid
                            continue

                        if special_ability_name == 'Anatomie':
                            add_sid = ' ' + value_to_check.get('sid')
                            special_ability_name += add_sid
                            continue

                        if special_ability_name == 'Eigene Sonderfertigkeit':
                            name_of_eigene_Sonderfertigkeit = value_to_check.get('sid').split(', ')
                            for x in name_of_eigene_Sonderfertigkeit:
                                new_list = [x]
                                special_abilities.append(new_list)
                            continue

                        # debug only
                        if not sf[int(x[3:])].get('selectOptions'):
                            if int(x[3:]) == 414:
                                spell_extension.append(character.activatable[x])
                            elif int(x[3:]) == 663:
                                liturgy_extension.append(character.activatable[x])
                            continue
                        if isinstance(value_to_check.get('sid'), int):
                            add_sid = ' ' + str(
                                sf[int(x[3:])]['selectOptions'][int(value_to_check.get('sid')) - 1]['name'])
                        else:
                            add_sid = ' ' + value_to_check.get('sid')
                        if character.activatable[x][y].get('sid2'):
                            add_sid += ' ' + str(value_to_check.get('sid2'))
                        if character.activatable[x][y].get('tier'):
                            add_sid += ' ' + str(character.activatable[x][y].get('tier'))
                        special_ability_name += add_sid
                elif character.activatable[x][0].get('tier'):
                    special_ability_name += ' ' + str(character.activatable[x][0].get('tier'))
                if special_ability_name in list_for_pre_combat.keys():
                    pre_combat_special.append(special_ability_name)
                elif special_ability_name in list_for_pre_combat_special_ability.keys():
                    pre_combat_abilities_special.append(special_ability_name)
                elif special_ability_name in list_for_pre_combat_basic_ability.keys():
                    pre_combat_abilities_basic.append(special_ability_name)
                elif special_ability_name in list_for_combat_special.keys():
                    combat_special_abilities_special.append(special_ability_name)
                elif special_ability_name in list_for_combat_basic.keys():
                    combat_special_abilities_basic.append(special_ability_name)
                special_abilities.append(special_ability_name)

        if x.startswith('DISADV_'):
            if character.activatable[x]:
                number_to_look_up = int(x[7:])
                disadvantage_Name = nt[number_to_look_up]['name']
                print(disadvantage_Name)
                if character.activatable[x][0].get('sid'):
                    for y in range(len(character.activatable[x])):
                        value_to_check = character.activatable[x][y]

                        if isinstance(value_to_check.get('sid'), int):
                            add_sid = ' ' + nt[number_to_look_up]['selectOptions'][value_to_check.get('sid') - 1][
                                'name']
                        else:
                            add_sid = ' ' + str(value_to_check.get('sid'))
                        if character.activatable[x][y].get('sid2'):
                            add_sid += ' ' + value_to_check.get('sid2')
                        if character.activatable[x][y].get('tier'):
                            add_sid += ' ' + str(character.activatable[x][y].get('tier'))
                    disadvantage_Name += add_sid
                elif character.activatable[x][0].get('tier'):
                    disadvantage_Name += ' ' + str(character.activatable[x][0].get('tier'))
                # BEGABUNG
                if disadvantage_Name.startswith('Unfähig TAL'):
                    is_the_word_to_find = disadvantage_Name[disadvantage_Name.find('TAL_'):]
                    for word in liste_zum_suchen:
                        if word.endswith(is_the_word_to_find):
                            disadvantage_Name = "Unfähigkeit " + word[:word.find(' TAL_')]
                            break
                # print(disadvantage_Name)
                disadvantages.append(disadvantage_Name)

        if x.startswith('ADV_'):
            if character.activatable[x]:
                number_to_look_up = int(x[4:])
                advantage_Name = vt[number_to_look_up]['name']
                if character.activatable[x][0].get('sid'):
                    for y in range(len(character.activatable[x])):
                        value_to_check = character.activatable[x][y]
                        if isinstance(value_to_check.get('sid'), int):
                            add_sid = ' ' + vt[number_to_look_up]['selectOptions'][value_to_check.get('sid')]['name']
                        else:
                            add_sid = ' ' + str(value_to_check.get('sid'))
                        if character.activatable[x][y].get('sid2'):
                            add_sid += ' ' + value_to_check.get('sid2')
                        if character.activatable[x][y].get('tier'):
                            add_sid += ' ' + str(character.activatable[x][y].get('tier'))
                    advantage_Name += add_sid
                elif character.activatable[x][0].get('tier'):
                    advantage_Name += ' ' + str(character.activatable[x][0].get('tier'))
                # BEGABUNG
                if advantage_Name.startswith('Begabung TAL'):
                    is_the_word_to_find = advantage_Name[advantage_Name.find('TAL_'):]
                    for word in liste_zum_suchen:
                        if word.endswith(is_the_word_to_find):
                            advantage_Name = "Begabung " + word[:word.find(' TAL_')]
                            break
                advantages.append(advantage_Name)

        if x == "ADV_25":  # hohe Lebenskraft
            print(character.activatable[x])
            try:
                LeP = LeP + character.activatable[x][0].get('tier')
            except:
                pass
        if x == "DISADV_28":
            print(character.activatable[x])
            try:
                LeP = LeP - character.activatable[x][0].get('tier')
            except:
                pass
        if x == 'ADV_49':
            Schmerz -= -1
            Schmerz_min -= -1

        if x == "SA_680":  # Gildenmagier
            Asp = Klugheit + 20
        elif x == "SA_681":  ##Qabalya Mage
            Asp = Klugheit + 20
        elif x == "SA_679":
            Asp = 20
        elif x == 'SA_346':  # druid
            Asp = 20 + Klugheit
        elif x == "SA_345":  # elf
            Asp = 20 + Intuition
        if x == "SA_86":
            Karmal = 20 + Klugheit
        elif x == "SA_682":
            Karmal = 20 + Mut
        elif x == "SA_683":
            Karmal = 20 + Mut
        elif x == "SA_684":
            Karmal = 20 + Klugheit
        elif x == "SA_685":
            Karmal = 20 + Intuition
        elif x == "SA_686":
            Karmal = 20 + Intuition
        elif x == "SA_687":
            Karmal = 20 + Charisma
        elif x == "SA_688":
            Karmal = 20 + Klugheit
        elif x == "SA_689":
            Karmal = 20 + Mut
        elif x == "SA_690":
            Karmal = 20 + Charisma
        elif x == "SA_691":
            Karmal = 20 + Intuition
        elif x == "SA_692":
            Karmal = 20 + Charisma
        elif x == "SA_693":
            Karmal = 20 + Mut
        elif x == "SA_694":
            Karmal = 20 + Intuition
        elif x == "SA_695":
            Karmal = 20 + Charisma
        elif x == "SA_696":
            Karmal = 20 + Mut
        elif x == "SA_697":
            Karmal = 20 + Klugheit
        elif x == "SA_698":
            Karmal = 20 + Mut

    actualKarmal = Karmal
    actualhp = LeP
    actualAsp = Asp

    Zauber = character.spells
    Zauber = get_zauber(Zauber)

    Liturgien = character.lituriges
    Liturgien = get_liturgy(Liturgien)

    Zaubertrick = character.cantrips
    Segen = character.blessings

    actualSchicksalspunkt = Schicksalspunkt
    Geld = [0, 0, 0, 0]
    Items = []
    meele_weapons = {}
    ranged_weapons = {}
    for item in character.belongings.get('items'):
        if character.belongings.get('items').get(item).get('combatTechnique'):
            if character.belongings.get('items').get(item).get('primaryThreshold'):
                new_weapon = {character.belongings.get('items').get(item).get('name'): {
                    'at_mod': character.belongings.get('items').get(item).get('at'),
                    'pa_mod': character.belongings.get('items').get(item).get('pa'),
                    'range': character.belongings.get('items').get(item).get('reach'),
                    'combatTechnique':
                        dict_of_combattalents[character.belongings.get('items').get(item).get('combatTechnique')][0],
                    'damageDiceSides': character.belongings.get('items').get(item).get('damageDiceSides'),
                    'damageDiceNumber': character.belongings.get('items').get(item).get('damageDiceNumber'),
                    'damageFlat': character.belongings.get('items').get(item).get('damageFlat'),
                    'threshold': character.belongings.get('items').get(item).get('primaryThreshold').get('threshold')}}
                meele_weapons.update(new_weapon)
            else:
                print(character.belongings.get('items').get(item))
                new_weapon = {character.belongings.get('items').get(item).get('name'): {
                    'at_mod': character.belongings.get('items').get(item).get('at'),
                    'range': character.belongings.get('items').get(item).get('reach'),
                    'combatTechnique':
                        dict_of_combattalents[character.belongings.get('items').get(item).get('combatTechnique')][0],
                    'damageDiceSides': character.belongings.get('items').get(item).get('damageDiceSides'),
                    'damageDiceNumber': character.belongings.get('items').get(item).get('damageDiceNumber'),
                    'damageFlat': character.belongings.get('items').get(item).get('damageFlat')}}
                ranged_weapons.update(new_weapon)
        else:
            Items.append(character.belongings.get('items').get(item).get('name'))

    talente = [0] * 60
    for x in character.talents:
        name_of_talent = int(x[4:])
        talente[name_of_talent] = character.talents[x]
    Picture = ""
    list_von_Zustaenden = []
    Furcht = Schmerz_durch_Tp = Verwirrung = Betaeubung = Paralyse = 0

    with open('jsoned_characters.json', encoding='utf8') as f:
        db = json.load(f)

    if db.get(dbname) and db[dbname].get(name):
        print('found the same character')
        actualhp = db[dbname].get(name).get('actualhp')
        actualAsp = db[dbname].get(name).get('actualAsp')
        actualSchicksalspunkt = db[dbname].get(name).get('actualSchicksalspunkt')
        actualKarmal = db[dbname].get(name).get('actualKarmal')
        Picture = db[dbname].get(name).get('Picture')
        if db[dbname].get(name).get('Geld'):
            Geld = db[dbname].get(name)['Geld']
        Schmerz = db[dbname].get(name).get('Zustaende').get('Schmerz')
        Schmerz_durch_Tp = db[dbname].get(name).get('Zustaende').get('Schmerz_durch_Tp')
        Furcht = db[dbname].get(name).get('Zustaende').get('Furcht')
        Verwirrung = db[dbname].get(name).get('Zustaende').get('Verwirrung')
        Paralyse = db[dbname].get(name).get('Zustaende').get('Paralyse')
        if db[dbname].get(name).get('list_von_Zustaenden'):
            list_von_Zustaenden = db[dbname].get(name).get('list_von_Zustaenden')
        else:
            list_von_Zustaenden = []

    Liste_der_Kampftalente = [None] * 21
    eigenschaften = {
        "Fingerfertigkeit": Fingerfertigkeit,
        "Körperkraft": Körperkraft,
        "Gewandtheit": Gewandtheit,
        "Mut": Mut,
        "nichts": 0
    }

    for x in range(1, 21):
        defense_attribute = int((max(eigenschaften[dict_of_combattalents['CT_' + str(x)][1]],
                                     eigenschaften[dict_of_combattalents['CT_' + str(x)][2]]) - 8) / 3)

    offensive_attribute = int((Mut - 8) / 3)
    kampf_talent_name = dict_of_combattalents['CT_' + str(x)][0]
    if not character.ct.get('CT_' + str(x)):
        Liste_der_Kampftalente[x - 1] = {kampf_talent_name: {'at': 6 + offensive_attribute,
                                                             'pa': 3 + defense_attribute}}
    else:
        ktw = character.ct.get('CT_' + str(x))
        Liste_der_Kampftalente[x - 1] = {kampf_talent_name: {'at': ktw + offensive_attribute,
                                                             'pa': ceil(ktw / 2) + defense_attribute}}

    if get_nickname(message) == 'Meister':
        print('Meistere')
        if db.get('Meister'):
            object_together = db['Meister']
            object_together.update({name:
                                        {'Picture': Picture, 'alive': True, 'LeP': LeP, 'actualhp': actualhp,
                                         'Asp': Asp, 'actualAsp': actualAsp,
                                         'Karmal': Karmal, 'actualKarmal': actualKarmal, 'Seelenkraft': Seelenkraft,
                                         'Zaehigkeit': Zaehigkeit,
                                         'Initiative': Initiative, 'Wundschwelle': Wundschwelle,
                                         'Geschwindigkeit': Geschwindigkeit,
                                         'Körperkraft': Körperkraft, 'modKK': 0, 'Konstitution': Konstitution,
                                         'modKO': 0,
                                         'Gewandtheit': Gewandtheit, 'modGE': 0, 'Fingerfertigkeit': Fingerfertigkeit,
                                         'modFF': 0,
                                         'Klugheit': Klugheit, 'modKL': 0, 'Intuition': Intuition, 'modIN': 0,
                                         'Mut': Mut, 'modMU': 0,
                                         'Charisma': Charisma, 'modCH': 0, 'Talente': talente,
                                         'Kampftalente': Liste_der_Kampftalente, 'Zauber': Zauber,
                                         "Zaubertrick": Zaubertrick, "Liturgien": Liturgien, 'Segen': Segen,
                                         'Schicksalspunkt': Schicksalspunkt,
                                         'actualSchicksalspunkt': actualSchicksalspunkt, 'Zustaende':
                                             {'Betaeubung': Betaeubung, 'Betaeubung_min': Betaeubung_min,
                                              'Schmerz': Schmerz, 'Schmerz_min': Schmerz_min,
                                              'Schmerz_durch_Tp': Schmerz_durch_Tp, 'Berauscht': 0,
                                              'Berauscht_min': Berauscht_min, 'Entrueckung': 0,
                                              'Furcht': Furcht, 'Furcht_min': Furcht_min, 'Paralyse': Paralyse,
                                              'Paralyse_min': Paralyse_min, 'Verwirrung': Verwirrung,
                                              'Verwirrung_min': Verwirrung_min, 'Überanstrengung': 0, 'Trance': 0},
                                         'Geld': Geld,
                                         'Sonderfertigkeiten': special_abilities,
                                         'Kampf Spezialmanöver': combat_special_abilities_special,
                                         'Kampf Basismanöver': combat_special_abilities_basic,
                                         'Kampfrunde Basismanöver': pre_combat_abilities_basic,
                                         'Kampfrunde Spezialmanöver': pre_combat_abilities_special,
                                         'Kampfrunde': pre_combat_special,
                                         'Nachteile': disadvantages, 'Vorteile': advantages,
                                         'Nahkampf Waffen': meele_weapons, 'Fernkampf Waffe': ranged_weapons,
                                         'Items': Items, 'liste_von_Zustaenden': list_von_Zustaenden}})
            db[dbname] = object_together
        else:
            print('erstes mal')
            db['Meister'] = {name:
                                 {'Picture': Picture, 'alive': True, 'LeP': LeP, 'actualhp': actualhp,
                                  'Asp': Asp, 'actualAsp': actualAsp,
                                  'Karmal': Karmal, 'actualKarmal': actualKarmal, 'Seelenkraft': Seelenkraft,
                                  'Zaehigkeit': Zaehigkeit,
                                  'Initiative': Initiative, 'Wundschwelle': Wundschwelle,
                                  'Geschwindigkeit': Geschwindigkeit,
                                  'Körperkraft': Körperkraft, 'modKK': 0, 'Konstitution': Konstitution,
                                  'modKO': 0,
                                  'Gewandtheit': Gewandtheit, 'modGE': 0, 'Fingerfertigkeit': Fingerfertigkeit,
                                  'modFF': 0,
                                  'Klugheit': Klugheit, 'modKL': 0, 'Intuition': Intuition, 'modIN': 0,
                                  'Mut': Mut, 'modMU': 0,
                                  'Charisma': Charisma, 'modCH': 0, 'Talente': talente,
                                  'Kampftalente': Liste_der_Kampftalente, 'Zauber': Zauber,
                                  "Zaubertrick": Zaubertrick, "Liturgien": Liturgien, 'Segen': Segen,
                                  'Schicksalspunkt': Schicksalspunkt,
                                  'actualSchicksalspunkt': actualSchicksalspunkt, 'Zustaende':
                                      {'Betaeubung': Betaeubung, 'Betaeubung_min': Betaeubung_min,
                                       'Schmerz': Schmerz, 'Schmerz_min': Schmerz_min,
                                       'Schmerz_durch_Tp': Schmerz_durch_Tp, 'Berauscht': 0,
                                       'Berauscht_min': Berauscht_min, 'Entrueckung': 0,
                                       'Furcht': Furcht, 'Furcht_min': Furcht_min, 'Paralyse': Paralyse,
                                       'Paralyse_min': Paralyse_min, 'Verwirrung': Verwirrung,
                                       'Verwirrung_min': Verwirrung_min, 'Überanstrengung': 0, 'Trance': 0},
                                  'Geld': Geld,
                                  'Sonderfertigkeiten': special_abilities,
                                  'Kampf Spezialmanöver': combat_special_abilities_special,
                                  'Kampf Basismanöver': combat_special_abilities_basic,
                                  'Kampfrunde Basismanöver': pre_combat_abilities_basic,
                                  'Kampfrunde Spezialmanöver': pre_combat_abilities_special,
                                  'Kampfrunde': pre_combat_special,
                                  'Nachteile': disadvantages, 'Vorteile': advantages,
                                  'Nahkampf Waffen': meele_weapons, 'Fernkampf Waffe': ranged_weapons,
                                  'Items': Items, 'liste_von_Zustaenden': list_von_Zustaenden}}
    elif db.get(dbname):
        object_together = db[dbname]
        object_together.update({name:
                                    {'Picture': Picture, 'alive': True, 'LeP': LeP, 'actualhp': actualhp,
                                     'Asp': Asp, 'actualAsp': actualAsp,
                                     'Karmal': Karmal, 'actualKarmal': actualKarmal, 'Seelenkraft': Seelenkraft,
                                     'Zaehigkeit': Zaehigkeit,
                                     'Initiative': Initiative, 'Wundschwelle': Wundschwelle,
                                     'Geschwindigkeit': Geschwindigkeit,
                                     'Körperkraft': Körperkraft, 'modKK': 0, 'Konstitution': Konstitution,
                                     'modKO': 0,
                                     'Gewandtheit': Gewandtheit, 'modGE': 0, 'Fingerfertigkeit': Fingerfertigkeit,
                                     'modFF': 0,
                                     'Klugheit': Klugheit, 'modKL': 0, 'Intuition': Intuition, 'modIN': 0,
                                     'Mut': Mut, 'modMU': 0,
                                     'Charisma': Charisma, 'modCH': 0, 'Talente': talente,
                                     'Kampftalente': Liste_der_Kampftalente, 'Zauber': Zauber,
                                     "Zaubertrick": Zaubertrick, "Liturgien": Liturgien, 'Segen': Segen,
                                     'Schicksalspunkt': Schicksalspunkt,
                                     'actualSchicksalspunkt': actualSchicksalspunkt, 'Zustaende':
                                         {'Betaeubung': Betaeubung, 'Betaeubung_min': Betaeubung_min,
                                          'Schmerz': Schmerz, 'Schmerz_min': Schmerz_min,
                                          'Schmerz_durch_Tp': Schmerz_durch_Tp, 'Berauscht': 0,
                                          'Berauscht_min': Berauscht_min, 'Entrueckung': 0,
                                          'Furcht': Furcht, 'Furcht_min': Furcht_min, 'Paralyse': Paralyse,
                                          'Paralyse_min': Paralyse_min, 'Verwirrung': Verwirrung,
                                          'Verwirrung_min': Verwirrung_min, 'Überanstrengung': 0, 'Trance': 0},
                                     'Geld': Geld,
                                     'Sonderfertigkeiten': special_abilities,
                                     'Kampf Spezialmanöver': combat_special_abilities_special,
                                     'Kampf Basismanöver': combat_special_abilities_basic,
                                     'Kampfrunde Basismanöver': pre_combat_abilities_basic,
                                     'Kampfrunde Spezialmanöver': pre_combat_abilities_special,
                                     'Kampfrunde': pre_combat_special,
                                     'Nachteile': disadvantages, 'Vorteile': advantages,
                                     'Nahkampf Waffen': meele_weapons, 'Fernkampf Waffe': ranged_weapons,
                                     'Items': Items, 'liste_von_Zustaenden': list_von_Zustaenden}})
    else:
        db[dbname] = {name:
                          {'Picture': Picture, 'alive': True, 'LeP': LeP, 'actualhp': actualhp,
                           'Asp': Asp, 'actualAsp': actualAsp,
                           'Karmal': Karmal, 'actualKarmal': actualKarmal, 'Seelenkraft': Seelenkraft,
                           'Zaehigkeit': Zaehigkeit,
                           'Initiative': Initiative, 'Wundschwelle': Wundschwelle,
                           'Geschwindigkeit': Geschwindigkeit,
                           'Körperkraft': Körperkraft, 'modKK': 0, 'Konstitution': Konstitution,
                           'modKO': 0,
                           'Gewandtheit': Gewandtheit, 'modGE': 0, 'Fingerfertigkeit': Fingerfertigkeit,
                           'modFF': 0,
                           'Klugheit': Klugheit, 'modKL': 0, 'Intuition': Intuition, 'modIN': 0,
                           'Mut': Mut, 'modMU': 0,
                           'Charisma': Charisma, 'modCH': 0, 'Talente': talente,
                           'Kampftalente': Liste_der_Kampftalente, 'Zauber': Zauber,
                           "Zaubertrick": Zaubertrick, "Liturgien": Liturgien, 'Segen': Segen,
                           'Schicksalspunkt': Schicksalspunkt,
                           'actualSchicksalspunkt': actualSchicksalspunkt, 'Zustaende':
                               {'Betaeubung': Betaeubung, 'Betaeubung_min': Betaeubung_min,
                                'Schmerz': Schmerz, 'Schmerz_min': Schmerz_min,
                                'Schmerz_durch_Tp': Schmerz_durch_Tp, 'Berauscht': 0,
                                'Berauscht_min': Berauscht_min, 'Entrueckung': 0,
                                'Furcht': Furcht, 'Furcht_min': Furcht_min, 'Paralyse': Paralyse,
                                'Paralyse_min': Paralyse_min, 'Verwirrung': Verwirrung,
                                'Verwirrung_min': Verwirrung_min, 'Überanstrengung': 0, 'Trance': 0},
                           'Geld': Geld,
                           'Sonderfertigkeiten': special_abilities,
                           'Kampf Spezialmanöver': combat_special_abilities_special,
                           'Kampf Basismanöver': combat_special_abilities_basic,
                           'Kampfrunde Basismanöver': pre_combat_abilities_basic,
                           'Kampfrunde Spezialmanöver': pre_combat_abilities_special,
                           'Kampfrunde': pre_combat_special,
                           'Nachteile': disadvantages, 'Vorteile': advantages,
                           'Nahkampf Waffen': meele_weapons, 'Fernkampf Waffe': ranged_weapons,
                           'Items': Items, 'liste_von_Zustaenden': list_von_Zustaenden}}

    if get_nickname(message) == 'Meister':
        character = db['Meister']
    else:
        character = db[dbname]
    string = print_character(character, str(name))

    with open('jsoned_characters.json', 'w', encoding='utf8') as f:
        json.dump(db, f)
    return string


def get_zauber(zauber):
    if len(zauber.keys()) < 1:
        return {}

    from Databases.lists.list import liste_für_zauber
    from Databases.lists.zauber_liste import zauber_liste
    spells_from_character = {}
    for zauber_name in zauber.keys():
        fw = zauber.get(zauber_name)
        for word in liste_für_zauber:
            if word.endswith(zauber_name):
                zauber_name = word[:len(word) - len(zauber_name) - 1]
                break
        for word in zauber_liste.keys():
            if word == zauber_name:
                spells_from_character[word] = zauber_liste.get(word)
                spells_from_character[word].update({'fw': fw})
    return spells_from_character


def get_liturgy(liturgy):
    if len(liturgy.keys()) < 1:
        return {}

    from Databases.lists.list import liste_für_Liturgien
    from Databases.lists.liturgy_list import liturgy_list

    liturgies_from_character = {}
    for liturgie_name in liturgy.keys():
        fw = liturgy.get(liturgie_name)
        for word in liste_für_Liturgien:
            if word.endswith(liturgie_name):
                liturgie_name = word[:len(word) - len(liturgie_name) - 1]
                break
        for word in liturgy_list:
            if word == liturgie_name:
                liturgies_from_character[word] = liturgy_list.get(word)
                liturgies_from_character[word].update({'fw': fw})
    return liturgies_from_character
