import os
from functools import wraps

from openai import AsyncOpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_QUESTION = os.getenv("OPENAI_QUESTION")
OPENAI_QUESTION_FORM = "Answer only with 'true' or 'false'"


def log_env_variables(logger):
    logger.info(
        f"OPENAI_MODEL: {OPENAI_MODEL}\n OPENAI_QUESTION: {OPENAI_QUESTION}\n OPENAI_QUESTION_FORM: {OPENAI_QUESTION_FORM}")


async def get_openai_response(api_key, model, question, question_form, prompt):
    # AsyncOpenAI() gets api_key from OPENAI_API_KEY env variable implicitly
    # client = AsyncOpenAI()
    # OR explicitly
    openai_client = AsyncOpenAI(
        # This is the default and can be omitted
        api_key=api_key
    )

    response = await openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": f"{question} {question_form}\n{prompt}"}],
        temperature=0,  # Ensures a deterministic response
        max_tokens=10
    )

    answer = response.choices[0].message.content.strip().lower()

    return answer in ["yes", "true"]


def filter_openai(logger):
    def decorator(func):
        @wraps(func)
        async def wrapper(event):

            ok = (not event.text or event.text.isspace()) \
                 or await get_openai_response(OPENAI_API_KEY, OPENAI_MODEL, OPENAI_QUESTION, OPENAI_QUESTION_FORM,
                                              prompt=event.text)
            if ok:
                return await func(event)
            else:
                logger.info(f"Blocked event:\n '{event.text}'\n recognized as a spam.")
                return

        return wrapper

    return decorator
