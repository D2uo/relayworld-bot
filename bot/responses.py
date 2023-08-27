import lib
import main
import processor
import datetime

# await messager.send_message('https://youtu.be/dQw4w9WgXcQ', 'response', message.channel) - Rickroll


# Checks what command is being run
async def handle_command(message):
    command = message.content.lower()[2:]
    print(f"Handling command {command}")

    if command == 'select next':
        if message.author.id in main.admins:
            await processor.selection()
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response', message.channel)

    elif command == 'update pity':
        if message.author.id in main.admins:
            processor.update_pity()
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response', message.channel)

    elif command == 'next turn':
        if message.author.id in main.admins:
            lib.dump_data(main.turnLength, 'current_day', 'w', 'data.yml')
            await processor.next_turn()
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response', message.channel)

    elif command == 'end turn':
        currentIds = []
        for i in range(len(main.currentPlayer)):
            currentIds.append(main.players[main.currentPlayer[i]]['id'])
        if message.author.id in currentIds:
            await message.add_reaction('\U0001F44D')
            lib.dump_data(main.turnLength, 'current_day', 'w', 'data.yml')
            await processor.next_turn()
        else:
            await message.add_reaction('\U0001F44E')

    elif command == 'uploaded':
        pastId = main.players[main.pastPlayers]['id']
        if message.author.id == pastId:
            await message.add_reaction('\U0001F44D')
            lib.dump_data(True, 'upload_anti_spam', 'w', 'data.yml')
        else:
            await message.add_reaction('\U0001F44E')

    elif command == 'unavailable':
        messagedIds = []
        for i in range(len(main.messagedPlayer)):
            messagedIds.append(main.players[main.messagedPlayer[i]]['id'])
        if message.author.id in messagedIds:
            await message.add_reaction('\U0001F44D')
            idList = []
            playerNum = 100
            for i in range(len(main.players)):
                idList.append(main.players[i]['id'])
            for i in range(len(idList)):
                if idList[i] == message.author.id:
                    playerNum = [i]

            messagedPlayers = main.messagedPlayer
            messagedPlayers.remove(playerNum[0])
            lib.dump_data(messagedPlayers, 'messaged_player', 'w', 'data.yml')
            for i in range(len(main.unavailablePlayers)):
                playerNum.append(main.unavailablePlayers[i])
            lib.dump_data(playerNum, 'unavailable_players', 'w', 'data.yml')
            await processor.selection()
        else:
            await message.add_reaction('\U0001F44E')

    # Switches whether world changes by upload or whitelist
    elif command == 'change mode':
        if message.author.id in main.admins:
            if main.changeMode == 'upload':
                lib.dump_data('server', 'change_mode', 'w', 'data.yml')
                await lib.send_message('Mode changed to server', 'response', message.channel)
            else:
                lib.dump_data('upload', 'change_mode', 'w', 'data.yml')
                await lib.send_message('Mode changed to upload', 'response', message.channel)
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response',
                                    message.channel)

    # Responds with every player's pity
    elif command == 'pity':
        output = []
        for i in range(len(main.players)):
            output.append(str(main.players[i]['name']) + ": " + str(main.players[i]['pity']))
        output = ", ".join(output)
        await lib.send_message(output, 'response', message.channel)

    # Changes a player's pity using their 2-digit player number and a new pity
    elif command[:9] == 'set pity ':
        if message.author.id in main.admins:
            playerNum = int(command[9:11])
            newPity = int(command[12:])
            lib.dump_data(newPity, 'players', 'w', 'data.yml', dest2=playerNum, dest3='pity')
            await lib.send_message(f'Set pity of {main.players[playerNum]["name"]} to {newPity}', 'response', message.channel)
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response', message.channel)

    # Lists previous players
    elif command == 'past players':
        output = []
        for i in range(len(main.pastPlayers)):
            output.append(main.players[main.pastPlayers[i]]['name'])
        for i in range(len(main.currentPlayer)):
            output.append(f"**{main.players[main.currentPlayer[i]]['name']}**")
        output = ", ".join(output)
        await lib.send_message(output, 'response', message.channel)

    # Responds with the player(s) messaged by the bot and scheduled to go next
    elif command == 'who next':
        output = []
        if message.author.id in main.admins:
            for i in range(len(main.messagedPlayer)):
                output.append(main.players[main.messagedPlayer[i]]['name'])
            output = ", ".join(output)
            await lib.send_message(str(output), 'response', message.channel)
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response', message.channel)

    # Changes what day it is in terms of how long until the timer changes the turn
    elif command[:8] == 'set day ':
        if message.author.id in main.admins:
            output = int(command[8:])
            lib.dump_data(output, 'current_day', 'w', 'data.yml')
            await lib.send_message(f"Day changed to {output}", 'response', message.channel)
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response', message.channel)

    # Changes the amount of days in each turn
    elif command[:12] == 'turn length ':
        if message.author.id in main.admins:
            output = command[12:]
            lib.dump_data(output, 'turn_length', 'w', 'data.yml')
            await lib.send_message(f"Turn length changed to {output}", 'response', message.channel)
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response', message.channel)

    # Changes who is scheduled to join next. Could be a list of people, separated by commas
    elif command[:16] == 'set next player ':
        if message.author.id in main.admins:
            output = []
            midList = []
            finalList = []
            player = command[16:]
            for i in range(len(player)):
                if player[i].isnumeric():
                    midList.append(player[i])
                else:
                    finalList.append(int(''.join(midList)))
                    midList = []
            lib.dump_data(finalList, 'messaged_player', 'w', 'data.yml')
            for i in range(len(finalList)):
                output.append(str(main.players[int(finalList[i])]['name']))
            output = ', '.join(output)
            await lib.send_message(f'Next player(s) set to {output}', 'response', message.channel)
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response', message.channel)

    # Checks what day it is in terms of how close it is to having a new turn
    elif command == 'day':
        await lib.send_message('The next turn is starting ' + str(main.nextChange) + ' unless the turn is ended early', 'response', message.channel)

    # Sends a message as the bot
    elif command[:13] == 'send message ':
        if message.author.id in main.admins:
            string = command[13:]
            message = []
            destination = []
            sendType = []
            i = 0
            while string[i] != "-":
                message.append(string[i])
                i += 1
            i += 1
            while string[i] != "-":
                sendType.append(string[i])
                i += 1
            i += 1
            while i < len(string):
                destination.append(string[i])
                i += 1
            await lib.send_message("".join(message), "".join(sendType), "".join(destination))
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response',
                                        message.channel)

    elif command[:13] == 'player count ':
        if message.author.id in main.admins:
            lib.dump_data(int(command[13:]), 'player_count', 'w', 'data.yml')
            await lib.send_message(f"Player count changed to {command[13:]}", 'response', message.channel)
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response',
                                        message.channel)

    # Turns the timer on or off
    elif command[:6] == 'timer ':
        if message.author.id in main.admins:
            if command[6:] == "on":
                lib.dump_data(True, 'timer', 'w', 'data.yml')
                await lib.send_message("Timer turned on", 'response', message.channel)
            elif command[6:] == "off":
                lib.dump_data(False, 'timer', 'w', 'data.yml')
                await lib.send_message("Timer turned off", 'response', message.channel)
            else:
                await lib.send_message("Speak up, I couldn't tell if you said ON or OFF", 'response', message.channel)
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response',
                                   message.channel)

    # Attempts to dump data to a given point in the data
    # WARNING: not very good to use just modify the code lmao
    elif command[:5] == "dump ":
        if message.author.id in main.admins:
            mode = str(command[5])
            string = command[7:]
            data = []
            destination = []
            file = []
            dest2 = []
            dest3 = []
            i = 0
            while string[i] != "-":
                data.append(string[i])
                i += 1
            i += 1
            data = "".join(data)
            while string[i] != "-":
                destination.append(string[i])
                i += 1
            i += 1
            destination = "".join(destination)
            if "-" in string[i:]:
                while string[i] != "-":
                    file.append(string[i])
                    i += 1
                i += 1
                file = "".join(file)
                if "-" in string[i:]:
                    while string[i] != "-":
                        dest2.append(string[i])
                        i += 1
                    i += 1
                    dest2 = "".join(dest2)
                    if dest2.isnumeric():
                        dest2 = int(dest2)
                    while i < len(string):
                        dest3.append(string[i])
                        i += 1
                    dest3 = "".join(dest3)
                    lib.dump_data(data, destination, mode, file, dest2=dest2, dest3=dest3)
                    await lib.send_message(f"{data} dumped to [{destination}][{dest2}][{dest3}] of {file} in {mode} mode",
                                           'response', message.channel)
                else:
                    while i < len(string):
                        dest2.append(string[i])
                        i += 1
                        dest2 = "".join(dest2)
                    lib.dump_data(data, destination, mode, file, dest2=dest2)
                    await lib.send_message(f"{data} dumped to [{destination}][{dest2}] of {file} in {mode} mode",
                                           'response', message.channel)
            else:
                while i < len(string):
                    file.append(string[i])
                    i += 1
                i += 1
                file = "".join(file)
                print(data)
                print(destination)
                print(mode)
                print(file)
                lib.dump_data(data, destination, mode, file)
                await lib.send_message(f"{data} dumped to {destination} of {file} in {mode} mode", 'response', message.channel)
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response',
                                        message.channel)

    # Responds with what version the bot is running
    elif command == 'version':
        await lib.send_message(str(main.version), 'response', message.channel)

    #Updates global variables, mostly for testing
    elif command[:8] == 'refresh ':
        if message.author.id in main.admins:
            lib.refresh(command[8:])
            await lib.send_message(f'Refreshed from {command[8:]}', 'response', message.channel)
        else:
            await lib.send_message('Sorry, this command is unavailable due to a **skill issue**.', 'response',
                                    message.channel)

    # Lists every command NEEDS TO BE UPDATED
    elif command == 'help':
        await lib.send_message(f'__B2ot {main.version} Commands:__ \n'
                                    '**.?help** - Responds with this message \n'
                                    '**.?pity** - Responds with all pity scores \n'
                                    '**.?past players** - Responds with a list of all previous players, in order \n'
                                    "**.?day** - Checks how many days until a new cycle \n"
                                    '**.?unavailable** - Use if you are not available when the bot prompts you, makes sure your pity is not affected \n'
                                    '**.?uploaded** - Use after uploading the save file to the drive after the bot prompts you \n'
                                    '**.?end turn** - Ends a cycle early, passing the world to the next person \n'
                                    '**.?version** - See what version the bot is running \n'
                                    '**.?debug** - See admin/debug commands', 'response', message.channel)

    # Lists all admin commands NEEDS TO BE UPDATED
    elif command == 'debug':
        await lib.send_message(f'__B2ot {main.version} Admin Commands:__ \n'
                                    '**.?select next** - Select the next player(s) for the world \n'
                                    '**.?next turn** - Starts a new turn \n'
                                    '**.?update pity** - Changes pity as if there was a new turn without having a new turn \n'
                                    '**.?refresh** [data.yml/data file]- Refreshes global variables from data file \n'
                                    '**.?change mode** - Changes whether the world is an upload or server \n'
                                    '**.?turn length** [new length] - Change the amount of time per turn \n'
                                    '**.?timer** [on/off] - Turns the timer on or off \n'
                                    '**.?set day** [day number] - Changes how many days left in the turn \n'
                                    '**.?set pity** ## [new pity] - Change the pity of a player \n'
                                    '**.?who next** - Check who is currently selected \n'
                                    '**.?set next player** ##(,##,##,) - Change who is currently selected \n'
                                    '**.?player count** [amount of players] - Change how many players will be selected (ONLY ABOVE 1 IF IN SERVER MODE) \n'
                                    '**.?send message** [message]-[dm/channel]-[ID] - Send a message with the bot \n'
                                    '**.?dump** [mode] [data]-[destination]-[file](-[dest2]-[dest3]) - just dont use this tbh \n'
                                    '\n'
                                    "*##represents a player's 2 digit code, found in the order they are listed in the data file or in .?pity*", 'response',
                                    message.channel)

    else:
        await lib.send_message("Sorry, I don't know that command. Type .?help for help.", 'response',
                                    message.channel)
