import random


def get_nickname(message):
    return_this = message.author.display_name.split('"')
    return return_this[1]


def rolling(message):
    counter = 1
    if message.content.startswith('w') and message.content[1:].isnumeric():
        numberarray = roll(message, 1, int(message.content[1:]))
        return numberarray
    while message.content[0:counter].isnumeric():
        counter += 1
    if message.content[counter - 1] == 'w':
        eins = message.content[:counter - 1]
        if message.content[counter:].isnumeric():
            numberarray = roll(message, eins, int(message.content[counter:]))
            return numberarray
        else:
            return False
    else:
        return False


def roll(message, eins, zwei):
    start_with = int(eins)
    string = get_nickname(message) + ' würfelt '
    while (start_with > 0):
        number = random.randint(1, int(zwei))
        string += '**['
        string += str(number)
        string += ']**'
        if start_with > 1:
            string += ', '
        start_with -= 1

    return string
