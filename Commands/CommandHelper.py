import asyncio
import datetime

import dateutil.parser
import discord
import requests

import Requester
import Security
import Session


async def loop_issues(session: Session, message: discord.Message):
    client = session.client

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
                    session.logger.info("Added {id} to open_issue.".format(id=issue.get('id')))
                    session.open_issues.append(issue.get('id'))
                    await session.chat_manager.send_message(
                        " :question: **{user} created Issue #{number}:**  `{title}` \n GitHub: {html_url}"
                            .format(user=issue.get('user').get('login'), number=issue.get('number'),
                                    title=issue.get('title'), html_url=issue.get('html_url')), 'issues')

            else:
                closed_time = dateutil.parser.parse(closed)

                if session.last_request_time > closed_time and issue.get('id') not in session.closed_issues:
                    session.logger.info("Added {id} to closed_issue.".format(id=issue.get('id')))
                    session.closed_issues.append(issue.get('id'))
                    await session.chat_manager.send_message(
                        " :white_check_mark: **Issue #{number} closed:**  `{title}` "
                            .format(number=issue.get('number'), title=issue.get('title')), 'issues')

        session.last_request_time = datetime.datetime.now(datetime.timezone.utc)
        await asyncio.sleep(60)


async def loop_comments(session: Session, message: discord.Message):
    client = session.client

    await client.wait_until_ready()
    await asyncio.sleep(5)

    while not client.is_closed:
        comments = Requester.get_comment_stats()

        for comment in comments:
            if comment.get('id') not in session.comments:
                session.comments.append(comment.get('id'))
                session.logger.info('Added {id} to comments.'.format(id=comment.get('id')))
                user = comment.get('user')
                url = str(comment.get('html_url'))
                issue = url[url.rfind('/') + 1:url.rfind('#')]
                await session.chat_manager.send_message(':bell: **{user} commented on Issue #{issue}.** \n GitHub: {html_url}'
                                                  .format(user=user.get('login'), issue=issue,
                                                          html_url=comment.get('html_url')), 'comments')

        await asyncio.sleep(60)


async def subscribe(session: Session, message: discord.Message):
    params = message.content.split(" ")
    ident = params[1] if len(params) >= 2 else None

    if ident is not None:
        session.chat_manager.add_channel(message.channel, ident)
        await session.client.send_message(message.channel, 'You subscribed to {ident} list.'.format(ident=ident))
    else:
        await session.client.send_message(message.channel, 'You have to specify a channel identifier.')


async def unsubscribe(session: Session, message: discord.Message):
    params = message.content.split(" ")

    ident = params[1] if len(params) >= 2 else None

    if ident is not None:
        session.chat_manager.remove_channel(message.channel, ident)
        await session.client.send_message(message.channel, 'You unsubscribed from {ident} list.'.format(ident=ident))
    else:
        await session.client.send_message(message.channel, 'You have to specify a channel identifier.')


async def say_toast(session: Session, message: discord.Message):
    client = session.client
    await client.send_message(message.channel, "**I <3 Toast**")


async def rate_limit(session: Session, message: discord.Message):
    rate_limit_result = Requester.get_rate_limit()

    await session.client.send_message(message.author, '**Requests:** {acutal}/{all}'
                                      .format(acutal=rate_limit_result.get('actual'), all=rate_limit_result.get('all')))


async def milestone(session: Session, message: discord.Message):
    milestones = Requester.get_milestone_stats()
    for milestone in milestones:
        await session.client.send_message(message.channel, '**Milestone {title}:** {closed}/{all} - {percent}%'
                                          .format(title=milestone['title'], closed=milestone['closed'],
                                                  all=milestone['all'],
                                                  percent=round(milestone['percentage'], 2)))


async def server(session: Session, message: discord.Message):
    await session.client.send_message(message.channel, "**Server:** {pos}"
                                      .format(pos="Server" if Security.SERVER is None or Security.SERVER else "Local"))


async def id_func(session: Session, message: discord.Message):
    await session.client.send_message(message.author, "** Your User ID is:** `{id}`".format(id=message.author.id))


async def test(session: Session, message: discord.Message):
    if 216566139 in session.closed_issues:
        session.closed_issues.remove(216566139)
    if 216597554 in session.open_issues:
        session.open_issues.remove(216597554)
    if 289068683 in session.comments:
        session.comments.remove(289068683)
