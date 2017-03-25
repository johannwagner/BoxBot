import discord

import Session


class ChatManager:
    session = None

    def __init__(self, session: Session):
        self.session = session

    def add_channel(self, channel: discord.Channel, ident: str):
        if ident in self.session.chat_manager_data:
            self.session.chat_manager_data[ident].append(channel)
        else:
            self.session.chat_manager_data[ident] = [channel]

    def remove_channel(self, channel: discord.Channel, ident: str):
        if ident in self.session.chat_manager_data and channel in self.session.chat_manager_data[ident]:
            self.session.chat_manager_data[ident].pop(self.session.chat_manager_data[ident].index(channel))

            if not self.session.chat_manager_data[ident]:
                self.session.chat_manager_data.pop(ident)

    async def send_message(self, message: str, ident: str):
        channels = self.session.chat_manager_data.get(ident)

        if channels is not None:
            for channel in channels:
                await self.session.client.send_message(channel, message)
