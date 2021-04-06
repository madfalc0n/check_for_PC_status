from modules.CheckPowerStatus import get_power_status
from modules.PostToSlack import post_slack
from modules.test_telegram import telegram_bot
import time

def main_process(mode=1):
    """
    mode 0 : Slack communication
    mode 1 : Telegram communication
    """
    count = 1
    while 1:
        if count == 5:
            break
        PC_status = get_power_status()
        print(PC_status)

        if PC_status['ACLineStatus']:
            Battery_connected = 'ON'
        else:
            Battery_connected = 'OFF'

        if PC_status['windowlocked']:
            window_status = 'OFFLINE'
        else:
            window_status = 'ONLINE'
        
        text_form = f"POWER Line Status : {Battery_connected} \nWindow Locked : {window_status}"
        

        if mode == 0: ##Slack 
            url = 'YOUR SLACK WORKSPACE URL'
            slack_post_result = post_slack(url,text_form)
            print(slack_post_result)
        elif mode == 1: ##Telegram
            token = 'YOUR TELEGRAM BOT TOKEN'
            tb = telegram_bot(token)
            tb.post_telegram(text_form)

        count += 1
        time.sleep(40)


if __name__ == "__main__":
    print("----------------------------")
    print("CHECK YOUR PC STATUS")
    print("----------------------------")
    main_process(mode=1)