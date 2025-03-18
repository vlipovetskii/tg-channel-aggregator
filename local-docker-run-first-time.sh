source "./util.sh"

# 2. First-time Login (User Authorization)
# When you run this script for the first time, Telethon will ask for your phone number and send you a login code via Telegram.

# --- The Interactive and TTY Options in docker run https://www.baeldung.com/linux/docker-run-interactive-tty-options

# --- Signing In to Telegram Client with Telethon automatically (python) https://stackoverflow.com/questions/64155483/signing-in-to-telegram-client-with-telethon-automatically-python

#  --env-file		Read in a file of environment variables

docker run --env-file ./.env -v ./session:/app/session -it tg-channel-aggregator

# Enter your phone number → Enter the login code.
# ✔ After logging in once, Telethon saves your session (session/session.session file), so you won't need to log in again.

ok_exit_w