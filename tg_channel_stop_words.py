from functools import wraps
import os

"""
PRB: ['\nKр птой', '\nhas been kicked', '\n']
WO: .strip() removes leading and trailing whitespace (including \n).
"""
STOP_WORDS = [word.strip() for word in os.getenv("STOP_WORDS", "").split(",") if word.strip()]


def log_env_variables(logger):
    logger.info(f"STOP_WORDS: {STOP_WORDS}")


def filter_stop_words(logger):
    def decorator(func):
        @wraps(func)
        async def wrapper(event):
            if not any(word in event.text for word in STOP_WORDS):
                return await func(event)
            else:
                logger.info(f"Blocked event: contains a stop word.")
                return

        return wrapper

    return decorator
