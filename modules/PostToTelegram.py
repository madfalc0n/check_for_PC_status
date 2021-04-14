"""
telegram bot
pip install python-telegram-bot
"""
import telegram

class telegram_bot:
    def __init__(self, token=None):
        self.token = token
        self.bot = telegram.Bot(token=token)

    def post_telegram(self, user_id='None', msg='set msg'):
        # chat_id = "1769218456"
        self.bot.sendMessage(chat_id = user_id , text=msg)

    def receive_msg(self):
        updates = self.bot.get_updates()
        # print(updates)
        user_dict = dict()
        for user_info in updates:
            # print(user_info)
            # print(len(user_info))
            user_id = user_info.message['chat']['id']
            user_name = user_info.message['chat']['first_name']
            text = user_info.message['text'] 
            user_dict[user_id] = user_dict.get(user_id,[[user_name],[]])
            # user_dict[user_id][1] += [text]
            user_dict[user_id][1] = [text]
            # print(user_dict)   
        return user_dict

    def send_location(self, user_id='None'):
        latitude = 37.4981
        longitude = 126.953089
        # chat_id = "1769218456"
        # user_id = chat_id
        self.bot.sendLocation(user_id, latitude, longitude, 
                        disable_notification = True)

    def send_photo(self, image='None', user_id='None'):
        chat_id = "1769218456"
        user_id = chat_id
        self.bot.sendPhoto(user_id, open(image, 'rb'))


if __name__ == "__main__":
    tb = telegram_bot(token='1750354982:AAEnceNQ8u_8IBLDXbdEr4RDEXc1Nie0I64')
    print(tb.receive_msg())
    # print(tb.send_location())
    # file = 'log_pic/2021414155145_initializing_img.jpg'
    # print(tb.send_photo(image=file))