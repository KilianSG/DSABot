from character.changing_stats import *
from character.create_character import print_character
from project_buttons.buttons_template import StatusView


def help_with_status(character, name_to_find):
    embeds = print_character(character, name_to_find)
    view = StatusView(name_to_find, embeds)
    return [embeds.embed, view]


def check_if_lep(message):
    if message.content[0] == '-' or message.content[0] == '+':
        if message.content[1:100].isdigit():
            return True
    return False


def plus_minus(sign, message, number_char=0):
    try:
        number = int(''.join(i for i in message.content if i.isdigit()))
    except ValueError as e:
        number = 1
    check_lep = check_if_lep(message)
    list_for_chip = ('chip', 'schip', 'schicksal', 'schicksals_punkte')
    if check_lep:
        return LP_reg_or_dmg(message, sign, number, None, number_char, False, False)
    elif message.content.endswith(list_for_chip):
        return SP_reg_or_dmg(message, sign, number, number_char)
    elif message.content.endswith('asp'):
        return LP_reg_or_dmg(message, sign, number, None, number_char, asp=True, kap=False)
    elif message.content.endswith('kap'):
        return LP_reg_or_dmg(message, sign, number, None, number_char, asp=False, kap=True)
    elif message.content.endswith((' d', ' h', ' s', ' k')):
        return changing_money(message, sign, number, message.content[-1])
    elif message.content.endswith(
            ('furcht', 'berauscht', 'schmerz', 'verwirrung', 'paralyse', 'betaeubung', 'betäubung')):
        return zustaende_reg_or_dmg(message, sign, number, message.content.split()[-1], number_char)
    return None


def cancel_tasks(tasks):
    for task in tasks:
        if task.cancelled():
            continue
        else:
            task.cancel()
