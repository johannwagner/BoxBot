import dateutil.parser
import asyncio
import datetime
import logging

import discord
import requests

import ChatHelper
import Security
from AsyncTask import AsyncTask
from Commands.CommandData import Command
from Commands.CommandHelper import say_toast, test, id_func, rate_limit, milestone, unsubscribe, subscribe, server
from Session import Session

import logging

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


async def pull_github():
    await client.wait_until_ready()
    await asyncio.sleep(5)

    while not client.is_closed:
        request = requests.get("https://api.github.com/repos/hovgaardgames/startupcompany/issues",
                               params={"state": "all",
                                       "client_id": "6155522b016d8c49ce3a",
                                       "client_secret": "75d08f6977075855c730a406e93c96774a386769",
                                       "per_page": 100})
        json = request.json()

        for issue in json:
            closed = issue.get('closed_at')
            if closed is None:
                if issue.get('id') not in session.open_issues:
                    session.logger.info("Added {id} to open_issue".format(id = issue.get('id')))
                    session.open_issues.append(issue.get('id'))
                    await ChatHelper.send_to_sub_channels(session, client,
                                                          " :question: **{user} created Issue #{number}:**  `{title}` \n GitHub: {html_url}"
                                                          .format(user=issue.get('user').get('login'),
                                                                  number=issue.get('number'), title=issue.get('title'),
                                                                  html_url=issue.get('html_url')))
            else:
                closed_time = dateutil.parser.parse(closed)

                if session.last_request_time > closed_time and issue.get('id') not in session.closed_issues:
                    session.logger.info("Added {id} to closed_issue".format(id=issue.get('id')))
                    session.closed_issues.append(issue.get('id'))
                    await ChatHelper.send_to_sub_channels(session, client,
                                                          " :white_check_mark: **Issue #{number} closed:**  `{title}` "
                                                          .format(number=issue.get('number'), title=issue.get('title')))

        session.last_request_time = datetime.datetime.now(datetime.timezone.utc)
        await asyncio.sleep(60)  # task runs every 30 seconds


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
commands.append(Command(command="!subscribe", restricted=False, assigned_function=subscribe))
commands.append(Command(command="!unsubscribe", restricted=False, assigned_function=unsubscribe))
commands.append(Command(command="!server", restricted=False, assigned_function=server))

client.loop.create_task(pull_github())
client.run(Security.DISCORD_TOKEN)
