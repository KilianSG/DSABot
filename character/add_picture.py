import json

from character.characters_do_stuff.talent import get_nickname


def add_picture_to_character(message, zahl=0):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    serverid = str(message.guild)
    author = str(message.author)
    dbname = serverid + author
    name_to_find = get_nickname(message)
    print(name_to_find)
    if get_nickname(message) == 'Meister':
        character = db['Meister'].get(str(zahl))

    else:
        character = db[dbname].get(name_to_find)
    if character == False:
        return "Konnte nicht gefunden werden"
    else:
        character[0]['Picture'] = message.attachments[0].url
        print('bild ist da')
        return message.attachments[0].url
    with open('jsoned_characters.json', 'w') as f:
        json.dump(db, f)
