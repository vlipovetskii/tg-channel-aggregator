import asyncio
import logging
import os
from telethon import TelegramClient, events
import tg_channel_openai
from tg_channel_aggregator_env_variables import TLG_SESSION_NAME, TLG_API_ID, TLG_API_HASH, TLG_TARGET_CHAT_ID, \
    TLG_CHANNELS, TLG_PHONE_NUMBER

# import tg_channel_stop_words

# Set up logger with date and time format
logging.basicConfig(
    format='%(asctime)s - %(message)s',  # Include date/time in log message
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'  # Specify date/time format (e.g., 2025-03-14 14:45:30)
)
logger = logging.getLogger("tg_channel_aggregator")

# with stop words
# tg_channel_stop_words.log_env_variables(logger)

# with Open AI
tg_channel_openai.log_env_variables(logger)

# Create Telegram client (logs in as you)
# --- Telethon - change session file path https://stackoverflow.com/questions/67605930/telethon-change-session-file-path
client = TelegramClient(TLG_SESSION_NAME, TLG_API_ID, TLG_API_HASH)


# @filter_stop_words(logger, STOP_WORDS)
@tg_channel_openai.filter_openai(logger)
async def forward_message(event):
    """Forwards messages to the target chat using the user's own session."""
    # sender = await event.get_sender()
    chat = await event.get_chat()

    # Construct message link
    if chat.username:
        message_link = f"https://t.me/{chat.username}/{event.message.id}"
    else:
        message_link = f"https://t.me/c/{chat.id}/{event.message.id}"

    """
    --- Telegram accepts standard Markdown text formatting: https://stackoverflow.com/a/61816537
    
    """
    message_text = f"📢 **{chat.title}** [🔗]({message_link})\n\n{event.text}"

    try:
        entity = await client.get_entity(int(TLG_TARGET_CHAT_ID))
        await client.send_message(entity, message_text, parse_mode="md")
        logger.info(f"Forwarded message: '{event.text[:10]}' from {chat.title}")
    except Exception as e:
        logger.error(f"Failed to forward message: {e}")


@client.on(events.NewMessage(chats=TLG_CHANNELS))
async def handler(event):
    await forward_message(event)


async def main():
    """Start listening for messages."""
    logger.info("Starting tg-channel-aggregator..")

    # await client.start()
    if os.path.exists(TLG_SESSION_NAME):
        await client.connect()  # Connect to Telegram
    else:
        client.start(phone=TLG_PHONE_NUMBER)  # Only request phone number if session is missing
        await client.disconnect()
        await client.connect()  # Reconnect using saved session

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
