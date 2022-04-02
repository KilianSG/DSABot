import random
import json
import discord
from Databases.lists.list import liste_für_pre_combat, list_für_combat
from character.characters_do_stuff.talent import get_nickname
from project_buttons.buttons_template import pre_combat, wait_button, back_and_start, back_and_start_and_wait, turn_end


def embed_end_of_turn():
    embedVar = discord.Embed(title='Zug Ende', description="Verzögerte Züge nun ausführen....", color=0x3498DB)
    button = turn_end()
    return embedVar, button


def embed_wait_for_later(name, character):
    embedVar = discord.Embed(title=name, description="Wartet auf später...", color=0x3498DB)
    embedVar.set_thumbnail(url=str(character['Picture']))
    button = wait_button()
    return embedVar, button


def embed_in_combat(name, alive, character):
    sonderfertigkeit = ()
    for x in range(len(character['Sonderfertigkeiten'])):
        for y in character['Sonderfertigkeiten'][x]:
            if y[-1].isdigit():
                number = int(y[-1])
                for counting_down in range(1, number+1):
                    add_this = (y[:-1] + str(counting_down),)
                    sonderfertigkeit += add_this
                add_this = (y[:-2],)
                sonderfertigkeit += add_this
            else:
                add_this = (y,)
                sonderfertigkeit += add_this
    list_of_possibilities = []
    list_of_predictions = []

    for x in list_für_combat.keys():
        if x.startswith(sonderfertigkeit) or x == "Improvisierte Techniken":
            if isinstance(list_für_combat, dict):
                for y in list_für_combat[x].keys():
                    if y in sonderfertigkeit or x.startswith('Improvisi'):
                        list_of_predictions.append((x, y))
            list_of_possibilities.append(x)

    if not alive and not name.isdigit():
        print('todo')
    else:
        embedVar = discord.Embed(title=name, description="Dein Zug ist dran!", color=0x3498DB)
        embedVar.set_thumbnail(url=str(character['Picture']))

    components = pre_combat(list_of_possibilities, list_of_predictions, name)
    components.append(back_and_start_and_wait())
    print(list_of_predictions)
    return embedVar, components


def create_embed_out_of_list(name, liste, character):
    get_dat = ''
    for x in liste:
        get_dat += '\n'+x
    embedVar = discord.Embed(title=name, description="", color=0x3498DB)
    embedVar.set_thumbnail(url=str(character['Picture']))
    embedVar.add_field(name='Ausgewählte Sonderfertigkeiten', value=get_dat)
    return embedVar


def embed_pre_combat(name, alive, character):
    sonderfertigkeit = ()
    for x in range(len(character['Sonderfertigkeiten'])):
        for y in character['Sonderfertigkeiten'][x]:
            add_this = (y,)
            sonderfertigkeit += add_this
    list_of_possibilities = []
    list_of_predictions = []
    for x in liste_für_pre_combat.keys():
        if x.startswith(sonderfertigkeit) or x == "Improvisierte Techniken":
            if isinstance(liste_für_pre_combat, dict):
                for y in liste_für_pre_combat[x].keys():
                    if y.startswith(sonderfertigkeit) or x.startswith('Improvisi'):
                        list_of_predictions.append((x, y))
            list_of_possibilities.append(x)
    if not alive and not name.isdigit():
        print('todo')
    else:
        embedVar = discord.Embed(title=name, description="Kampfrundenbeginn", color=0x3498DB)
        embedVar.set_thumbnail(url=str(character['Picture']))
    components = pre_combat(list_of_possibilities, list_of_predictions, name)
    components.append(back_and_start())
    return embedVar, components, list_of_predictions


def embed_turn_table(liste, counter):
    namen = ''
    for x in range(len(liste)):
        if x == counter:
            namen += '__' + liste[x][3] + '__\n'
        else:
            namen += liste[x][3] + '\n'
    embedVar = discord.Embed(title='Kampfrunden', description=namen, color=0x3498DB)

    return embedVar


zone = ""
scenecrit = [
    " KRITISCH "
]
scenecritpfeil = [
    " KRITISCH "
]
sceneschlag = [
    " Angriff "
]
scenepfeil = [
    " Fernkampfangriff "
]

scenekopf = [
    "gegen den **Schädel** ",
    "auf die **Wange** ",
    "auf das **Kinn** ",
    "auf das **linke Ohr** ",
    "gegen das **rechte Ohr** "
]
scenebeinl = [
    "gegen das **linke Schienbein** ",
    "auf die **linke Wade** ",
    "auf den linken **Oberschenkel** ",
    "von rechts gegen das **linke Schienbein** ",
    "von links gegen das **linke Schienbein** ",
    "auf den **linken Fuß** "
]
scenebeinr = [
    "gegen das **rechte Schienbein** ",
    "auf die **rechte Wade** ",
    "auf den **rechten Oberschenkel** ",
    "auf den **rechten Fuß** "
]
scenearml = [
    "auf die **Schildhand** ",
    "gegen den **linken Oberarm** ",
    "gegen den **linken Unterarm** ",
    "gegen den **linken Ellenbogen** ",
    "gegen die **linke Schulter**"
]
scenearmr = [
    "auf die **Waffenhand** ",
    "gegen den **rechten Oberarm** ",
    "gegen den **rechten Unterarm** ",
    "gegen den **rechten Ellenbogen** "
]
scenetorso = [
    "gegen den oberen **Torso** ",
    "auf den **Oberkörper** ",
    "gegen den **Bauch** ",
    "links gegen die **Rippen** ",
    "auf die Höhe der **Niere** ",
    "auf die Höhe des **Brustbeins** ",
    "auf die Seite des **Brustbeins** "
]
scenepatzer = [
    " PATZER\nHoppla, da warst du wohl mit zu viel Schwung unterwegs"
]
scenepatzerpfeil = [
    " PATZER\nSo etwas passiert nur Dir, oder?"
]


def attack(string, message):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    serverid = str(message.guild)
    author = str(message.author)
    dbname = serverid + author
    characters = db[dbname]
    name_to_find = str(get_nickname(message))

    number = random.randint(1, 20)
    string = ''
    crittext = ''
    crit = 0
    patzer = 0
    if number == 1:
        crit = 1
        string += random.choice(scenecrit)
    elif number == 20:
        patzer = 1
        string += random.choice(scenepatzer)
    else:
        string += random.choice(sceneschlag)

    if patzer == 0:
        if number < 3:
            string += "gegen den Kopf"  # random.choice(scenekopf)
            db[zone] = "Kopf"
        elif number < 13:
            string += 'gegen den Torso'  # random.choice(scenetorso)
            db[zone] = "Torso"
        elif number < 15:
            string += 'gegen den linken Arm'  # random.choice(scenearml)
            db[zone] = "LinkerArm"
        elif number < 17:
            string += 'gegen den rechten Arm'  # random.choice(scenearmr)
            db[zone] = "RechterArm"
        elif number < 19:
            string += 'gegen das linke Bein'  # random.choice(scenebeinl)
            db[zone] = "LinkesBein"
        elif number < 21:
            string += 'gegen das rechte Bein'  # random.choice(scenebeinr)
            db[zone] = "RechtesBein"
    string += "_"

    is_crit = False
    if crit == 1 or patzer == 1:
        is_crit = True
        # crittext = '\n\n_Der Bestätigungswurf ist ..._'

    Zustaende = ""
    if characters[name_to_find]['Zustaende']['Schmerz'] > 0:
        Zustaende += "Schmerz\t= "
        Zustaende += (str(characters[name_to_find]['Zustaende']['Schmerz']))
    if characters[name_to_find]['Zustaende']['Betaeubung'] > 0:
        Zustaende += ("\Betäubung\t= ")
        Zustaende += (str(characters[name_to_find]['Zustaende']['Betaeubung']))
    if characters[name_to_find]['Zustaende']['Furcht'] > 0:
        Zustaende += ("\nFurcht\t= ")
        Zustaende += (str(characters[name_to_find]['Zustaende']['Furcht']))
    if characters[name_to_find]['Zustaende']['Verwirrung'] > 0:
        Zustaende += ("\nVerwirrung\t= ")
        Zustaende += (str(characters[name_to_find]['Zustaende']['Verwirrung']))
    if characters[name_to_find]['Zustaende']['Paralyse'] > 0:
        Zustaende += ("\nParalyse\t= ")
        Zustaende += (str(characters[name_to_find]['Zustaende']['Paralyse']))
    embedVar = discord.Embed(title=name_to_find, description="", color=0x3498DB)
    embedVar.set_thumbnail(url=str(characters[name_to_find]['Picture']))
    embedVar.add_field(name="_Würfelt eine " + str(number) + "_", value=('_' + string), inline=True)
    if Zustaende != "":
        embedVar.add_field(name="_Erschwernisse_", value=(Zustaende), inline=True)
    if crittext != '':
        embedVar.add_field(name="Der Bestätigungswurf ist ", value='_||' + str(random.randint(1, 20)) + "||_",
                           inline=False)
    return embedVar, is_crit, str(random.randint(1, 20))
