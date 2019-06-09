from pymessenger.bot import Bot


def send_message(page_access_token: str, recipient_id: str, message: str):
    bot = Bot(page_access_token)
    bot.send_text_message(recipient_id, message)
