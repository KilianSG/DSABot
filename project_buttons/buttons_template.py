from discord import ActionRow, Button, ButtonStyle, SelectMenu, SelectOption


def back_and_start():
    return ActionRow(Button(label='Zurück',
                            custom_id='back',
                            style=ButtonStyle.red),
                     Button(label='Fertig ausgewählt',
                            custom_id='start',
                            style=ButtonStyle.green))


def back_and_start_and_wait():
    return ActionRow(Button(label='Aktion Verzögern',
                            custom_id='interrupt',
                            style=ButtonStyle.blurple),
                     Button(label='Zurück',
                            custom_id='back',
                            style=ButtonStyle.red),
                     Button(label='Fertig ausgewählt',
                            custom_id='start',
                            style=ButtonStyle.green))


def turn_end():
    return ActionRow(Button(label='Beende den Zug',
                            custom_id='end_this',
                            style=ButtonStyle.blurple))


def wait_button():
    return ActionRow(Button(label='Eingreifen',
                            custom_id='eingreifen',
                            style=ButtonStyle.blurple))


def next_turn_button():
    return ActionRow(Button(label='Beginn',
                            custom_id='start',
                            style=ButtonStyle.green))


def pre_combat(combat_list, secondary_list, get_nickname, first_one=None):
    new_list = list(combat_list)
    new_secondary_list = list(secondary_list)
    counter = 0
    in_other_list = [x[0] for x in new_secondary_list]
    components = []
    lose_buttons1 = [(), (), (), (), ()]
    lose_buttons2 = [(), (), (), (), ()]
    for element_is in new_list:
        if element_is in in_other_list:
            index_pos_list = []
            index_pos = 0
            while True:
                try:
                    index_pos = in_other_list.index(element_is, index_pos)
                    index_pos_list.append(index_pos)
                    index_pos += 1
                except:
                    break
            sample_the_options = []
            for option in index_pos_list:
                label_name = new_secondary_list[option][1]
                if len(label_name) > 25:
                    label_name = label_name.split(' ', 1)[1]
                new_option = SelectOption(label=label_name[0:25], value=new_secondary_list[option][1], description= 'wo bin ich?')
                sample_the_options.append(new_option)
            options = []
            for sample in sample_the_options:
                options.append(sample)
            new_menu = ActionRow(SelectMenu(custom_id=element_is, placeholder=element_is, min_values=0, max_values=1, options=options))
            components.append(new_menu)
        else:
            new_button = Button(label=element_is, custom_id=element_is, style=ButtonStyle.grey)
            if counter < 5:
                lose_buttons1[counter] = new_button
            else:
                lose_buttons2[counter - 5] = new_button
            counter += 1
    if lose_buttons1 != [(), (), (), (), ()]:
        components.append(
            ActionRow(lose_buttons1[0], lose_buttons1[1], lose_buttons1[2], lose_buttons1[3], lose_buttons1[4]))
    if lose_buttons2 != [(), (), (), (), ()]:
        components.append(
            ActionRow(lose_buttons2[0], lose_buttons2[1], lose_buttons2[2], lose_buttons2[3], lose_buttons2[4]))

    return components


def liturgie_template(get_nickname, table):
    erzwingen = kosten_senken = dauer_senken = dauer_erhöhen = reichweite_erhöhen = ()
    tiers = [(), (), (), ()]
    for x in range(len(table.tiers_seperated)):
        tiers[x] = (Button(label=table.tiers_seperated[x],
                           custom_id=get_nickname + str(x),
                           style=ButtonStyle.blurple))

    play_button = (Button(label='Beginn',
                          custom_id=get_nickname + 'cast',
                          style=ButtonStyle.red))

    if table.kap == 1:
        erzwingen = (Button(label='Erzwingen',
                            custom_id=get_nickname + 'erzwingen',
                            style=ButtonStyle.grey))
        kosten_senken = (Button(label='Kosten senken',
                                custom_id=get_nickname + 'kosten_senken',
                                style=ButtonStyle.grey))
    if table.reach == 1:
        reichweite_erhöhen = (Button(label='Reichweite erhöhen',
                                     custom_id=get_nickname + 'reichweite_erhöhen',
                                     style=ButtonStyle.grey))
    if table.casttime == 1:
        dauer_erhöhen = (Button(label='Dauer erhöhen',
                                custom_id=get_nickname + 'dauer_erhöhen',
                                style=ButtonStyle.grey))
        dauer_senken = (Button(label='Dauer senken',
                               custom_id=get_nickname + 'dauer_senken',
                               style=ButtonStyle.grey))
    sprache_weglassen = (Button(label='Sprache weglassen',
                                custom_id=get_nickname + 'sprache_weglassen',
                                style=ButtonStyle.grey))
    gesten_weglassen = (Button(label='Gesten weglassen',
                               custom_id=get_nickname + 'gesten_weglassen',
                               style=ButtonStyle.grey))
    components = []
    if not tiers == [(), (), (), ()]:
        components.append(ActionRow(tiers[0], tiers[1], tiers[2], tiers[3]))
    components.append(ActionRow(erzwingen, dauer_erhöhen, sprache_weglassen, reichweite_erhöhen))
    components.append(ActionRow(kosten_senken, dauer_senken, gesten_weglassen, play_button))
    return components


def status_template(get_nickname, spells=0, liturgy=0):
    if spells == liturgy == 0:
        status_template = [ActionRow((Button(label='Status',
                                             custom_id=get_nickname + 'stats',
                                             style=ButtonStyle.green)),
                                     (Button(label='Vor&Nachteile',
                                             custom_id=get_nickname + 'Vor und Nachteile',
                                             style=ButtonStyle.red)),
                                     (Button(label='Sonderfertigkeiten',
                                             custom_id=get_nickname + 'Sonderfertigkeiten',
                                             style=ButtonStyle.blurple)),
                                     (Button(label='Inventar',
                                             custom_id=get_nickname + 'Items',
                                             style=ButtonStyle.blurple)))]
    if spells != 0:
        status_template = [ActionRow((Button(label='Status',
                                             custom_id=get_nickname + 'stats',
                                             style=ButtonStyle.green)),
                                     (Button(label='Vor&Nachteile',
                                             custom_id=get_nickname + 'Vor und Nachteile',
                                             style=ButtonStyle.red)),
                                     (Button(label='Sonderfertigkeiten',
                                             custom_id=get_nickname + 'Sonderfertigkeiten',
                                             style=ButtonStyle.blurple)),
                                     (Button(label='Inventar',
                                             custom_id=get_nickname + 'Items',
                                             style=ButtonStyle.blurple)),
                                     (Button(label='Zauber',
                                             custom_id=get_nickname + 'Spells',
                                             style=ButtonStyle.blurple)))]
    elif liturgy != 0:
        status_template = [ActionRow((Button(label='Status',
                                             custom_id=get_nickname + 'stats',
                                             style=ButtonStyle.green)),
                                     (Button(label='Vor&Nachteile',
                                             custom_id=get_nickname + 'Vor und Nachteile',
                                             style=ButtonStyle.red)),
                                     (Button(label='Sonderfertigkeiten',
                                             custom_id=get_nickname + 'Sonderfertigkeiten',
                                             style=ButtonStyle.blurple)),
                                     (Button(label='Inventar',
                                             custom_id=get_nickname + 'Items',
                                             style=ButtonStyle.blurple)),
                                     (Button(label='Liturgien',
                                             custom_id=get_nickname + 'Liturgie',
                                             style=ButtonStyle.blurple)))]
    return status_template


def schicksals_row_begabungs_row_template(get_nickname, schicksalsrow=0, begabungsrow=0):
    components = []
    if schicksalsrow != 0:
        Schicksals_Row = ActionRow((Button(label='',
                                           emoji='<:d1:933880668981690441>',
                                           custom_id=get_nickname + 'reroll1',
                                           style=ButtonStyle.green)),
                                   Button(label='',
                                          emoji='<:d2:933880684341252107>',
                                          custom_id=get_nickname + 'reroll2',
                                          style=ButtonStyle.blurple),
                                   Button(label='',
                                          emoji='<:d3:933880696144007198>',
                                          custom_id=get_nickname + 'reroll3',
                                          style=ButtonStyle.red),
                                   Button(label='',
                                          emoji='<:red_dice:933643340442914826>',
                                          custom_id=get_nickname + 'Schicksal',
                                          style=ButtonStyle.grey))
        components.append(Schicksals_Row)
    if begabungsrow == 1:
        Begabungs_Row = ActionRow((Button(label='',
                                          emoji='<:nandus_1:933799404928905329>',
                                          custom_id=get_nickname + 'begabung1',
                                          style=ButtonStyle.green)),
                                  Button(label='',
                                         emoji='<:nandus_2:933799429922775040>',
                                         custom_id=get_nickname + 'begabung2',
                                         style=ButtonStyle.blurple),
                                  Button(label='',
                                         emoji='<:nandus_1:933799449522745344>',
                                         custom_id=get_nickname + 'begabung3',
                                         style=ButtonStyle.red))
        components.append(Begabungs_Row)
    elif begabungsrow == -1:
        Begabungs_Row = ActionRow(
            (Button(label='Unfähigkeit', custom_id=get_nickname + 'unfähig1', style=ButtonStyle.red)))
        components.append(Begabungs_Row)
    return components


def schicksal_spells(get_nickname, schicksalsrow=0, begabungsrow=0):
    components = []
    if begabungsrow == 1:
        Begabungs_Row = ActionRow((Button(label='',
                                          emoji='<:nandus_1:933799404928905329>',
                                          custom_id=get_nickname + 'begabung1',
                                          style=ButtonStyle.green)),
                                  Button(label='',
                                         emoji='<:nandus_2:933799429922775040>',
                                         custom_id=get_nickname + 'begabung2',
                                         style=ButtonStyle.blurple),
                                  Button(label='',
                                         emoji='<:nandus_1:933799449522745344>',
                                         custom_id=get_nickname + 'begabung3',
                                         style=ButtonStyle.red))
        components.append(Begabungs_Row)
    if schicksalsrow != 0:
        Schicksals_Row = ActionRow((Button(label='',
                                           emoji='<:d1:933880668981690441>',
                                           custom_id=get_nickname + 'reroll1',
                                           style=ButtonStyle.green)),
                                   Button(label='',
                                          emoji='<:d2:933880684341252107>',
                                          custom_id=get_nickname + 'reroll2',
                                          style=ButtonStyle.blurple),
                                   Button(label='',
                                          emoji='<:d3:933880696144007198>',
                                          custom_id=get_nickname + 'reroll3',
                                          style=ButtonStyle.red),
                                   Button(label='',
                                          emoji='<:red_dice:933643340442914826>',
                                          custom_id=get_nickname + 'Schicksal',
                                          style=ButtonStyle.grey))
        components.append(Schicksals_Row)
        Schicksals_Row = ActionRow((Button(label='QS+1', costum_id=get_nickname + 'qs', style=ButtonStyle.blurple)))
        components.append(Schicksals_Row)
    if begabungsrow == -1:
        Begabungs_Row = ActionRow(
            (Button(label='Unfähigkeit', custom_id=get_nickname + 'unfähig1', style=ButtonStyle.red)))
        components.append(Begabungs_Row)
    return components
