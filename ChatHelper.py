async def send_to_sub_channels(session, client, message):
    for channel in session.channels:
        await client.send_message(channel, message)

async def send_to_user(client, destination, message):
    client.send_message(destination, message)