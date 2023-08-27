import asyncio
import main
import processor
import lib
from datetime import datetime


async def run_timer():
    while True:
        await asyncio.sleep(20)
        time = datetime.now()
        if time.hour == 16 and not main.timerAntiSpam and main.timerTF:
            if main.currentDay == 1:
                lib.dump_data(main.turnLength, 'current_day', 'w', 'data.yml')

                await processor.next_turn()
            else:
                main.currentDay -= 1
                lib.dump_data(main.currentDay, 'current_day', 'w', 'data.yml')
            lib.dump_data(True, 'timer_anti_spam', 'w', 'data.yml')
        elif time.hour != 16 and main.timerAntiSpam:
            lib.dump_data(False, 'timer_anti_spam', 'w', 'data.yml')
