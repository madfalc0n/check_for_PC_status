"""
telegram bot
pip install python-telegram-bot
"""
import telegram

class telegram_bot:
    def __init__(self, token=None):
        self.token = token
        self.bot = telegram.Bot(token=token)

    def post_telegram(self,msg='set msg'):
        chat_id = "1769218456"
        self.bot.sendMessage(chat_id = chat_id , text=msg)

    def receive_msg(self):
        updates = self.bot.get_updates()
        # test = self.bot.Update()
        # print(updates)
        user_dict = dict()
        for user_info in updates:
            # print(user_info)
            user_id = user_info.message['chat']['id']
            user_name = user_info.message['chat']['first_name']
            text = user_info.message['text'] 
            user_dict[user_id] = user_dict.get(user_id,[[user_name],[]])
            # user_dict[user_id][1] += [text]
            user_dict[user_id][1] = [text]
            # print(user_dict)   
        return user_dict 

if __name__ == "__main__":
    tb = telegram_bot(token='1661842188:AAHmsUmjJKzZj_SFaLQ5gGBzQwL-cTsfD50')
    tb.receive_msg()