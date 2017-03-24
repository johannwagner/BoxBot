import discord

import Requester
import Session


async def subscribe(session: Session, message: discord.Message):
    session.channels.append(message.channel)
    await session.client.send_message(message.channel, 'This channel was added to channel list.')

async def unsubscribe(session: Session, message: discord.Message):
    if message.channel in session.channels:
        session.channels.remove(message.channel)
    await session.client.send_message(message.channel, 'This channel was removed from channel list.')

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


async def id_func(session: Session, message: discord.Message):
    await session.client.send_message(message.author, "** Your User ID is:** `{id}`".format(id=message.author.id))




async def test(session: Session, message: discord.Message):
    if 216566139 in session.closed_issues:
        session.closed_issues.remove(216566139)
    if 216597554 in session.open_issues:
        session.open_issues.remove(216597554)
