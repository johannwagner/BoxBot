import logging

import discord

import Security
from AsyncTask import AsyncTask
from Commands.CommandData import Command
from Commands.CommandHelper import say_toast, test, id_func, rate_limit, milestone, unsubscribe, subscribe, server, \
    loop_issues, loop_comments
from Session import Session

logger = logging.getLogger('BoxBot')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('BoxBot.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

logger.info('Hello baby')

commands = []

client = discord.Client()
session = Session(client, logger)


@client.event
async def on_ready():
    session.logger.info("Logged in !")
    session.logger.info(client.user.id)
    session.logger.info(client.user.name)

    if not str(153845852153184256) in session.user_manager_data.get('allowed_members'):
        session.user_manager_data['allowed_members'].append(str(153845852153184256))


@client.event
async def on_message(message: discord.Message):
    try:
        session.logger.info("Message from {sender}: {message}".format(sender = message.author.name, message=message.content).encode(encoding='UTF-8'))
    except:
        session.logger.info("Message from {sender}: Message was not logged.".format(sender =message.author.name))
    finally:
        for command in commands:
            await command.process_command(session, message)


def autosave_task():
    if session.loaded:
        session.save()


session.load()

autosave_session = AsyncTask(50)
autosave_session.task = autosave_task
autosave_session.start()

commands.append(Command(command="!toast", restricted=True, assigned_function=say_toast))
commands.append(Command(command="!test", restricted=True, assigned_function=test))
commands.append(Command(command="!id", restricted=False, assigned_function=id_func))
commands.append(Command(command="!ratelimit", restricted=True, assigned_function=rate_limit))
commands.append(Command(command="!milestone", restricted=False, assigned_function=milestone))
commands.append(Command(command="!subscribe", restricted=True, assigned_function=subscribe))
commands.append(Command(command="!unsubscribe", restricted=True, assigned_function=unsubscribe))
commands.append(Command(command="!server", restricted=True, assigned_function=server))

client.loop.create_task(loop_issues(session, None))
client.loop.create_task(loop_comments(session, None))

client.run(Security.DISCORD_TOKEN)
