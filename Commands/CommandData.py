import discord

import Session
import UserManager


class Command:
    assigned_function = None
    command = None
    restricted = None

    def __init__(self, command: str, restricted: bool, assigned_function):
        self.command = command
        self.restricted = restricted
        self.assigned_function = assigned_function



    async def process_command(self, session: Session, message: discord.Message):

        user_manager = session.user_manager
        if not message.content.startswith(self.command) or message.author == session.client.user:
            return

        user_allow = await user_manager.is_user_allowed(channel=message.channel, member=message.author)

        if (not self.restricted) or (self.restricted and user_allow):
            session.logger.info("User {user} issued {command}.".format(user = message.author.name, command = self.command))
            await self.assigned_function(session, message)
        else:
            session.logger.info("User {user} issued {command} and was not allowed.".format(user = message.author.name, command = self.command))
            await session.client.send_message(message.channel, "**You are not allowed to this!**")

