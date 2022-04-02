import discord
import discord.ext
import json
from math import ceil

from character.characters_do_stuff.talent import get_nickname


def LP_reg_or_dmg(message, sign, number, zone, zahl=0, asp=False, kap=False):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    serverid = str(message.guild)
    author = str(message.author)
    dbname = serverid + author
    name_to_find = str(get_nickname(message))

    liegt_im_sterben = 0
    number = int(number)

    if name_to_find == 'Meister':
        if db['Meister'].get(zahl):
            character = db['Meister'].get(str(zahl))
            name_to_find = str(zahl)
        else:
            embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
            return embedVar
    elif not db[dbname].get(name_to_find):
        embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
        return embedVar
    else:
        character = db[dbname].get(name_to_find)
    dict_for_lep_kap_asp = {"asp": ["Asp", "actualAsp", "Astralpunkte"],
                            "kap": ["Karmal", "actualKarmal", "Karmalpunkte"],
                            "lep": ['LeP', 'actualhp', 'Lebenspunkte']}

    decider = "lep"
    if asp == True:
        decider = "asp"
    elif kap == True:
        decider = 'kap'
    lep_dict = {int(ceil(3/4 * character['LeP'])): 1,
                int(ceil(2/4 * character['LeP'])): 2,
                int(ceil(1/4 * character['LeP'])): 3,
                5: 4}

    if sign == '+':
        difference = character[dict_for_lep_kap_asp[decider][0]] - character[
            dict_for_lep_kap_asp[decider][1]] - number
        if difference < 0:
            character[dict_for_lep_kap_asp[decider][1]] = character[dict_for_lep_kap_asp[decider][0]]
        else:
            character[dict_for_lep_kap_asp[decider][1]] = character[dict_for_lep_kap_asp[decider][1]] + number
    elif sign == '-':
        character[dict_for_lep_kap_asp[decider][1]] = character[dict_for_lep_kap_asp[decider][1]] - number
        if character[dict_for_lep_kap_asp[decider][1]] < 0 and decider == "lep":
            liegt_im_sterben = 1
    if decider == "lep":
        never_taken = 0
        for x in lep_dict.keys():
            if character['actualhp'] < x:
                never_taken = 1
                character['Zustaende']['Schmerz_durch_Tp'] = lep_dict[x]
        if never_taken == 0:
            character['Zustaende']['Schmerz_durch_Tp'] = 0

    embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
    embedVar.set_thumbnail(url=str(character['Picture']))
    embedVar.add_field(name=f"{dict_for_lep_kap_asp[decider][2]}", value=(f"{character[dict_for_lep_kap_asp[decider][1]]}/{character[dict_for_lep_kap_asp[decider][0]]}"),inline=False)
    embedVar.set_footer(text=f"Letzte Änderung: {sign}{number}")
    if liegt_im_sterben == 1:
        embedVar.add_field(name="", value=(' liegt im sterben '), inline=False)

    db[dbname][name_to_find].update(character)
    with open('jsoned_characters.json', 'w') as f:
        json.dump(db, f)
    return embedVar


def changing_money(message, sign, number, money_typ):
    print('changing money')
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    serverid = str(message.guild)
    author = str(message.author)
    dbname = serverid + author
    name_to_find = str(get_nickname(message))
    if not db[dbname].get(name_to_find):
        embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
        return embedVar
    else:
        character = db[dbname].get(name_to_find)
    if number == '':
        number = 1
    else:
        number = int(number)
    money_dict = {
        'd': 0,
        's': 1,
        'h': 2,
        'k': 3,
    }
    money_dict_string = {
        'd': 'Dukate',
        's': 'Silbertaler',
        'h': 'Heller',
        'k': 'Kreuzer'
    }
    if sign == '-':
        if character['Geld'][money_dict[money_typ]] >= number:
            character['Geld'][money_dict[money_typ]] -= number
            embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
            embedVar.add_field(name="Geld",
                               value=f"D {str(character['Geld'][0])} | S {str(character['Geld'][1])} | H {str(character['Geld'][2])} | K {str(character['Geld'][3])}",
                               inline=False)
            embedVar.set_footer(text=f"Letzte Änderung: {sign}{number} {money_dict_string[money_typ]}")
            db[dbname][name_to_find].update(character)
            with open('jsoned_characters.json', 'w') as f:
                json.dump(db, f)
            return embedVar
        else:
            saved_number = number
            converted = character['Geld'][3] + character['Geld'][2] * 10 + character['Geld'][1] * 100 + \
                        character['Geld'][0] * 1000
            number = number * (10 ** (3 - money_dict[money_typ]))
            converted -= number

            for money_typ in range(4):
                character['Geld'][money_typ] = int(converted / (10 ** (3 - money_typ)))
                converted -= int(converted / (10 ** (3 - money_typ))) * (10 ** (3 - money_typ))
            embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
            embedVar.add_field(name="Geld",
                               value=f"D {str(character['Geld'][0])} | S {str(character['Geld'][1])} | H {str(character['Geld'][2])} | K {str(character['Geld'][3])}",
                               inline=False)
            # embedVar.set_footer(text = f"Letzte Änderung: {sign}{saved_number} {money_dict_string[money_typ]}")
            db[dbname][name_to_find].update(character)
            with open('jsoned_characters.json', 'w') as f:
                json.dump(db, f)
            return embedVar

    elif sign == '+':
        character['Geld'][money_dict[money_typ]] += number
        db[dbname][name_to_find] = character
        embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
        embedVar.add_field(name="Geld",
                           value=f"D {str(character['Geld'][0])} | S {str(character['Geld'][1])} | H {str(character['Geld'][2])} | K {str(character['Geld'][3])}",
                           inline=False)
        embedVar.set_footer(text=f"Letzte Änderung: {sign}{number} {money_dict_string[money_typ]}")
        db[dbname][name_to_find].update(character)
        with open('jsoned_characters.json', 'w') as f:
            json.dump(db, f)
        return embedVar


def SP_reg_or_dmg(message, sign, number, zahl=0):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    serverid = str(message.guild)
    author = str(message.author)
    dbname = serverid + author
    name_to_find = str(get_nickname(message))
    if name_to_find == 'Meister':
        if db['Meister'].get(str(zahl)):
            character = db['Meister'].get(str(zahl))
            name_to_find = str(zahl)
        else:
            embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
            return embedVar
    elif not db[dbname].get(name_to_find):
        embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
        return embedVar
    else:
        character = db[dbname].get(name_to_find)

    if number == '':
        number = 1
    else:
        number = int(number)

    if sign == '-':
        if character['actualSchicksalspunkt'] >= number:
            character['actualSchicksalspunkt'] -= number
            embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
            embedVar.set_thumbnail(url=str(character['Picture']))
            embedVar.set_image(
                url="https://cdn.discordapp.com/attachments/823616400274096148/935244872061968424/jeton.png")
            embedVar.add_field(name="Schicksalspunkte", value=(
                        str(character['actualSchicksalspunkt']) + '/' + str(character['Schicksalspunkt'])),
                               inline=True)
            db[dbname][name_to_find].update(character)
            with open('jsoned_characters.json', 'w') as f:
                json.dump(db, f)
                return embedVar
        else:
            embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
            embedVar.set_thumbnail(url=str(character['Picture']))
            embedVar.add_field(name="Zu wenig Schicksalspunkte", value=(
                        'Du besitzt ' + str(character['actualSchicksalspunkt']) + '/' + str(
                    character['Schicksalspunkt'])), inline=True)
            db[dbname][name_to_find].update(character)
            with open('jsoned_characters.json', 'w') as f:
                json.dump(db, f)
            return embedVar
    elif sign == '+':
        if (character['actualSchicksalspunkt'] + number) <= character['Schicksalspunkt']:
            character['actualSchicksalspunkt'] += number
            embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
            embedVar.set_thumbnail(url=str(character['Picture']))
            embedVar.add_field(name="Schicksalspunkte", value=(
                        str(character['actualSchicksalspunkt']) + '/' + str(character['Schicksalspunkt'])),
                               inline=True)
            db[dbname][name_to_find].update(character)
            with open('jsoned_characters.json', 'w') as f:
                json.dump(db, f)
            return embedVar
        else:
            character['actualSchicksalspunkt'] = character['Schicksalspunkt']
            embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
            embedVar.set_thumbnail(url=str(character['Picture']))
            embedVar.add_field(name="Schicksalspunkte", value=(
                        str(character['actualSchicksalspunkt']) + '/' + str(character['Schicksalspunkt'])),
                               inline=True)
            db[dbname][name_to_find].update(character)
            with open('jsoned_characters.json', 'w') as f:
                json.dump(db, f)
            return embedVar


def zustaende_reg_or_dmg(message, sign, number, zustand, zahl):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    serverid = str(message.guild)
    author = str(message.author)
    dbname = serverid + author
    name_to_find = str(get_nickname(message))
    if name_to_find == 'Meister':
        if db['Meister'].get(str(zahl)):
            character = db['Meister'].get(str(zahl))
            name_to_find = str(zahl)
        else:
            embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
            return embedVar

    elif not db[dbname].get(name_to_find):
        embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
        return embedVar
    else:
        character = db[dbname].get(name_to_find)

    if 'furcht'.startswith(zustand.lower()):
        zustand = 'Furcht'
        zustand_minimum = 'Furcht_min'
    elif 'schmerz'.startswith(zustand.lower()):
        zustand = 'Schmerz'
        zustand_minimum = 'Schmerz_min'
    elif 'betaeubung'.startswith(zustand.lower()) or zustand.lower() == 'betäubung':
        zustand = 'Betaeubung'
        zustand_minimum = 'Betaeubung_min'
    elif 'verwirrung'.startswith(zustand.lower()):
        zustand = 'Verwirrung'
        zustand_minimum = 'Verwirrung_min'
    elif 'paralyse'.startswith(zustand.lower()):
        zustand = 'Paralyse'
        zustand_minimum = 'Paralyse_min'
    elif 'berauscht'.startswith(zustand.lower()):
        zustand = 'Berauscht'
        zustand_minimum = 'Berauscht_min'

    if number == '':
        number = 1
    else:
        number = int(number)
    if sign == '-':
        if (character['Zustaende'][zustand] - number) >= character['Zustaende'][zustand_minimum]:
            character['Zustaende'][zustand] -= number
            embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
            embedVar.set_thumbnail(url=str(character['Picture']))
            embedVar.add_field(name=zustand, value=(character['Zustaende'][zustand]), inline=True)
        else:
            character['Zustaende'][zustand] = character['Zustaende'][zustand_minimum]
            embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
            embedVar.set_thumbnail(url=str(character['Picture']))
            embedVar.add_field(name=zustand, value=(
                        'Du besitzt ' + str(character['Zustaende'][zustand]) + ' vom Zustand ' + zustand),
                               inline=True)
        db[dbname][name_to_find].update(character)
        with open('jsoned_characters.json', 'w') as f:
            json.dump(db, f)
        return embedVar
    elif sign == '+':
        if (character['Zustaende'][zustand] + number) < 4:
            character['Zustaende'][zustand] += number
            embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
            embedVar.set_thumbnail(url=str(character['Picture']))
            embedVar.add_field(name=zustand, value=(str(character['Zustaende'][zustand])), inline=True)
        else:
            if zustand == 'Berauscht':
                character['Zustaende']['Betaeubung'] += 1
                character['Zustaende'][zustand] = character['Zustaende'][zustand] + number - 4
            else:
                character['Zustaende'][zustand] = 4
            embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
            embedVar.set_thumbnail(url=str(character['Picture']))
            embedVar.add_field(name=zustand, value=(str(character['Zustaende'][zustand])), inline=True)
        db[dbname][name_to_find].update(character)
        with open('jsoned_characters.json', 'w') as f:
            json.dump(db, f)
        return embedVar
