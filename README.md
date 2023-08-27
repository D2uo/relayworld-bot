# relayworld-bot
Discord bot for the Minecraft gamemode Relayworld


D2uo's relayworld bot version 2.1.3

What is relayworld?
Relayworld is a gamemode for Minecraft where friends share a singleplayer world. The file gets passed between people based on who hasn't had it recently, as well as a little bit of luck.

How does it work?
This is a hard question to answer, since it is highly configurable. To start it, someone with admin permissions for the bot run '.?next turn' twice. The first time it will message someone asking if they are available for the next turn. The second time it will start and give them the world. It messages a new player to ask if they are available for the next turn as soon as a turn is started to give them time to respond with '.?unavailable' so they can keep their pity score. After a set number of days, if you have the timer on (default), it will pass the world to the next person. It will also do this if the current player runs '.?end turn'.

How does it pick someone?
Every time the world is passed, it generates pity for someone. If they don't have the players role, it keeps it at whatever it was before. If they have had the world in the past few turns, it sets it to 0. Otherwise, it follows current_pity * (1 + (random decimal 0-1)) + (random number 1-3). Then, when the bot selects a new player, it is a random choice with each player's weight in the choice being their pity.

That sounds awesome! How do I set it up?
Download the 'bot' folder and edit anything with a comment in data.yml. When it references ID's, copy and paste discord ID's for users, roles, or channels depending on what it is asking. Create a bot in the discord developer portal and paste in the token. Then follow the steps necessary to host it, making sure you have the requirements for discord, discord.py, and PyYAML satisfied. I used discloud for this, so if you want to do the same, paste the files from the file 'discloud' into the main bot. If you want to do something else, feel free to delete this file.

Is anything else planned?
Yeah, configuring the time that the bot works. Right now it's set to 16, so if you want to change that go into timer.py and change everywhere it says 16. This is a simple thing I though I already did, but I don't have the time to do it right now.
