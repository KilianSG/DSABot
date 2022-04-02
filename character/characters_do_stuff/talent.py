import random

import discord
import discord.ext
import yaml
import json

from Databases.lists.list import liste_zum_suchen

# SF bei FK
# Talent1|Talent2|Talent3|fw bonus|QS bonus| fp bonus bei erfolg|erleichterung


with open("Databases/Fertigkeiten.yaml", 'r', encoding='utf8') as stream:
    fk = yaml.safe_load(stream)


def get_nickname(message):
    return_this = message.author.display_name.split('"')
    if len(return_this) > 1:
        return return_this[1]
    return message.author.display_name


def what_talent(message, zahl=0):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    if message.content == 't':
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

        block_roll = [0] * 3
        for i in range(3):
            block_roll[i] = random.randint(1, 20)
        embedVar = discord.Embed(title=get_nickname(message), description="", color=0x3498DB)
        embedVar.set_thumbnail(url=str(character[0]['Picture']))
        embedVar.add_field(name="Gewürfelt",
                           value='\t' + str(block_roll[0]) + ' | ' + str(block_roll[1]) + ' | ' + str(block_roll[2]),
                           inline=False)
        return embedVar

    cutted = ""
    if message.content.startswith("t "):
        cutted = message.content[2:]

    else:
        cutted = message.content[7:]

    erschwernis = 0
    i = -1
    while cutted[i].isnumeric():
        i = i - 1

    if i != -1:
        erschwernis = int(cutted[i:])

        cutted = cutted[:i]

    splitted_message = cutted.split();
    lenght = len(splitted_message)

    counter = 0
    for word in liste_zum_suchen:
        is_the_word_to_find = ''
        is_the_number_to_find = ''

        check_this = word.split()
        for x in check_this:
            for y in splitted_message:
                c = x.lower()
                if c.startswith(y.lower()):
                    counter += 1
                if counter == lenght:
                    is_the_word_to_find = word
                    is_the_number_to_find = check_this[len(check_this) - 1]
                    break;
        counter = 0
        if is_the_word_to_find != '':
            print(is_the_word_to_find)
            print('end of finding')
            return do_the_probe(message, erschwernis, is_the_word_to_find, is_the_number_to_find, zahl)

    embedVar = discord.Embed(title="Wurde nicht gefunden", description="", color=0x3498DB)
    return embedVar


def do_the_probe(message, erschwernis, talent_name, number_of_talent, zahl):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    serverid = str(message.guild)
    author = str(message.author)
    dbname = serverid + author
    name_to_find = str(get_nickname(message))

    if name_to_find == 'Meister':
        if db['Meister'].get(zahl):
            characters = db['Meister'].get(zahl)
            name_to_find = str(zahl)
        else:
            embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
            return embedVar
    elif not db[dbname].get(name_to_find):
        embedVar = discord.Embed(title=name_to_find, description="konnte nicht gefunden werden", color=0x3498DB)
        return embedVar
    else:
        characters = db[dbname].get(name_to_find)
    the_talent_is_here = talent_name

    first_term = fk[int(number_of_talent[4:]) - 1]['name'] + ' '

    talent_name = talent_name.replace(first_term, '')

    number_of_talent_with_space = ' ' + number_of_talent
    print(number_of_talent)
    talent_name = talent_name.replace(number_of_talent_with_space, '')
    talent_name = talent_name.replace(number_of_talent, '')
    FW = characters['Talente'][int(number_of_talent[4:])]
    FP_Bonus = 0
    QS = 0
    Erleichterung = 0
    Begabung = 0

    block_eigenschaften = [0] * 3

    for i in range(3):
        if list(fk[int(number_of_talent[4:]) - 1]['talente'][i].values())[0] == 'KL':
            block_eigenschaften[i] = int(characters['Klugheit']) + int(characters['modKL'])
        elif list(fk[int(number_of_talent[4:]) - 1]['talente'][i].values())[0] == 'IN':
            block_eigenschaften[i] = int(characters['Intuition']) + int(characters['modIN'])
        elif list(fk[int(number_of_talent[4:]) - 1]['talente'][i].values())[0] == 'KO':
            block_eigenschaften[i] = int(characters['Konstitution']) + int(characters['modKO'])
        elif list(fk[int(number_of_talent[4:]) - 1]['talente'][i].values())[0] == 'GE':
            block_eigenschaften[i] = int(characters['Gewandtheit']) + int(characters['modGE'])
        elif list(fk[int(number_of_talent[4:]) - 1]['talente'][i].values())[0] == 'FF':
            block_eigenschaften[i] = int(characters['Fingerfertigkeit']) + int(characters['modFF'])
        elif list(fk[int(number_of_talent[4:]) - 1]['talente'][i].values())[0] == 'MU':
            block_eigenschaften[i] = int(characters['Mut']) + int(characters['modMU'])
        elif list(fk[int(number_of_talent[4:]) - 1]['talente'][i].values())[0] == 'CH':
            block_eigenschaften[i] = int(characters['Charisma']) + int(characters['modCH'])
        elif list(fk[int(number_of_talent[4:]) - 1]['talente'][i].values())[0] == 'KK':
            block_eigenschaften[i] = int(characters['Körperkraft']) + int(characters['modKK'])

    copy_eigenschaften = block_eigenschaften

    has_chip = 0
    has_begabung = 0
    print(the_talent_is_here)
    for y in characters['Vorteile']:
        if y[0].startswith('Begabung') and y[0][9:] in the_talent_is_here:
            has_begabung = 1
    for y in characters['Nachteile']:
        if y[0].startswith('Unfähigkeit') and y[0][12:] in the_talent_is_here:
            has_begabung = -1
    Berücksichtigt = ''
    # Talent1|Talent2|Talent3|fw bonus|QS bonus| fp bonus bei erfolg|erleichterung|Begabung
    if talent_name == '':
        print('dont search further')
        # TODO:
        if fk[int(number_of_talent[4:]) - 1].get('SF'):
            for x in fk[int(number_of_talent[4:]) - 1]['SF']:
                for y in (characters['Sonderfertigkeiten']):
                    if x['id'] == y[0]:
                        Berücksichtigt += y[0] + ' '
                        block_eigenschaften[0] = int(block_eigenschaften[0]) + x['effekt'][0]
                        block_eigenschaften[1] = int(block_eigenschaften[0]) + x['effekt'][1]
                        block_eigenschaften[2] = int(block_eigenschaften[0]) + x['effekt'][2]
                        FW += x['effekt'][3]
                        FP_Bonus += x['effekt'][4]
                        QS += x['effekt'][5]
                        Erleichterung += x['effekt'][6]
                        Begabung += x['effekt'][7]
                        break
                for y in characters['Vorteile']:
                    if x['id'] == y[0]:
                        Berücksichtigt += y[0] + ' '
                        block_eigenschaften[0] = int(block_eigenschaften[0]) + x['effekt'][0]
                        block_eigenschaften[1] = int(block_eigenschaften[0]) + x['effekt'][1]
                        block_eigenschaften[2] = int(block_eigenschaften[0]) + x['effekt'][2]
                        FW += x['effekt'][3]
                        FP_Bonus += x['effekt'][4]
                        QS += x['effekt'][5]
                        Erleichterung += x['effekt'][6]
                        Begabung += x['effekt'][7]
                        break
                for y in characters['Nachteile']:
                    if x['id'] == y[0]:
                        Berücksichtigt += y[0] + ' '
                        block_eigenschaften[0] = int(block_eigenschaften[0]) + x['effekt'][0]
                        block_eigenschaften[1] = int(block_eigenschaften[0]) + x['effekt'][1]
                        block_eigenschaften[2] = int(block_eigenschaften[0]) + x['effekt'][2]
                        FW += x['effekt'][3]
                        FP_Bonus += x['effekt'][4]
                        QS += x['effekt'][5]
                        Erleichterung += x['effekt'][6]
                        Begabung += x['effekt'][7]
                        break
    else:
        for y in characters['Sonderfertigkeiten']:
            if y[0].startswith('Fertigkeitsspezialisierung ') and talent_name != '' and (talent_name in y[0]):
                Berücksichtigt += 'Fertigkeitsspezialisierung'
                FW += 2
                break
        if fk[int(number_of_talent[4:]) - 1].get('SF'):
            for x in fk[int(number_of_talent[4:]) - 1]['SF']:
                for y in characters['Sonderfertigkeiten']:
                    if x['id'] == y[0]:
                        Berücksichtigt += y[0] + ' '
                        block_eigenschaften[0] = int(block_eigenschaften[0]) + x['effekt'][0]
                        block_eigenschaften[1] = int(block_eigenschaften[0]) + x['effekt'][1]
                        block_eigenschaften[2] = int(block_eigenschaften[0]) + x['effekt'][2]
                        FW += x['effekt'][3]
                        FP_Bonus += x['effekt'][4]
                        QS += x['effekt'][5]
                        Erleichterung += x['effekt'][6]
                        Begabung += x['effekt'][7]
                        break
                for y in characters['Vorteile']:
                    if x['id'] == y[0]:
                        Berücksichtigt += y[0] + ' '
                        block_eigenschaften[0] = int(block_eigenschaften[0]) + x['effekt'][0]
                        block_eigenschaften[1] = int(block_eigenschaften[0]) + x['effekt'][1]
                        block_eigenschaften[2] = int(block_eigenschaften[0]) + x['effekt'][2]
                        FW += x['effekt'][3]
                        FP_Bonus += x['effekt'][4]
                        QS += x['effekt'][5]
                        Erleichterung += x['effekt'][6]
                        Begabung += x['effekt'][7]
                        break
                for y in characters['Nachteile']:
                    if x['id'] == y[0]:
                        Berücksichtigt += y[0] + ' '
                        block_eigenschaften[0] = int(block_eigenschaften[0]) + x['effekt'][0]
                        block_eigenschaften[1] = int(block_eigenschaften[0]) + x['effekt'][1]
                        block_eigenschaften[2] = int(block_eigenschaften[0]) + x['effekt'][2]
                        FW += x['effekt'][3]
                        FP_Bonus += x['effekt'][4]
                        QS += x['effekt'][5]
                        Erleichterung += x['effekt'][6]
                        Begabung += x['effekt'][7]
                        break
        id = None
        for z in range(len(fk[int(number_of_talent[4:]) - 1]['applications'])):
            if talent_name == '':
                break
            if fk[int(number_of_talent[4:]) - 1]['applications'][z]['name'] == talent_name:
                id = z
                break
        if id != None and fk[int(number_of_talent[4:]) - 1]['applications'][id].get('SF'):
            for x in fk[int(number_of_talent[4:]) - 1]['applications'][id]['SF']:
                for y in characters['Sonderfertigkeiten']:
                    if x['id'] == y[0]:
                        Berücksichtigt += y[0] + ' '
                        block_eigenschaften[0] = int(block_eigenschaften[0]) + x['effekt'][0]
                        block_eigenschaften[1] = int(block_eigenschaften[0]) + x['effekt'][1]
                        block_eigenschaften[2] = int(block_eigenschaften[0]) + x['effekt'][2]
                        FW += x['effekt'][3]
                        FP_Bonus += x['effekt'][4]
                        QS += x['effekt'][5]
                        Erleichterung += x['effekt'][6]
                        Begabung += x['effekt'][7]
                        break
                for y in characters['Vorteile']:
                    if x['id'] == y[0]:
                        Berücksichtigt += y[0] + ' '
                        block_eigenschaften[0] = int(block_eigenschaften[0]) + x['effekt'][0]
                        block_eigenschaften[1] = int(block_eigenschaften[0]) + x['effekt'][1]
                        block_eigenschaften[2] = int(block_eigenschaften[0]) + x['effekt'][2]
                        FW += x['effekt'][3]
                        FP_Bonus += x['effekt'][4]
                        QS += x['effekt'][5]
                        Erleichterung += x['effekt'][6]
                        Begabung += x['effekt'][7]
                        break
                for y in characters['Nachteile']:
                    if x['id'] == y[0]:
                        Berücksichtigt += y[0] + ' '
                        block_eigenschaften[0] = int(block_eigenschaften[0]) + x['effekt'][0]
                        block_eigenschaften[1] = int(block_eigenschaften[0]) + x['effekt'][1]
                        block_eigenschaften[2] = int(block_eigenschaften[0]) + x['effekt'][2]
                        FW += x['effekt'][3]
                        FP_Bonus += x['effekt'][4]
                        QS += x['effekt'][5]
                        Erleichterung += x['effekt'][6]
                        Begabung += x['effekt'][7]
                        break
    the_talent_is_here = the_talent_is_here.replace(number_of_talent, '')
    # Talent1|Talent2|Talent3|fw bonus|QS bonus| fp bonus bei erfolg|erleichterung|Begabung
    FW_copy = FW

    block_roll = [0] * 3
    for i in range(3):
        block_roll[i] = random.randint(1, 20)

    crit = 0
    patzer = 0
    for i in range(3):
        if block_roll[i] == 1:
            crit = crit + 1
        if block_roll[i] == 20:
            patzer = patzer + 1

    for i in range(3):
        if block_roll[i] - erschwernis > block_eigenschaften[i] + Erleichterung:
            FW = FW - (block_roll[i] - erschwernis) + (block_eigenschaften[i] + Erleichterung)

    QS_return = 0

    if FW >= -1:
        QS_return = 1
        QS_return = int(FW / 3 + 1 + QS - 0.001)

    if erschwernis > 0:
        embedVar = discord.Embed(title=name_to_find, description="Würfelt auf " + the_talent_is_here + ' (' + str(
            FW_copy) + ') mit einer Erleichterung von ' + str(erschwernis), color=0x3498DB)
    elif erschwernis < 0:
        embedVar = discord.Embed(title=name_to_find, description="Würfelt auf " + the_talent_is_here + ' (' + str(
            FW_copy) + ') mit einer Erschwernis von ' + str(erschwernis), color=0x3498DB)
    else:
        embedVar = discord.Embed(title=name_to_find,
                                 description="Würfelt auf " + the_talent_is_here + ' (' + str(FW_copy) + ')',
                                 color=0x3498DB)
    embedVar.set_thumbnail(url=str(characters['Picture']))
    if erschwernis != 0 or Erleichterung != 0:
        embedVar.add_field(name="Eigenschaften", value=(
                    list(fk[int(number_of_talent[4:]) - 1]['talente'][0].values())[0] + '  |  ' +
                    list(fk[int(number_of_talent[4:]) - 1]['talente'][1].values())[0] + '  |  ' +
                    list(fk[int(number_of_talent[4:]) - 1]['talente'][2].values())[0] + '\n\t' + str(
                copy_eigenschaften[0]) + '  |  ' + str(copy_eigenschaften[1]) + '  |  ' + str(
                copy_eigenschaften[2]) + '\n\t(' + str(
                block_eigenschaften[0] + erschwernis + Erleichterung) + '  |  ' + str(
                block_eigenschaften[1] + erschwernis + Erleichterung) + '  |  ' + str(
                block_eigenschaften[2] + erschwernis + Erleichterung) + ')'), inline=False)
    else:
        embedVar.add_field(name="Eigenschaften", value=(
                    list(fk[int(number_of_talent[4:]) - 1]['talente'][0].values())[0] + '  |  ' +
                    list(fk[int(number_of_talent[4:]) - 1]['talente'][1].values())[0] + '  |  ' +
                    list(fk[int(number_of_talent[4:]) - 1]['talente'][2].values())[0] + '\n' + str(
                copy_eigenschaften[0]) + '  |  ' + str(copy_eigenschaften[1]) + '  |  ' + str(copy_eigenschaften[2])),
                           inline=False)
    embedVar.add_field(name="Gewürfelt",
                       value='\t' + str(block_roll[0]) + '  |  ' + str(block_roll[1]) + ' | ' + str(block_roll[2]),
                       inline=False)
    if patzer > 1:
        embedVar.add_field(name="Patzer", value='du hast einen Patzer gewürfelt!', inline=False)
    elif crit > 1:
        embedVar.add_field(name="Kritisch", value='du hast kritisch gewürfelt!', inline=False)
    elif FW >= 0:
        if QS_return < 1:
            QS_return = 1
        embedVar.add_field(name="Ergebnis", value=f'QS {QS_return} | FP :{FW}/{FW_copy}', inline=False)
    else:
        embedVar.add_field(name="Ergebnis", value='Probe nicht bestanden.', inline=False)
    if Berücksichtigt != '':
        embedVar.add_field(name="Berücksichtigt wurden: ", value=Berücksichtigt, inline=False)
    if characters['actualSchicksalspunkt'] >= 1:
        has_chip = 1
    original_block_eigenschaften = block_eigenschaften
    block_eigenschaften[0] = block_eigenschaften[0] - erschwernis + Erleichterung
    block_eigenschaften[1] = block_eigenschaften[1] - erschwernis + Erleichterung
    block_eigenschaften[2] = block_eigenschaften[2] - erschwernis + Erleichterung
    return embedVar, has_chip, has_begabung, original_block_eigenschaften, block_eigenschaften, FW_copy, QS, block_roll, patzer


def probe_begabung(embedVar, has_chip, has_begabung, original_block_eigenschaften, block_eigenschaften, FW_copy, QS,
                   block_roll, reroll):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    old_value = 0
    print(has_begabung)
    if has_begabung == 0:
        return
    else:
        old_value = has_begabung
        has_begabung = 0
    FW = FW_copy

    if old_value == -1:
        reroll_this = 20
        reroll = 0
        for x in range(3):
            if block_roll[x] <= reroll_this:
                reroll_this = block_roll[x]
                reroll = x

    old_roll = block_roll[int(reroll)]
    new_roll = block_roll[int(reroll)] = random.randint(1, 20)
    if (old_value == 1 and block_eigenschaften[int(reroll)] > old_roll):
        block_eigenschaften[int(reroll)] = old_roll

    for i in range(3):
        if block_roll[i] > block_eigenschaften[i]:
            FW = FW - block_roll[i] + block_eigenschaften[i]

    QS_return = int(FW / 3 + 1 + QS - 0.001)
    Was_fuer_ne_probe = {-1: 'Unfähigkeit', 1: 'Begabung'}
    embedVar.add_field(name=f'{Was_fuer_ne_probe[old_value]} für den {reroll + 1}ten Würfel',
                       value=f'{old_roll}-->{new_roll}.', inline=False)
    if (old_roll > new_roll * old_value):
        embedVar.add_field(name=f'Ergebnis mit {Was_fuer_ne_probe[old_value]}',
                           value=f'QS {QS_return} | FP :{FW}/{FW_copy}', inline=False)
    else:
        embedVar.add_field(name=f'Ergebnis mit {Was_fuer_ne_probe[old_value]}', value='Keine Änderung des Ergebnis',
                           inline=False)
    return embedVar, has_chip, has_begabung, block_roll


def probe_schicksal(embedVar, has_chip, has_begabung, original_block_eigenschaften, block_eigenschaften, FW_copy, QS,
                    block_roll, reroll):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    has_chip = 0
    FW = FW_copy
    old_list = [0] * 3

    for x in range(3):
        old_list[x] = block_roll[x]
        if reroll[x] == 1:
            block_roll[x] = random.randint(1, 20)

    for i in range(3):
        if block_roll[i] > block_eigenschaften[i]:
            FW = FW - block_roll[i] + block_eigenschaften[i]

    QS_return = int(FW / 3 + 1 + QS - 0.001)

    embedVar.add_field(name=f'Schicksalswürfe',
                       value=f'{old_list[0]}|{old_list[1]}|{old_list[2]}-->{block_roll[0]}|{block_roll[1]}|{block_roll[2]}',
                       inline=False)
    embedVar.add_field(name='Ergebnis mit Schicksalspunkt', value=f'QS {QS_return} | FP :{FW}/{FW_copy}', inline=False)

    return embedVar, has_chip, has_begabung, block_roll
