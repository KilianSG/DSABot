import asyncio
import json
import os
import random
import threading
import time
from dotenv import load_dotenv
from os import getenv
import discord
import yaml
from discord import ActionRow, Button, ButtonStyle
from discord.ext import commands
from asyncio_helper.help_with_await import cancel_tasks
from character.add_picture import add_picture_to_character
from character.changing_stats import SP_reg_or_dmg, LP_reg_or_dmg, zustaende_reg_or_dmg, changing_money
from character.characters_do_stuff.combat import attack, embed_turn_table, embed_pre_combat, embed_in_combat, \
    embed_wait_for_later, embed_end_of_turn, create_embed_out_of_list
from character.characters_do_stuff.liturgie import prep_liturgy, get_basic_liturgy_embed, cast_liturgy
from character.characters_do_stuff.talent import what_talent, get_nickname, probe_begabung, probe_schicksal
from character.characters_do_stuff.w20 import rolling
from character.create_character import charactere, create_char, print_character
from project_buttons.button_handle import handle_modification_liturgy, handle_status, handle_in_combat
from project_buttons.buttons_template import status_template, schicksals_row_begabungs_row_template, next_turn_button, \
    back_and_start_and_wait, pre_combat as buttons_pre_combat

e = threading.Event()
q = []
stop_or_wait = []
is_end_of_turn = 0
anyone_awaited = 0
load_dotenv()


def only_numerics(seq):
    seq_type = type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))


def liste_zum_suchen():
    with open("zauber_liste_namen.yaml", 'r', encoding='utf8') as stream:
        fk = yaml.safe_load(stream)
    for x in fk:
        print('"' + x['name'] + ' ' + x['id'] + '",')


client = commands.Bot(command_prefix='!')


# @client.command(name='', description='Invoke new Character')
async def loading_character(ctx: commands.Context):
    print('got invoked')
    msg = await ctx.channel.send(content='Der Charakter wird geladen...')
    for attachment in ctx.attachments:
        if any(attachment.filename.lower().endswith(json) for json in json_types):
            await attachment.save(attachment.filename)
            with open(attachment.filename, 'r', encoding='utf8') as openfile:
                newchar = json.load(openfile)
            os.remove(attachment.filename)
            char = charactere(**newchar)
            printable_character = create_char(char, ctx, "")
            components = status_template(get_nickname(ctx), printable_character.zauber, printable_character.liturgie)
            msg = await ctx.channel.send(embed=printable_character.embed, components=components)
    imbed_to_send = printable_character.embed
    t_end = time.time() + 60 * 5
    while time.time() < t_end:
        def _check(i: discord.Interaction, b):
            return i.message == msg and i.member == ctx.author

        interaction, button = await client.wait_for('button_click', check=_check)
        button_id = button.custom_id
        imbed_to_send = handle_status(button_id, printable_character)
        await interaction.defer()
        await interaction.edit(embed=imbed_to_send)
    components = status_template(get_nickname(ctx), printable_character.zauber, printable_character.liturgie)
    await interaction.edit(embed=imbed_to_send, components=components)
    return


# @client.command(name='', description='Status of character')
async def status_character(ctx: commands.Context):
    print('got status')
    with open('jsoned_characters.json', encoding='utf8') as f:
        db = json.load(f)
    serverid = str(ctx.guild)
    author = str(ctx.author)
    dbname = serverid + author
    characters = db[dbname]
    name_to_find = str(get_nickname(ctx))
    if name_to_find == 'Meister':
        characters = db[name_to_find]
        if ctx.content[-1].isnumeric():
            name_to_find = str(ctx.content[-1:])
    printable_character = print_character(characters, name_to_find)
    components = status_template(get_nickname(ctx), printable_character.zauber, printable_character.liturgie)
    msg = await ctx.channel.send(embed=printable_character.embed, components=components)
    imbed_to_send = printable_character.embed
    t_end = time.time() + 60 * 5
    while time.time() < t_end:
        def _check(i: discord.Interaction, b):
            return i.message == msg and i.member == ctx.author

        interaction, button = await client.wait_for('button_click', check=_check)
        button_id = button.custom_id
        imbed_to_send = handle_status(button_id, printable_character)
        await interaction.defer()
        await interaction.edit(embed=imbed_to_send)
    components = status_template(get_nickname(ctx), printable_character.zauber, printable_character.liturgie)
    await interaction.edit(embed=imbed_to_send, components=components)
    return


@client.command(name='', description='liturgie Cast')
async def do_liturgie_cast(ctx, liturgy_to_cast, liturgy_name, roll_on_this, character_name, character,
                           list_of_modifications=None, tier=None, target=None):
    print('something')
    # cast_liturgy(liturgy_to_cast, liturgy_name, roll_on_this, character_name, character,list_of_modifications = None, tier = None, target = None):
    return_from_cast = cast_liturgy(liturgy_to_cast, liturgy_name, roll_on_this, character_name, character,
                                    list_of_modifications=None, tier=None)
    msg = await ctx.channel.send(embed=return_from_cast[0])
    return

    """t_end = time.time() + 60 * 2
    while time.time() < t_end:
      def _check(i: discord.Interaction, b):
        return i.message == msg and i.member == ctx.author
      interaction, button = await client.wait_for('button_click', check=_check)
      button_id = button.custom_id
      
      await interaction.defer()
      await interaction.edit(embed=embeded[0])
      return"""


# @client.command(name = '', description = 'liturgie')
async def do_button_liturgie(ctx: commands.Context, combat=False):
    print('do Liturgie')
    with open('jsoned_characters.json', encoding='utf8') as f:
        db = json.load(f)
    serverid = str(ctx.guild)
    author = str(ctx.author)
    dbname = serverid + author
    characters = db[dbname]
    name_to_find = str(get_nickname(ctx))
    if name_to_find == 'Meister':
        characters = db[name_to_find]
        if ctx.content[-1].isnumeric():
            name_to_find = str(ctx.content[-1:])
    characters = characters[name_to_find]
    # [return_embed, components, max_modificator, character['Liturgien'][liturgy_to_cast] , liturgy_to_cast, list_of_attributes]
    printable_liturgie = prep_liturgy(ctx, get_nickname(ctx), characters)
    copy_liturgy = dict(printable_liturgie[3])
    list_of_modification = []
    print(printable_liturgie[1])
    msg = await ctx.channel.send(embed=printable_liturgie[0], components=printable_liturgie[1])
    t_end = time.time() + 60 * 2
    counter = 0
    while time.time() < t_end:
        def _check(i: discord.Interaction, b):
            return i.message == msg and i.member == ctx.author

        interaction, button = await client.wait_for('button_click', check=_check)
        button_id = button.custom_id
        if button_id.endswith('cast'):
            if combat == False:
                # cast_liturgy(liturgy_to_cast, liturgy_name, roll_on_this, character_name, character,list_of_modifications = None, tier = None, target = None):
                await do_liturgie_cast(ctx, copy_liturgy, printable_liturgie[4], printable_liturgie[5],
                                       get_nickname(ctx), characters, False)
            await interaction.edit(components=[])
            await interaction.defer()
            return
        return_this = handle_modification_liturgy(button_id, printable_liturgie[2], counter, list_of_modification,
                                                  copy_liturgy, printable_liturgie[5])
        # return [maximum_mods,counter , list_of_modification, copy_liturgy, abilities_table]
        counter = return_this[1]
        printable_liturgie[5] = return_this[2]
        copy_liturgy = return_this[3]
        printable_liturgie[5] = return_this[4]
        embeded = get_basic_liturgy_embed(get_nickname(ctx), characters, copy_liturgy, printable_liturgie[4],
                                          printable_liturgie[5])
        string = 'Maximal ' + str(printable_liturgie[2]) + ':'
        for x in list_of_modification:
            string += ' ' + x + ' '
        if string != '':
            interaction.edit()
            embeded[0].add_field(name='Modifikationen', value=string, inline=False)
        await interaction.defer()
        await interaction.edit(embed=embeded[0])
    else:
        await ctx.channel.send(embed=embeded[0])
    return


# @client.command(name='', description='attack with buttons')
async def do_attack(ctx: commands.Context):
    print('do attack')
    with open('jsoned_characters.json', encoding='utf8') as f:
        db = json.load(f)
    serverid = str(ctx.guild)
    author = str(ctx.author)
    dbname = serverid + author
    characters = db[dbname]
    name_to_find = str(get_nickname(ctx))
    if name_to_find == 'Meister':
        characters = db[name_to_find]
        if ctx.content[-1].isnumeric():
            name_to_find = str(ctx.content[-1:])
    printable_attack = attack('', ctx)
    if printable_attack[1] == True:
        msg = await ctx.channel.send(embed=printable_attack[0],
                                     components=[ActionRow((Button(label='Bestätigungswurf (W20)',
                                                                   custom_id=get_nickname(ctx) + 'attack',
                                                                   style=ButtonStyle.green)))])
        imbed_to_send = printable_attack[0]
        t_end = time.time() + 60 * 5
        while time.time() < t_end:
            def _check(i: discord.Interaction, b):
                return i.message == msg and i.member == ctx.author

            interaction, button = await client.wait_for('button_click', check=_check)
            button_id = button.custom_id
            if button_id.endswith('attack'):
                imbed_to_send.add_field(name="Bestätigungswurf:", value=(str(random.randint(1, 20))), inline=False)
            await interaction.defer()
            await interaction.edit(embed=imbed_to_send)
    else:
        await ctx.channel.send(embed=printable_attack[0])

    return


async def some_callback(args):
    print('new good stuff')
    await asyncio.sleep(10)
    print('finished')


@client.command(name='', description='do turn')
async def do_turn(ctx: commands.Context):
    print('do turn')
    global is_end_of_turn
    e.clear()
    serverid = str(ctx.guild)
    author = str(ctx.author)
    dbname = serverid + author
    t_end = time.time() + 60 * 60 * 12  # 12 Stunden
    counter = 0
    turn = 0
    maxcounter = 1
    list_of_tasks = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    kampfteilnehmer = [[100, 10, 1, 'Rundenstart', True, 0, None]]
    # actual initiative, base initiative,random_number, name of character, alive, channelid, character
    msg = None
    global anyone_awaited
    while time.time() < t_end:
        while True:
            try:
                new_entry = q.pop()
                print('success')
                if not isinstance(new_entry, list):
                    return
                maxcounter += 1
                counter_name = kampfteilnehmer[counter][3]
                kampfteilnehmer.append(new_entry)
                kampfteilnehmer.sort(reverse=True)
                for x in range(maxcounter):
                    if kampfteilnehmer[x][3] == counter_name:
                        counter = x
                        break
            except:
                pass
            await do_turn_start(kampfteilnehmer, ctx)
            while True:
                counter = (counter + 1) % maxcounter
                if msg is not None:
                    await msg.edit(delete_after=0)
                msg = await ctx.channel.send(embed=embed_turn_table(kampfteilnehmer, counter))
                if counter != 0:
                    flag = asyncio.Event()
                    list_of_tasks[counter] = asyncio.create_task(combat_options(kampfteilnehmer[counter], flag))
                    await flag.wait()
                    flag.clear()
                else:
                    if anyone_awaited != 0:
                        await end_of_turn(ctx)
                        anyone_awaited = 0
                    turn += 1
                    # counter = (counter + 1) % maxcounter
                    break
        continue
    print('got returned?')
    return


# @client.command(name='', description='end_of_turn')
async def end_of_turn(ctx):
    embed_and_button_for_end_turn = embed_end_of_turn()
    msg = await ctx.channel.send(embed=embed_and_button_for_end_turn[0], components=embed_and_button_for_end_turn[1])
    t_end = time.time() + 60 * 2
    while time.time() < t_end:
        def _check(i: discord.Interaction, b):
            return i.message == msg

        interaction, button = await client.wait_for('button_click', check=_check)
        if button.custom_id.endswith('end_this'):
            await msg.edit(delete_after=0)
            return
    msg.edit(delete_after=0)
    return


async def combat_wait_for_button(msg, name_of_character, components,check_turn, end_time, flag, combat_start_components, character, new_effect):
    print('wait for buttons')
    while time.time() < end_time and check_turn == is_end_of_turn and not flag.is_set():
        def _check(i: discord.Interaction, b):
            return i.message == msg and (get_nickname(i) == name_of_character or get_nickname(i) == "Meister")
        interaction, button = await client.wait_for('button_click', check=_check)
        print('in Buttons')
        button_id = button.custom_id
        if button_id.endswith('interrupt'):
            if is_end_of_turn != check_turn:
                msg.edit(content=0, embed='', components=[], delete_after=2)
                return
            wait_embed, wait_button = embed_wait_for_later(name_of_character, character)
            await msg.edit(embed=wait_embed, components=wait_button)
            flag.set()
            global anyone_awaited
            anyone_awaited = 1
        elif button_id.endswith('start'):
            msg = await interaction.edit(components=[])
            flag.set()
            return
        elif button_id.endswith('eingreifen'):
            components = combat_start_components
            await msg.edit(embed=combat_embed, components=combat_start_components)
        else:
            components = handle_in_combat(button_id, character, new_effect, components)
            await interaction.edit(components=components)
    return 0


async def combat_wait_for_component(msg, name_of_character, components, check_turn, end_time, flag, combat_start_components, character, new_effects):
    print('wait for buttons')
    while time.time() < end_time and check_turn == is_end_of_turn and not flag.is_set():
        def _check(i: discord.Interaction, b):
            return i.message == msg and (get_nickname(i) == name_of_character or get_nickname(i) == "Meister")
        interaction, component = await client.wait_for('select_option', check=_check)
        print('in components')
        button_id = component.custom_id
        components = handle_in_combat(button_id, character, new_effects, components)
        await interaction.edit(components=components)
    return 0


# @client.command(name='', description='combat options')
async def combat_options(character_liste, flag):
    check_turn = is_end_of_turn
    print("combat_options")
    list_of_needs = []
    combat_embed, combat_start_components = embed_in_combat(character_liste[3], character_liste[4], character_liste[6])
    channel = client.get_channel(character_liste[5])
    msg = await channel.send(embed=combat_embed, components=combat_start_components)
    t_end = time.time() + 60 * 10
    tasks = [asyncio.create_task(combat_wait_for_button(msg, character_liste[3], combat_start_components, check_turn, t_end, flag, combat_start_components, character_liste[6], list_of_needs)), asyncio.create_task(combat_wait_for_component(msg, character_liste[3], combat_start_components, check_turn, t_end, flag, combat_start_components, character_liste[6], list_of_needs))]
    flag.wait()
    cancel_tasks(tasks)
    return


# @client.command(name='', description='pre combat')
async def pre_combat(kampfteilnehmerliste, number):
    print("pre_combat")
    check_turn = is_end_of_turn
    actual_ini = kampfteilnehmerliste[number][0]  # for nothing
    base_ini = kampfteilnehmerliste[number][1]  # for nothing
    rand_number = kampfteilnehmerliste[number][2]  # for nothing
    name = kampfteilnehmerliste[number][3]
    alive = kampfteilnehmerliste[number][4]
    channelid = kampfteilnehmerliste[number][5]
    character = kampfteilnehmerliste[number][6]
    embedVar = embed_pre_combat(name, alive, character)
    components = embedVar[1]
    channel = client.get_channel(channelid)
    msg = await channel.send(embed=embedVar[0], components=embedVar[1])
    new_effects = []
    t_end = time.time() + 60 * 100
    flag = asyncio.Event()
    tasks = [asyncio.create_task(combat_wait_for_button(msg, name, components, check_turn, t_end, flag, components, character, new_effects)), asyncio.create_task(combat_wait_for_component(msg, name, components, check_turn, t_end, flag, components, character, new_effects))]
    flag.wait()
    cancel_tasks(tasks)
    return


# @client.command(name='', description='do start of combat turn')
async def do_turn_start(list_of_combatants: list, ctx):
    print("combat_round_start")
    list_of_tasks = [0] * len(list_of_combatants)
    for x in range(1, len(list_of_combatants)):
        list_of_tasks[x] = asyncio.create_task(pre_combat(list_of_combatants, x))

    t_end = time.time() + 60 * 10  # 10 min

    msg = await ctx.channel.send(content='Eine neue Kampfrunde beginnt...', components=next_turn_button())
    while time.time() < t_end:
        def _check(i: discord.Interaction, b):
            return i.message == msg and i.member == ctx.author

        interaction, button = await client.wait_for('button_click', check=_check)
        if button.custom_id == 'start':
            await interaction.defer()
            await interaction.edit(delete_after=0)
            return
    await list_of_tasks
    return


# @client.command(name='', description='new_inhabitants')
async def new_inhabitants(ctx):
    with open('jsoned_characters.json', encoding='utf8') as f:
        db = json.load(f)
    serverid = str(ctx.guild)
    author = str(ctx.author)
    dbname = serverid + author
    characters = db[dbname]
    name_to_find = str(get_nickname(ctx))
    characters = characters[name_to_find]
    new_combatants = [int(characters['Initiative']) + (random.randint(1, 6)), characters['Initiative'],
                      random.random() % 5 + 1, name_to_find, True, ctx.channel.id, characters]
    q.append(new_combatants)


# @client.command(name='', description='Probe with buttons')
async def do_button_probe(ctx: commands.Context):
    print('do Probe')
    if ctx.content[-1].isnumeric() and get_nickname(ctx) == 'Meister':
        zahl = ctx.content[-1:]
        print(zahl)
        ctx.content = ctx.content[:-1]
    else:
        zahl = 0
    printable_probe = what_talent(ctx, zahl)

    components = []
    components = schicksals_row_begabungs_row_template(get_nickname(ctx), printable_probe[1], printable_probe[2])
    if components != []:
        list_of_reroll = [0] * 3
        if printable_probe[8] == 2:
            await ctx.channel.send(embed=printable_probe[0], components=[])
            return
        msg = await ctx.channel.send(embed=printable_probe[0], components=components)
        imbed_to_send = None
        t_end = time.time() + 60 * 5
        while time.time() < t_end:
            def _check(i: discord.Interaction, b):
                return i.message == msg and i.member == ctx.author

            interaction, button = await client.wait_for('button_click', check=_check)
            button_id = button.custom_id
            if button_id.endswith(('begabung1', 'begabung2', 'begabung3', 'unfähig1')):
                getting_new_embed = probe_begabung(printable_probe[0], printable_probe[1], printable_probe[2],
                                                   printable_probe[3], printable_probe[4], printable_probe[5],
                                                   printable_probe[6], printable_probe[7], int(button_id[-1]) - 1)
                printable_probe = list(printable_probe)
                printable_probe[0] = getting_new_embed[0]
                printable_probe[1] = getting_new_embed[1]
                printable_probe[2] = getting_new_embed[2]
                printable_probe[7] = getting_new_embed[3]
                imbed_to_send = printable_probe[0]
                components = schicksals_row_begabungs_row_template(get_nickname(ctx), printable_probe[1],
                                                                   printable_probe[2])
            elif button_id.endswith(('reroll1', 'reroll2', 'reroll3')):
                if list_of_reroll[int(button_id[-1]) - 1] == 0:
                    list_of_reroll[int(button_id[-1]) - 1] = 1
                else:
                    list_of_reroll[int(button_id[-1]) - 1] = 0
                value = ''
                for x in range(3):
                    if list_of_reroll[x] == 1:
                        value += str(x + 1) + ', '
                if value != '':
                    value = value[:-2]
                    imbed_to_send = discord.Embed(title=get_nickname(ctx), description="", color=0x3498DB)
                    for x in printable_probe[0].fields:
                        imbed_to_send.add_field(name=x.name, value=x.value, inline=x.inline)
                    imbed_to_send.add_field(name='Schicksalspunkte Würfel', value=value, inline=False)
                    value = ''
            elif button_id.endswith('Schicksal'):
                if list_of_reroll != [0, 0, 0]:
                    getting_new_embed = probe_schicksal(printable_probe[0], printable_probe[1], printable_probe[2],
                                                        printable_probe[3], printable_probe[4], printable_probe[5],
                                                        printable_probe[6], printable_probe[7], list_of_reroll)
                    printable_probe = list(printable_probe)
                    printable_probe[0] = getting_new_embed[0]
                    printable_probe[1] = getting_new_embed[1]
                    printable_probe[2] = getting_new_embed[2]
                    printable_probe[7] = getting_new_embed[3]
                    embedVar = SP_reg_or_dmg(ctx, '-', 1, zahl)
                    await ctx.channel.send(embed=embedVar)
                    components = schicksals_row_begabungs_row_template(get_nickname(ctx), printable_probe[1],
                                                                       printable_probe[2])
            await interaction.defer()
            if imbed_to_send != None:
                await interaction.edit(embed=imbed_to_send, components=components)
                imbed_to_send = None
            else:
                await interaction.edit(embed=printable_probe[0], components=components)
    else:
        await ctx.channel.send(embed=printable_probe[0])
    return


json_types = ["json"]
image_types = ["jpg", "jpeg", "png"]


# on login
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # liste_zum_suchen()


# main
@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        await client.process_commands(message)
    message.content = str(message.content.lower())
    for attachment in message.attachments:
        if any(attachment.filename.lower().endswith(json) for json in json_types):
            await loading_character(message)
            return

        if any(attachment.filename.lower().endswith(image) for image in image_types):
            if message.content.lower().startswith('add'):
                zahl = 0
                if get_nickname(message) == 'Meister':
                    if message.content.lower().startswith('add '):
                        zahl = int(message.content[-1])
                string = add_picture_to_character(message, zahl)
                await message.channel.send(string)
            return

    if message.content == "list key":
        with open('jsoned_characters.json', encoding='utf8') as f:
            db = json.load(f)
        keys = db.keys()
        # keys = db['Meister'].keys()
        await message.channel.send(keys)
        return

    if message.content.startswith("delete meister"):
        with open('jsoned_characters.json', encoding='utf8') as f:
            db = json.load(f)
        for x in db['Meister'].keys():
            del db['Meister'][x]
        with open('jsoned_characters.json', encoding='utf8') as f:
            json.dump(db, f)
        print('deleted Meister')
        return

    if message.content == "start combat":
        # start_ini(message)
        await do_turn(message)
        x = threading.Thread(target=do_turn, args=([message.channel.id]), daemon=True)
        x.start()
        return

    if message.content == "ini":
        # print("Hello new Fella")
        # put_ini(message)
        await new_inhabitants(message)
        return
    if message.content == "end combat":
        q.append('ende')

    if message.content.startswith("t ") or message.content.startswith("talent ") or message.content == 't':
        await do_button_probe(message)
        return

    if message.content.startswith('l ') or message.content.startswith("liturgie "):
        await do_button_liturgie(message)
        return

    if message.content.startswith('status'):
        await status_character(message)
        return

    if message.content.startswith('w') or message.content[0:1].isnumeric():
        string = rolling(message)
        if string != False:
            await message.channel.send(string)
            return
        else:
            return

    if message.content.startswith('at'):
        await do_attack(message)
        return

    if message.content == 'panik':
        embedVar = discord.Embed(title='Panikregeln', description="", color=0x3498DB)
        embedVar.image()
        await message.channel.send(embed=embedVar)

    if message.content.startswith(('+', '-')):
        zahl = 0
        if get_nickname(message) == 'Meister':
            zahl = message.content[-1]
            message.content = message.content[:-2]
        number = message.content
        number = only_numerics(number)
        zone = ''
        if message.content.endswith(('schip', 'chip')):
            embededVar = SP_reg_or_dmg(message, str(message.content[:1]), only_numerics(number), zahl)
        elif message.content[-1].isnumeric():
            embededVar = LP_reg_or_dmg(message, str(message.content[:1]), number, zone, zahl)
            await message.channel.send(embed=embededVar)
            await message.delete()
            return
        elif message.content.endswith("asp"):
            embededVar = LP_reg_or_dmg(message, str(message.content[:1]), number, zone, zahl, True, False)
            await message.channel.send(embed=embededVar)
            await message.delete()
        elif message.content.endswith("kap"):
            embededVar = LP_reg_or_dmg(message, str(message.content[:1]), number, zone, zahl, False, True)
            await message.channel.send(embed=embededVar)
            await message.delete()
        elif message.content.endswith(
                ('furcht', 'paralyse', 'betäubung', 'betaebung', 'verwirrung', 'schmerz', 'berauscht')):
            zustand = message.content.split()[len(message.content.split()) - 1]
            embededVar = zustaende_reg_or_dmg(message, str(message.content[:1]), number, zustand, zahl)
        elif message.content.endswith((' k', ' d', ' s', ' h')):
            money_typ = message.content.split()[len(message.content.split()) - 1]
            embededVar = changing_money(message, str(message.content[:1]), number, money_typ)
        else:
            return
        await message.channel.send(embed=embededVar)


client.run(getenv("TOKEN"))
