import os

# Load environment variables
TLG_API_ID = int(os.getenv("TLG_API_ID"))
TLG_API_HASH = os.getenv("TLG_API_HASH")
# --- Telethon - change session file path https://stackoverflow.com/questions/67605930/telethon-change-session-file-path
# In general, when creating TelegramClient object - pass it the full path to session file
# client = TelegramClient('path/to/session.session',api_id,app_hash)
# I test it working without the .session extension e.g: client = TelegramClient('path/to/session',api_id,app_hash)
TLG_SESSION_NAME = "session/session.session"
TLG_PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# Target channel/group to send messages
TLG_TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

# List of source channels
TLG_CHANNELS = os.getenv("CHANNELS", "").split(",")
