# Figure out who is currently in cycle
# Store this as the number value of their place in txts
# sum(pityList) -> maxValue
# if maxValue == 0, select someone random
# Otherwise run the selector
# random.choices(namesList, weights=pityList)
# Update pity with formula
import lib
import main
import random
import datetime as dt


async def selection():
    newDate = dt.datetime.now() + dt.timedelta(days=int(main.turnLength))
    dateObject = dt.datetime(year=newDate.year, month=newDate.month, day=newDate.day, hour=16)
    output = f'<t:{int(dt.datetime.timestamp(dateObject))}:R>'
    lib.dump_data(output, 'next_change', 'w', 'data.yml')

    amountToSelect = main.playerCount - len(main.messagedPlayer)
    pityList = []
    for i in range(len(main.players)):
        pityList.append(main.players[i]['pity'])
    idList = []
    for i in range(len(main.players)):
        idList.append(main.players[i]['id'])
    relayRunners = []
    for member in main.client.guilds[1].members:
        if member.get_role(main.role) is not None:
            relayRunners.append(member.id)
    if not relayRunners:
        await lib.send_message("No one is playing relayworld anymore.. :(", 'channel', main.mainChannel)
    else:
        chosenPlayer = []
        prunedList = []
        prunedPity = []
        for i in range(len(idList)):
            if idList[i] in relayRunners and i not in main.unavailablePlayers and i not in main.messagedPlayer and i not in main.currentPlayer:
                prunedList.append(i)
                prunedPity.append(pityList[i])
        if len(prunedList) == 0:
            await lib.send_message("No one was available for this turn", 'channel', main.mainChannel)
        elif len(prunedList) <= amountToSelect:
            print("Amount of players too low OR just enough for the set amount of players. Proceeding with everyone available.")
            for i in range(len(prunedList)):
                await lib.send_message(f"You have been selected for next relayworld turn, planned to start {main.nextChange}, though the current player(s) could end their turn early. Respond with .? unavailable if you are unavailable, and your pity score will not be affected. You do not need to respond if you are available", 'dm', idList[prunedList[i]])
            for i in range(len(main.messagedPlayer)):
                prunedList.append(main.messagedPlayer[i])
            lib.dump_data(prunedList, 'messaged_player', 'w', 'data.yml')
        elif len(prunedList) > amountToSelect:
            for i in range(amountToSelect):
                if sum(prunedPity) > 0:
                    chosenPlayer.append(random.choices(prunedList, weights=prunedPity, k=1)[0])
                else:
                    chosenPlayer.append(random.choices(prunedList, k=1)[0])
                prunedList.remove(chosenPlayer[-1])
                prunedPity.remove(pityList[chosenPlayer[-1]])
            for i in range(len(chosenPlayer)):
                await lib.send_message(f"You have been selected for next relayworld turn, planned to start {main.nextChange}, though the current player(s) could end their turn early. Respond with .? unavailable if you are unavailable, and your pity score will not be affected. You do not need to respond if you are available", 'dm', idList[chosenPlayer[i]])
                #for i in range(len(chosenPlayer)):
                    #chosenPlayer.append(main.messagedPlayer[i])
            lib.dump_data(chosenPlayer, 'messaged_player', 'w', 'data.yml')


async def next_turn():
    playersEnding = main.currentPlayer
    playersStarting = main.messagedPlayer
    pastPlayers = main.pastPlayers
    for i in range(len(playersEnding)):
        pastPlayers.append(playersEnding[i])
    lib.dump_data(pastPlayers, 'past_players', 'w', 'data.yml')
    lib.dump_data(playersStarting, 'current_player', 'w', 'data.yml')
    update_pity()
    for i in range(len(playersEnding)):
        if main.changeMode == 'upload':
            await lib.send_message(
                f"Your time is up! Upload the save file to the [drive]({main.driveLink}) and let the next person know when it is uploaded",
                'dm', main.players[playersEnding[i]]['id'])
        elif main.changeMode == 'server':
            await lib.send_message("Your time is up! Please unwhitelist yourself or do not join the server", 'dm', main.players[playersEnding[i]]['id'])
            #Could include an api here to whitelist or unwhitelist
    annStarts = ["Hey ", "I'm in the IRL discord, and a new Relayworld cycle just started, featuring ", "Let's all hope ", "Clean up the shulker monster before you leave, ", "Can you believe it's ", "Hey ", "It's time for ", "New cycle, I'm too tired to think of another phrase for this but "]
    annEnds = [", wake up. It's time for your cycle.", ".", " doesn't die.", ".", "'s turn again???", ", please don't mess up the enderchest like last time.", " to build more ducks.", " is playing now."]
    r = random.randint(0, 7)

    selectedIds = []
    for i in range(len(playersStarting)):
        selectedIds.append(f"<@{main.players[playersStarting[i]]['id']}>")
    await lib.send_message(annStarts[r] + ", ".join(selectedIds) + annEnds[r], 'channel', main.mainChannel)
    if main.changeMode == 'upload':
        await lib.send_message(f'The world can be found on the [drive]({main.driveLink}). Good luck!', 'channel', main.mainChannel)
    elif main.changeMode == 'server':
        await lib.send_message(f'The server ip is {main.serverIp}. Good luck!', 'channel', main.mainChannel)
    lib.dump_data(False, 'upload_anti_spam', 'w', 'data.yml')
    lib.dump_data([], 'unavailable_players', 'w', 'data.yml')
    lib.dump_data([], 'messaged_player', 'w', 'data.yml')
    await selection()


def update_pity():
    pityList = []
    idList = []
    pastPlayers = []
    relayRunners = []
    newPity = []
    for i in range(int(main.rechargeTime)):
        pastPlayers.append(main.pastPlayers[(-i-1)])
    for i in range(len(main.players)):
        pityList.append(main.players[i]['pity'])
        idList.append(main.players[i]['id'])
    for member in main.client.guilds[1].members:
        if member.get_role(main.role) is not None:
            relayRunners.append(member.id)

    for i in range(len(pityList)):
        if i in pastPlayers or i in main.currentPlayer:
            newPity.append(0)
        elif idList[i] in relayRunners:
            newPity.append(round((int(pityList[i]) * (1 + random.random()))) + random.randint(1, 3))
        else:
            newPity.append(pityList[i])

    for i in range(len(newPity)):
        lib.dump_data(newPity[i], 'players', 'w', 'data.yml', dest2=i, dest3='pity')
