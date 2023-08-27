import yaml
import main


# Message = message to respond with (from responses.[]handler)
# sendType = decides where to send message by varying how ID is used
# ID = user id if sendType of dm, channel id if sendType of channel, message.channel if sendType of response
async def send_message(message, sendType, ID):
    if sendType == "dm":
        sendLocation = await main.client.fetch_user(ID)
        await sendLocation.send(message)
        print(f"Sending message |{message}| by {sendType} to {str(sendLocation)}")
    elif sendType == "channel":
        sendLocation = await main.client.fetch_channel(ID)
        await sendLocation.send(message)
        print(f"Sending message |{message}| by {sendType} to {str(sendLocation)}")
    elif sendType == "response":
        sendLocation = ID
        await sendLocation.send(message)
        print(f"Sending message |{message}| by {sendType} to {str(sendLocation)}")


# Used in the exact same way as send_message but instead only prints to logs for testing
async def fake_message(message, sendType, ID):
    if sendType == "dm":
        sendLocation = await main.client.fetch_user(ID)
        print(f"NOT Sending message |{message}| by {sendType} to {str(sendLocation)}")
    elif sendType == "channel":
        sendLocation = await main.client.fetch_channel(ID)
        print(f"NOT Sending message |{message}| by {sendType} to {str(sendLocation)}")
    elif sendType == "response":
        sendLocation = ID
        print(f"NOT Sending message |{message}| by {sendType} to {str(sendLocation)}")


# To dump data by writing outside of function:
# f = open('data.yml', 'r')
# data = yaml.safe_load(f)
# data[destination] = new_values
# f = open(file, 'w')
# yaml.dump(data, f, sort_keys=False)

# To dump data by appending outside of function:
# f = open('data.yml', 'r')
# data = yaml.safe_load(f)
# data[destination].append(new_values)
# f = open(file, 'a')
# yaml.dump(data, f, sort_keys=False)


# Function to write data to storage
# Only use dest2 and dest3 for nested lists
def dump_data(values, destination, mode, file, dest2=None, dest3=None):
    f = open(file, "r")
    data = (yaml.safe_load(f))
    if dest3 is not None and dest2 is not None:
        if mode == 'w':
            data[destination][dest2][dest3] = values
        if mode == 'a':
            data[destination][dest2][dest3].append(values)
        f = open(file, 'w')
        yaml.dump(data, f, sort_keys=False)

    elif dest2 is not None and dest3 is None:
        if mode == 'w':
            data[destination][dest2] = values
        if mode == 'a':
            data[destination][dest2].append(values)
        f = open(file, 'w')
        yaml.dump(data, f, sort_keys=False)

    elif dest2 is None and dest3 is None:
        if mode == 'w':
            data[destination] = values
        if mode == 'a':
            data[destination].append(values)
        f = open(file, 'w')
        yaml.dump(data, f, sort_keys=False)

    # Reread global variables
    refresh(file)

# Some example calls:
# add clock as an admin:
# lib.dump_data(442388594330697728, 'admins', 'a', 'data.yml')
# Add echo as a player
# lib.dump_data({15: 'Echo', 'name': 'Echo', 'pity': 0, 'id': 321}, 'players', 'a', 'data.yml')
# Set audery's pity to 420
# lib.dump_data(420, 'players', 'w', 'data.yml', dest2=2, dest3='pity')


def refresh(file):
    f = open(file, "r")
    data = (yaml.safe_load(f))
    main.token = data['token']
    main.admins = data['admins']
    main.mainChannel = data['main_channel']
    main.role = data['role']
    main.players = data['players']
    main.turnLength = int(data['turn_length'])
    main.currentDay = int(data['current_day'])
    main.timerTF = data['timer']
    main.uploadAntiSpam = data['upload_anti_spam']
    main.timerAntiSpam = data['timer_anti_spam']
    main.changeMode = data['change_mode']
    main.playerCount = data['player_count']
    main.messagedPlayer = data['messaged_player']
    main.unavailablePlayers = data['unavailable_players']
    main.currentPlayer = data['current_player']
    main.version = data['version']
    main.driveLink = data['drive_link']
    main.serverIp = data['server_ip']
    main.pastPlayers = data['past_players']
    main.rechargeTime = data['recharge_turns']
    main.nextChange = data['next_change']
