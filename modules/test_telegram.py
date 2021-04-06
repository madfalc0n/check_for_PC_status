"""
telegram bot
pip install python-telegram-bot
"""
import telegram


class telegram_bot:
    def __init__(self, token=None):
        assert token is not None, "set Bot token value"
        self.token = token

        self.bot = telegram.Bot(token=token)

    def post_telegram(self,msg='set msg'):
        chat_id = "1769218456"
        self.bot.sendMessage(chat_id = chat_id , text=msg)

    def receive_msg(self):
        updates = self.bot.get_updates()
        for u in updates:
            # print(u)
            print(u.message['chat']['id'])
            print(u.message['text'])