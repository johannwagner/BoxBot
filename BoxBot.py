import dateutil.parser
import asyncio
import datetime
import logging

import discord
import requests

import ChatHelper
import Requester
import Security
from AsyncTask import AsyncTask
from Session import Session

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



client = discord.Client()
session = Session(logger)


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
            print("Iterating over Issue " + str(issue.get('number')))
            closed = issue.get('closed_at')
            if closed is None:
                if issue.get('id') not in session.open_issues:
                    session.open_issues.append(issue.get('id'))
                    await ChatHelper.send_to_sub_channels(session, client,
                                                          " :question: **{user} created Issue #{number}:**  `{title}` \n GitHub: {html_url}"
                                                          .format(user=issue.get('user').get('login'),
                                                                  number=issue.get('number'), title=issue.get('title'),
                                                                  html_url=issue.get('html_url')))
            else:
                closed_time = dateutil.parser.parse(closed)

                if session.last_request_time > closed_time and issue.get('id') not in session.closed_issues:
                    session.closed_issues.append(issue.get('id'))
                    await ChatHelper.send_to_sub_channels(session, client,
                                                          " :white_check_mark: **Issue #{number} closed:**  `{title}` "
                                                          .format(number=issue.get('number'), title=issue.get('title')))

        session.last_request_time = datetime.datetime.now(datetime.timezone.utc)
        await asyncio.sleep(60)  # task runs every 30 seconds


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!subscribe'):
        session.channels.append(message.channel)
        await client.send_message(message.channel, 'This channel was added to channel list.')
    elif message.content.startswith('!unsubscribe'):

        if message.channel in session.channels:
            session.channels.remove(message.channel)
        await client.send_message(message.channel, 'This channel was removed to channel list.')
    elif message.content.startswith('!heartbeat'):
        await client.send_message(message.channel, 'The Box is alive.')
    elif message.content.startswith('!ratelimit'):
        await client.send_message(message.channel, Requester.get_rate_limit())
    elif message.content.startswith('!milestone'):
        milestones = Requester.get_milestone_stats()
        for milestone in milestones:
            await client.send_message(message.channel, '**Milestone {title}:** {closed}/{all} - {percent}%'
                                      .format(title=milestone['title'], closed=milestone['closed'],
                                              all=milestone['all'],
                                              percent=milestone['percentage']))


    elif message.content.startswith('!test'):
        if 216566139 in session.closed_issues:
            session.closed_issues.remove(216566139)
        if 216597554 in session.open_issues:
            session.open_issues.remove(216597554)

def autosave_task():
    if session.loaded:
        session.save()


session.load()

autosave_session = AsyncTask(50)
autosave_session.task = autosave_task
autosave_session.start()

client.loop.create_task(pull_github())
client.run(Security.DISCORD_TOKEN)
