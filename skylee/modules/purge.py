import time
from skylee import dispatcher, LOGGER, SUDO_USERS, TELETHON_ID, TELETHON_HASH

from telethon import events
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins

api_id = TELETHON_ID
api_hash = TELETHON_HASH
client = TelegramClient('skylee', api_id, api_hash)

# Check if user has admin rights
async def is_administrator(user_id: int, message):
    status = False
    async for user in client.iter_participants(message.chat_id,
                             filter=ChannelParticipantsAdmins):
        if user_id == user.id or user_id in SUDO_USERS:
            status = True
            break
    return status


@client.on(events.NewMessage(pattern='/purge'))
async def purge(event):
        chat = event.chat_id

        if not await is_administrator(user_id=event.from_id, message=event):
           await event.reply("You're not an admin!")
           return

        msg = await event.get_reply_message()
        if not msg:
           await event.reply("Reply to a message to select where to start purging from.")

        msgs = []
        msg_id = msg.id
        to_delete = event.message.id - 1
        await event.client.delete_messages(chat, event.message.id)

        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            if len(msgs) == 100:
               await event.client.delete_messages(chat, msgs)
               msgs = []

        await event.client.delete_messages(chat, msgs)
        text = "Flash purge complete!"
        await event.respond(text, parse_mode='md')


@client.on(events.NewMessage(pattern="^/del$"))
async def delet(event):

    if not await is_administrator(user_id=event.from_id, message=event):
        await event.reply("You're not an admin!")
        return

    chat = event.chat_id
    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to some message to delete it.")
        return
    to_delete = event.message
    chat = await event.get_input_chat()
    rm = [msg, to_delete]
    await event.client.delete_messages(chat, rm)



__help__ = """
Deleting messages made easy with this command. Bot purges \
messages all together or individually.

*Admin only:*
 × /del: Deletes the message you replied to
 × /purge: Deletes all messages between this and the replied to message.
"""

__mod_name__ = "Purges"
