import random


def probe_begabung(embedVar, block_eigenschaften, FW_copy, QS,
                   block_roll, reroll, unable=1):
    FW = FW_copy

    if unable == -1:
        reroll_this = 20
        reroll = 0
        for x in range(3):
            if block_roll[x] <= reroll_this:
                reroll_this = block_roll[x]
                reroll = x

    old_roll = block_roll[int(reroll)]
    new_roll = block_roll[int(reroll)] = random.randint(1, 20)
    if unable == 1 and block_eigenschaften[int(reroll)] > old_roll:
        block_eigenschaften[int(reroll)] = old_roll

    for i in range(3):
        if block_roll[i] > block_eigenschaften[i]:
            FW = FW - block_roll[i] + block_eigenschaften[i]

    QS_return = int(FW / 3 + 1 + QS - 0.001)
    Was_fuer_ne_probe = {-1: 'Unfähigkeit', 1: 'Begabung'}
    embedVar.add_field(name=f'{Was_fuer_ne_probe[unable]} für den {reroll + 1}ten Würfel',
                       value=f'{old_roll}-->{new_roll}.', inline=False)
    if old_roll > new_roll * unable:
        embedVar.add_field(name=f'Ergebnis mit {Was_fuer_ne_probe[unable]}',
                           value=f'QS {QS_return} | FP :{FW}/{FW_copy}', inline=False)
    else:
        embedVar.add_field(name=f'Ergebnis mit {Was_fuer_ne_probe[unable]}', value='Keine Änderung des Ergebnis',
                           inline=False)
    return embedVar


def probe_schicksal(embedVar, block_attributes, fw_copy, qs,
                    block_roll, reroll):
    fw = fw_copy
    old_list = [0] * 3

    for x in range(3):
        old_list[x] = block_roll[x]
        if reroll[x] == 1:
            block_roll[x] = random.randint(1, 20)

    for i in range(3):
        if block_roll[i] > block_attributes[i]:
            fw = fw - block_roll[i] + block_attributes[i]

    QS_return = int(fw / 3 + 1 + qs - 0.001)

    embedVar.add_field(name=f'Schicksalswürfe',
                       value=f'{old_list[0]}|{old_list[1]}|{old_list[2]}-->{block_roll[0]}|{block_roll[1]}|{block_roll[2]}',
                       inline=False)
    embedVar.add_field(name='Ergebnis mit Schicksalspunkt', value=f'QS {QS_return} | FP :{fw}/{fw_copy}', inline=False)
    return embedVar
