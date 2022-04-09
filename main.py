import json
import os

import discord
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import View
from dotenv import load_dotenv

from character.add_picture import add_picture_to_character
from character.characters_do_stuff import w20
from character.characters_do_stuff.combat import embed_pre_combat
from character.characters_do_stuff.liturgie import prep_liturgy
from character.characters_do_stuff.talent import get_nickname, what_talent
from character.create_character import loading_character
from helpers.help_with_await import plus_minus, help_with_status

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)
load_dotenv('.env')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


class MyView(View):
    @discord.ui.button(label='new buttons', style=ButtonStyle.grey)
    async def button_callback(self, interaction: discord.Interaction, button):
        await interaction.response.send_message("hallo")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    message.content = message.content.lower()
    dbname = str(message.guild) + str(message.author)
    name_to_find = str(get_nickname(message))
    number = 0
    character = None
    for attachment in message.attachments:
        if attachment.filename.lower().endswith('json'):
            await attachment.save(attachment.filename)
            with open(attachment.filename, 'r', encoding='utf8') as openfile:
                newchar = json.load(openfile)
            import os
            os.remove(attachment.filename)
            embed_view = loading_character(message, newchar)
            await message.channel.send(embed=embed_view[0], view=embed_view[1])
            return
        image_types = ["jpg", "jpeg", "png"]
        if any(attachment.filename.lower().endswith(image) for image in image_types):
            if not message.content.startswith('add'):
                return
            string = add_picture_to_character(message)
            await message.channel.send(string)
            return
    with open('jsoned_characters.json') as f:
        db = json.load(f)
    try:
        character = db.get(dbname).get(name_to_find)
    except:
        pass
    if name_to_find == 'Meister':
        number = message.content[-1]
        character = db.get(dbname).get('Meister').get('number')
    if message.content == 'test':
        view = embed_pre_combat(name_to_find, 'True', character)
        await message.channel.send("nachricht", view=view)
    if message.content.startswith('l '):
        embed_view = prep_liturgy(message, name_to_find, character)
        await message.channel.send(embed=embed_view[0], view=embed_view[1])
    if message.content == 'status':
        character = db.get(dbname)
        embeds = help_with_status(character, name_to_find)
        await message.channel.send(embed=embeds[0], view=embeds[1])
    if message.content.startswith(('+', '-')):
        embed = plus_minus(message.content[0], message, number)
        if embed is not None:
            await message.channel.send(embed=embed)
    if message.content.startswith('t '):
        embed_view = what_talent(message)
        await message.channel.send(embed=embed_view[0], view=embed_view[1])
    if all(x for x in message.content if x.isdigit() or x == 'w'):
        await message.channel.send(w20.rolling(message))


client.run(os.environ.get("Token"))
