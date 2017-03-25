import discord

import ChatManager
import Session


class UserManager:
    session = None
    client = None
    server = None

    def __init__(self, client: discord.Client, session: Session):
        self.session = session
        self.client = client

        if self.session.user_manager_data.get('allowed_members') is None:
            self.session.user_manager_data['allowed_members'] = []

    async def is_user_allowed(self, member: discord.Member, channel: discord.Channel) -> bool:

        allowed_members = self.session.user_manager_data.get('allowed_members')

        channel_permission = member.permissions_in(channel)
        if channel_permission.administrator or (member.id in allowed_members):
            return True
        else:
            return False

    def add_allowed_user(self, id: int):
        for server in self.client.servers:
            member = server.get_member(id)
            if member is not None:
                self.session.user_manager_data['allowed_members'].append(member)
