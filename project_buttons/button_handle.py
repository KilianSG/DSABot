from discord import ButtonStyle, SelectMenu


def handle_in_combat_button(buttonid, character, liste_of_changes: list, components):
    print('handle a button_click')
    print(components)
    if buttonid in liste_of_changes:
        liste_of_changes.remove(buttonid)
    else:
        liste_of_changes.append(liste_of_changes)
    for item in components:
        for button in item:
            if isinstance(button, SelectMenu):
                continue
            if buttonid == button.custom_id:
                if button.style == ButtonStyle.red:
                    button.update(style=ButtonStyle.grey)
                else:
                    button.update(style=ButtonStyle.red)
                print(components)
                return components
    return components


def handle_in_combat(select_id, character, liste_of_changes, components):
    print('todo_list of all things with a system to find them fast (key value?)')
    for item in components:
        for actionRow in item:
            if isinstance(actionRow, SelectMenu):
                print(actionRow)
                return components
    return components


def only_numerics(seq):
    seq_type = type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))


def handle_modification_liturgy(button_id, maximum_mods, counter, list_of_modification, copy_liturgy, abilities_table):
    if button_id.endswith('erzwingen'):
        if not 'Erzwingen' in list_of_modification and maximum_mods > counter:
            list_of_modification.append('Erzwingen')
            list_of_changes = [2, -1]
        elif 'Erzwingen' in list_of_modification:
            list_of_modification.remove('Erzwingen')
            list_of_changes = [0.5, 1]
        else:
            list_of_changes = [1, 0]
        copy_liturgy['KaP-Kosten'] = str(int(int(only_numerics(copy_liturgy['KaP-Kosten'])) * list_of_changes[0]))
        for x in range(3):
            abilities_table[x] -= list_of_changes[1]
        counter -= list_of_changes[1]
    elif button_id.endswith('kosten_senken'):
        if not 'Kosten senken' in list_of_modification and maximum_mods > counter:
            list_of_modification.append('Kosten senken')
            list_of_changes = [0.5, -1]
        elif 'Kosten senken' in list_of_modification:
            list_of_modification.remove('Kosten senken')
            list_of_changes = [2, 1]
        else:
            list_of_changes = [1, 0]
            copy_liturgy['KaP-Kosten'] = str(int(int(only_numerics(copy_liturgy['KaP-Kosten'])) * list_of_changes[0]))
            for x in range(3):
                abilities_table[x] -= list_of_changes[1]
            counter -= list_of_changes[1]

    elif button_id.endswith('reichweite_erhöhen'):
        if not 'Reichweite erhöhen' in list_of_modification and maximum_mods > counter:
            list_of_modification.append('Reichweite erhöhen')
            list_of_changes = [2, 1]
        elif 'Reichweite erhöhen' in list_of_modification:
            list_of_modification.remove('Reichweite erhöhen')
            list_of_changes = [0.5, -1]
        else:
            list_of_changes = [1, 0]
        copy_liturgy['Reichweite'] = str(int(int(only_numerics(copy_liturgy['Reichweite'])) * list_of_changes[0]))
        for x in range(3):
            abilities_table[x] -= list_of_changes[1]
        counter -= list_of_changes[1]

    elif button_id.endswith('dauer_erhöhen'):
        if not 'Dauer erhöhen' in list_of_modification and maximum_mods > counter:
            list_of_modification.append('Dauer erhöhen')
            list_of_changes = [2, -1]
        elif 'Dauer erhöhen' in list_of_modification:
            list_of_modification.remove('Dauer erhöhen')
            list_of_changes = [0.5, 1]
        else:
            list_of_changes = [1, 0]
        copy_liturgy['Liturgiedauer'] = str(int(int(only_numerics(copy_liturgy['Liturgiedauer'])) * list_of_changes[0]))
        for x in range(3):
            abilities_table[x] -= list_of_changes[1]
        counter -= list_of_changes[1]

    elif button_id.endswith('dauer_senken'):
        if not 'Dauer senken' in list_of_modification and maximum_mods > counter:
            if copy_liturgy['Liturgiedauer'] != "1 Aktion(en)":
                list_of_modification.append('Dauer senken')
                list_of_changes = [0.5, -1]
            else:
                list_of_changes = [1, 0]
        elif 'Dauer senken' in list_of_modification:
            list_of_modification.remove('Dauer senken')
            list_of_changes = [2, 1]
        else:
            list_of_changes = [1, 0]
        copy_liturgy['Liturgiedauer'] = str(int(int(only_numerics(copy_liturgy['Liturgiedauer'])) * list_of_changes[0]))
        for x in range(3):
            abilities_table[x] -= list_of_changes[1]
        counter -= list_of_changes[1]

    elif button_id.endswith('sprache_weglassen'):
        if not 'Sprache weglassen' in list_of_modification and maximum_mods > counter:
            list_of_modification.append('Sprache weglassen')
            list_of_changes = [-1, 1]
        elif 'Sprache weglassen' in list_of_modification:
            list_of_modification.remove('Sprache weglassen')
            list_of_changes = [1, -1]
        else:
            list_of_changes = [1, 0]
        for x in range(3):
            abilities_table[x] -= 2 * list_of_changes[1]
        counter -= list_of_changes[1]

    elif button_id.endswith('gesten_weglassen'):
        if not 'Gesten weglassen' in list_of_modification and maximum_mods > counter:
            list_of_modification.append('Gesten weglassen')
            list_of_changes = [-1, 1]
        elif 'Gesten weglassen' in list_of_modification:
            list_of_modification.remove('Gesten weglassen')
            list_of_changes = [1, -1]
        else:
            list_of_changes = [1, 0]
        for x in range(3):
            abilities_table[x] -= 2 * list_of_changes[1]
        counter -= list_of_changes[1]
    return [maximum_mods, counter, list_of_modification, copy_liturgy, abilities_table]


def handle_status(button_id, printable_character):
    print('handle')
    if button_id.endswith('stats'):
        imbed_to_send = printable_character.embed
    elif button_id.endswith('Vor und Nachteile'):
        imbed_to_send = printable_character.embed1
    elif button_id.endswith('Sonderfertigkeiten'):
        imbed_to_send = printable_character.embed2
    elif button_id.endswith('Items'):
        imbed_to_send = printable_character.embed3
    elif button_id.endswith('Spells'):
        imbed_to_send = printable_character.embed4
    elif button_id.endswith('Liturgie'):
        imbed_to_send = printable_character.embed5
    return imbed_to_send
