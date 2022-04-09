import discord
from discord import ButtonStyle, SelectOption
from discord.ui import Button, Select, View

from project_buttons.view_interactions.fortunetalentview import probe_schicksal, probe_begabung


def get_all_select_menu_items_liturgy(table):
    list_of_modifications = []
    if table.kap == 1:
        list_of_modifications.append(SelectOption(label='Erzwingen', description='1 Erleichterung, doppelte kosten'))
        list_of_modifications.append(SelectOption(label='Kosten senken', description='1 Erschwernis, halbe kosten'))
    if table.reach == 1:
        list_of_modifications.append(
            SelectOption(label='Reichweite erhöhen', description='1 Erschwernis, doppelte Reichweite'))
    if table.casttime == 1:
        list_of_modifications.append(
            SelectOption(label='Dauer erhöhen', description='1 Erleichterung, doppelte Spruchzeit'))
        list_of_modifications.append(
            SelectOption(label='Dauer senken', description='1 Erschwernis, halbe Spruchzeit'))
    list_of_modifications.append(
        SelectOption(label='Sprache weglassen', description='2 Erschwernis'))
    list_of_modifications.append(
        SelectOption(label='Gesten weglassen', description='2 Erschwernis'))
    list_of_modifications.append(
        SelectOption(label='Keine Modifikation')
    )
    return list_of_modifications


def get_all_select_menu_items(element_is, in_other_list, new_secondary_list):
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            index_pos = in_other_list.index(element_is, index_pos)
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    sample_the_options = []
    for option in index_pos_list:
        label_name = new_secondary_list[option][1]
        new_option = SelectOption(label=label_name[0:100], value=new_secondary_list[option][1])
        sample_the_options.append(new_option)
    list_of_select_options = []
    for x in sample_the_options:
        new_select_option = SelectOption(value=str(x), label=str(x), description='noch nichts')
        list_of_select_options.append(new_select_option)
    list_of_select_options.append(
        SelectOption(label="Nichts Ausgewählt", value="Nichts Ausgewählt", description='Keine Veränderung'))
    return list_of_select_options


class VariableButton(Button):
    @property
    def view(self):
        return self._view

    def __init__(self, this_element, view):
        super().__init__()
        self.label = this_element
        self.style = ButtonStyle.grey
        self.callback = self.button_callback
        self.view = view

    async def button_callback(self, interaction):
        if self.style == ButtonStyle.grey:
            self.style = ButtonStyle.red
        else:
            self.style = ButtonStyle.grey
        await interaction.response.edit_message(view=self.view)

    @view.setter
    def view(self, value):
        self._view = value


class VariableSelect(Select):
    @property
    def view(self):
        return self._view

    def __init__(self, this_element, list_of_select_option, view):
        super().__init__()
        self.placeholder = this_element
        self.view = view
        for select_option in list_of_select_option:
            self.append_option(select_option)
        self.callback = self.select_callback
        self.row = 0

    async def select_callback(self, interaction: discord.Interaction):
        for x in self.options:
            x.default = False
        new_trendsetter = [x for x in self.options if x.label == self.values[0]][0]
        new_trendsetter.default = True
        await interaction.response.edit_message(view=self.view)

    @view.setter
    def view(self, value):
        self._view = value


class CombatView(View):
    combat_list = []
    secondary_list = []

    def __init__(self, combat_list, secondary_list, discord_name, character, pre_combat=True):
        super().__init__()
        self.discord_name = discord_name
        self.character = character
        self.combat_list = list(combat_list)
        print(self.combat_list)
        self.secondary_list = list(secondary_list)
        new_list = list(combat_list)
        print(new_list)
        new_secondary_list = list(secondary_list)
        in_other_list = [x[0] for x in new_secondary_list]

        for element_is in new_list:
            if element_is in in_other_list:
                list_of_select_options = get_all_select_menu_items(element_is, in_other_list, new_secondary_list)
                new_select = VariableSelect(element_is, list_of_select_options, self)
                self.add_item(new_select)
            else:
                new_button = VariableButton(element_is, self)
                self.add_item(new_button)

    @discord.ui.button(label="Fertig ausgewählt", custom_id="Fertig ausgewählt", style=ButtonStyle.grey, row=4)
    async def finished_callback(self, interaction, button: discord.ui.Button):
        self.stop()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Aktion Verzögern", custom_id="Aktion Verzögern", style=ButtonStyle.grey, row=4)
    async def delay_callback(self, interaction, button: discord.ui.Button):
        button.label = 'Aktion Verzögert!'
        await interaction.response.edit_message(view=self)

    async def button_callback(self, button, interaction):
        if button.style == ButtonStyle.grey:
            button.style = ButtonStyle.red
        else:
            button.style = ButtonStyle.grey
        await interaction.response.edit_message(view=self)

    async def interaction_check(self, interaction) -> bool:
        nickname = interaction.user.display_name.split('"')
        if nickname[1] != self.discord_name and not interaction.user.display_name.startswith('"Meister"'):
            await interaction.response.send_message(f"Du bist nicht {self.discord_name}", ephemeral=True)
            return False
        return True


class StatusView(View):
    def __init__(self, get_nickname, embed):
        super().__init__()
        self.embed = embed
        if embed.zauber != 1:
            for children in self.children:
                if children.label == 'Zauber':
                    self.remove_item(children)
        if embed.liturgie != 1:
            for children in self.children:
                if children.label == 'Liturgien':
                    self.remove_item(children)

    @discord.ui.button(label='Status', style=ButtonStyle.grey, row=0)
    async def status_callback(self, interaction, button):
        for children in self.children:
            children.style = ButtonStyle.grey
        button.style = ButtonStyle.blurple
        await interaction.response.edit_message(embed=self.embed.embed, view=self)

    @discord.ui.button(label='Vor&Nachteile', style=ButtonStyle.grey, row=0)
    async def advantage_disadventage_callback(self, interaction, button):
        for children in self.children:
            children.style = ButtonStyle.grey
        button.style = ButtonStyle.blurple
        await interaction.response.edit_message(embed=self.embed.embed1, view=self)

    @discord.ui.button(label='Sonderfertigkeit', style=ButtonStyle.grey, row=0)
    async def special_abilities_callback(self, interaction, button):
        for children in self.children:
            children.style = ButtonStyle.grey
        button.style = ButtonStyle.blurple
        await interaction.response.edit_message(embed=self.embed.embed2, view=self)

    @discord.ui.button(label='Inventar', style=ButtonStyle.grey, row=0)
    async def inventory_callback(self, interaction, button):
        for children in self.children:
            children.style = ButtonStyle.grey
        button.style = ButtonStyle.blurple
        await interaction.response.edit_message(embed=self.embed.embed3, view=self)

    @discord.ui.button(label='Liturgien', style=ButtonStyle.grey)
    async def liturgy_callback(self, interaction, button):
        for children in self.children:
            children.style = ButtonStyle.grey
        button.style = ButtonStyle.blurple
        await interaction.response.edit_message(embed=self.embed.embed5, view=self)

    @discord.ui.button(label='Zauber', style=ButtonStyle.grey)
    async def spells_callback(self, interaction, button):
        for children in self.children:
            children.style = ButtonStyle.grey
        button.style = ButtonStyle.blurple
        await interaction.response.edit_message(embed=self.embed.embed4, view=self)


class LiturgySelect(Select):
    @property
    def view(self):
        return self._view

    def __init__(self, list_of_select_option, liturgy, view):
        super().__init__()
        self.view = view
        self.liturgy = liturgy
        for select_option in list_of_select_option:
            self.append_option(select_option)
        self.callback = self.select_callback
        self.max_values = int(liturgy['fw'] / 4) + 1
        self.placeholder = f"Modifizierungen, maximal {str(self.max_values - 1)}"
        self.min_values = 1
        self.callback = self.select_callback
        self.row = 0

    async def select_callback(self, interaction: discord.Interaction):
        if "Keine Modifikation" in (value for value in self.values):
            self.placeholder = self.placeholder = f"Modifizierungen, maximal {str(self.max_values - 1)}"
        else:
            self.placeholder = ''
            for value in self.values:
                self.placeholder += f'{value} '
        await interaction.response.edit_message(view=self.view)

    @view.setter
    def view(self, value):
        self._view = value


class LiturgyTemplate(View):
    def __init__(self, discord_name, table, character, liturgy, liturgy_name: str, attributes: list, in_combat=False):
        super().__init__()
        self.discord_name = discord_name
        all_options = get_all_select_menu_items_liturgy(table)
        self.add_item(LiturgySelect(all_options, liturgy, self))

    @discord.ui.button(label='Wirken!', emoji='<:roll:961976524532228126>', style=ButtonStyle.blurple, row=4)
    async def button_callback(self, interaction, button, ):
        button.label = 'Du wirkst mit ...'
        for value in self.children[1].values:
            button.label += f'{str(value)}'
        button.disable = True
        self.remove_item([x for x in self.children if isinstance(x, Select)][0])
        await interaction.response.edit_message(view=self)

    async def interaction_check(self, interaction) -> bool:
        nickname = interaction.user.display_name.split('"')
        if nickname[1] != self.discord_name and not interaction.user.display_name.startswith('"Meister"'):
            await interaction.response.send_message(f"Du bist nicht {self.discord_name}", ephemeral=True)
            return False
        return True


class FortuneTalentView(View):
    def __init__(self, embed, has_talent, has_fate, block_attributes, fw_copy, qs, block_roll):
        super().__init__()
        self.embed = embed
        self.has_talent = has_talent
        self.has_fate = has_fate
        self.block_attributes = block_attributes
        self.fw_copy = fw_copy
        self.qs = qs
        self.block_roll = block_roll
        if has_fate == 0:
            for children in self.children:
                if children.custom_id.startswith(('reroll', 'Fate')):
                    self.remove_item(children)
        if has_talent == 0:
            for children in self.children:
                if children.custom_id.startswith(('talent', 'unable')):
                    self.remove_item(children)
        elif has_talent > 0:
            for children in self.children:
                if children.custom_id.startswith('unable'):
                    self.remove_item(children)
        elif has_talent == -1:
            for children in self.children:
                if children.custom_id.startswith('talent'):
                    self.remove_item(children)

    list_of_rerolls = [0, 0, 0]

    @discord.ui.button(label='',
                       emoji='<:d1:933880668981690441>',
                       custom_id='reroll1',
                       style=ButtonStyle.blurple)
    async def reroll1_callback(self, interaction, button):
        if button.style == ButtonStyle.blurple:
            button.style = ButtonStyle.grey
            self.list_of_rerolls[0] = 1
        else:
            self.list_of_rerolls[0] = 0
            button.style = ButtonStyle.blurple
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='',
                       emoji='<:d2:933880684341252107>',
                       custom_id='reroll2',
                       style=ButtonStyle.blurple)
    async def reroll2_callback(self, interaction, button):
        if button.style == ButtonStyle.blurple:
            button.style = ButtonStyle.grey
            self.list_of_rerolls[1] = 1
        else:
            self.list_of_rerolls[1] = 0
            button.style = ButtonStyle.blurple
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='',
                       emoji='<:d3:933880696144007198>',
                       custom_id='reroll3',
                       style=ButtonStyle.blurple)
    async def reroll3_callback(self, interaction, button):
        if button.style == ButtonStyle.blurple:
            button.style = ButtonStyle.grey
            self.list_of_rerolls[2] = 1
        else:
            self.list_of_rerolls[2] = 0
            button.style = ButtonStyle.blurple
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='',
                       emoji='<:red_dice:933643340442914826>',
                       custom_id='Fate',
                       style=ButtonStyle.grey)
    async def fate_callback(self, interaction, button):
        if self.list_of_rerolls == ():
            interaction.response.send_message("Du hast keine Würfel, zum neu würfeln, ausgewählt", ephemeral=True)
        embedVar = probe_schicksal(embedVar=self.embed, block_attributes=self.block_attributes, fw_copy=self.fw_copy,
                                   qs=self.qs, block_roll=self.block_roll, reroll=self.list_of_rerolls)
        self.has_fate -= 1
        if self.has_fate == 0:
            for children in self.children:
                if children.custom_id.startswith(('Fate', 'reroll')):
                    self.remove_item(children)
        await interaction.response.edit_message(embed=embedVar, view=self)

    @discord.ui.button(label='',
                       emoji='<:nandus1:933799404928905329>',
                       custom_id='talent1',
                       style=ButtonStyle.blurple,
                       row=2)
    async def talent1_callback(self, interaction, button):
        embedVar = probe_begabung(embedVar=self.embed, block_eigenschaften=self.block_attributes, reroll=2,
                                  FW_copy=self.fw_copy, QS=self.qs,
                                  block_roll=self.block_roll)
        for children in self.children:
            if children.custom_id.startswith('talent'):
                self.remove_item(children)
        await interaction.response.edit_message(embed=embedVar, view=self)

    @discord.ui.button(label='',
                       emoji='<:nandus2:933799429922775040>',
                       custom_id='talent2',
                       style=ButtonStyle.blurple,
                       row=2)
    async def talent2_callback(self, interaction, button):
        embedVar = probe_begabung(embedVar=self.embed, block_eigenschaften=self.block_attributes, reroll=2,
                                  FW_copy=self.fw_copy, QS=self.qs,
                                  block_roll=self.block_roll)
        for children in self.children:
            if children.custom_id.startswith('talent'):
                self.remove_item(children)
        await interaction.response.edit_message(embed=embedVar, view=self)

    @discord.ui.button(label='',
                       emoji='<:nandus3:933799449522745344>',
                       custom_id='talent3',
                       style=ButtonStyle.blurple,
                       row=2
                       )
    async def talent3_callback(self, interaction, button):
        embedVar = probe_begabung(embedVar=self.embed, block_eigenschaften=self.block_attributes, reroll=2,
                                  FW_copy=self.fw_copy, QS=self.qs,
                                  block_roll=self.block_roll)
        for children in self.children:
            if children.custom_id.startswith('talent'):
                self.remove_item(children)
        await interaction.response.edit_message(embed=embedVar, view=self)

    @discord.ui.button(label='Unfähig',
                       custom_id='unable',
                       style=ButtonStyle.grey,
                       row=4
                       )
    async def unable_callback(self, interaction, button):
        embedVar = probe_begabung(embedVar=self.embed, block_eigenschaften=self.block_attributes, reroll=2,
                                  FW_copy=self.fw_copy, QS=self.qs,
                                  block_roll=self.block_roll, unable=-1)
        await interaction.response.edit_message(embed=embedVar, view=self)


def schicksal_spells(get_nickname, schicksalsrow=0, begabungsrow=0):
    new_view = View()

    if schicksalsrow != 0:
        new_view.add_item(Button(label='',
                                 emoji='<:d1:933880668981690441>',
                                 custom_id=get_nickname + 'reroll1',
                                 style=ButtonStyle.green))
        new_view.add_item(Button(label='',
                                 emoji='<:d2:933880684341252107>',
                                 custom_id=get_nickname + 'reroll2',
                                 style=ButtonStyle.blurple))
        new_view.add_item(Button(label='',
                                 emoji='<:d3:933880696144007198>',
                                 custom_id=get_nickname + 'reroll3',
                                 style=ButtonStyle.red))
        new_view.add_item(Button(label='',
                                 emoji='<:red_dice:933643340442914826>',
                                 custom_id=get_nickname + 'Schicksal',
                                 style=ButtonStyle.grey))

    if begabungsrow == 1:
        new_view.add_item(Button(label='',
                                 emoji='<:nandus_1:933799404928905329>',
                                 custom_id=get_nickname + 'begabung1',
                                 style=ButtonStyle.green))
        new_view.add_item(Button(label='',
                                 emoji='<:nandus_2:933799429922775040>',
                                 custom_id=get_nickname + 'begabung2',
                                 style=ButtonStyle.blurple))
        new_view.add_item(Button(label='',
                                 emoji='<:nandus_1:933799449522745344>',
                                 custom_id=get_nickname + 'begabung3',
                                 style=ButtonStyle.red))

    elif begabungsrow == -1:
        new_view.add_item(Button(label='Unfähigkeit', custom_id=get_nickname + 'unfähig1', style=ButtonStyle.red))

    return new_view
