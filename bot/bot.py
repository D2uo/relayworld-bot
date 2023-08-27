import discord
import asyncio
import timer
import main
import responses


# Called by main function on bot start
def run_discord_bot():
    main.client = discord.Client(intents=discord.Intents.all())

    # Provides logs that the bot has started
    @main.client.event
    async def on_ready():
        print(f'{main.client.user} version {main.version} is now running!')

    # Activate functions on message
    @main.client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == main.client.user:
            return

        # Checks if it has prefix for command, and if so, tosses to command handler
        if message.content[0:2] == ".?":
            await responses.handle_command(message)

    # Waits a split second for timer to start, then begins bot
    async def clientRunner():
        await asyncio.sleep(0.001)
        await main.client.start(main.token)

    # Starts timer
    async def timerRunner():
        f1 = loop.create_task(timer.run_timer())
        f2 = loop.create_task(clientRunner())
        await asyncio.wait([f1, f2])

    # Loops everything so the bot runs constantly
    loop = asyncio.get_event_loop()
    loop.run_until_complete(timerRunner())
    loop.close()
