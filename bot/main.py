import yaml
import bot

# Open config
f = open("data.yml", "r")
data = (yaml.safe_load(f))

# Set global variables
token = data['token']
admins = data['admins']
mainChannel = data['main_channel']
role = data['role']
players = data['players']
turnLength = int(data['turn_length'])
currentDay = int(data['current_day'])
timerTF = data['timer']
changeMode = data['change_mode']
playerCount = data['player_count']
unavailablePlayers = data['unavailable_players']
messagedPlayer = data['messaged_player']
currentPlayer = data['current_player']
version = data['version']
driveLink = data['drive_link']
serverIp = data['server_ip']
uploadAntiSpam = data['upload_anti_spam']
timerAntiSpam = data['timer_anti_spam']
pastPlayers = data['past_players']
rechargeTime = data['recharge_turns']
nextChange = data['next_change']

# Run the bot
if __name__ == '__main__':
    global client
    bot.run_discord_bot()
