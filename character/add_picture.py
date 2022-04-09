import json

from character.characters_do_stuff.talent import get_nickname


def add_picture_to_character(message):
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    serverid = str(message.guild)
    author = str(message.author)
    dbname = serverid + author
    name_to_find = get_nickname(message)
    print(name_to_find)
    if get_nickname(message) == 'Meister':
        character = db['Meister'].get(message.content[-1])
    else:
        character = db[dbname].get(name_to_find)
    if not character:
        return "Konnte nicht gefunden werden"
    else:
        character['Picture'] = message.attachments[0].url
        print('bild ist da')
        with open('jsoned_characters.json', 'w') as f:
            json.dump(db, f)
        return message.attachments[0].url
