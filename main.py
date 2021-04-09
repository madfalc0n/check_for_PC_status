# from modules.CheckPowerStatus import get_power_status
from modules.CheckPowerStatus_psutil import get_power_status
from modules.PostToSlack import post_slack
from modules.PostToTelegram import telegram_bot
from modules.SaveCam import capture
import time
import cv2
from threading import Thread
import argparse

def check_HW_status(mode=1):
    PC_status = get_power_status()
    if mode == -1: # initalizing(test)
        # print(PC_status)
        for key, val in PC_status.items():
            print(f"----->{key} : {val}")

    if PC_status['ACLineStatus']:
        Battery_connected = 'ON'
    else:
        Battery_connected = 'OFF'

    if PC_status['windowlocked']:
        window_status = 'OFFLINE'
    else:
        window_status = 'ONLINE'
        
    text_form = f"POWER Line Status : {Battery_connected} \nWindow Locked : {window_status}"
    return text_form

def post_process(mode=1,token=None,url=None,text_form=None):
    """
    mode 0 : Slack communication
    mode 1 : Telegram communication
    """
    
    if mode == 0: ##Slack 
        # url = 'YOUR SLACK WORKSPACE URL'
        slack_post_result = post_slack(url,text_form)
        # print(slack_post_result)
    
    elif mode == 1: ##Telegram
        # token = 'YOUR TELEGRAM BOT TOKEN'
        tb = telegram_bot(token)
        tb.post_telegram(text_form)

    elif mode == -1: ##initializing TEST
        initializing_text = "---INITIALIZING TEST MODE---\n"
        tb = telegram_bot(token)
        tb.post_telegram(initializing_text + text_form)
        user_info = tb.receive_msg()
        print(f"----->Current User Count : {len(user_info)}")


if __name__ == "__main__":
    #main.py 실행시 옵션을 설정할 수 있도록 argparse 객체 지정 
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=int, default=1, 
                        help='choice using "telegram" or "slack"')
    parser.add_argument('-t', '--token', type=str, default='1661842188:AAHmsUmjJKzZj_SFaLQ5gGBzQwL-cTsfD50', 
                        help='when using telegram communication, input your TelegramBot token')
    parser.add_argument('-u', '--url', type=str, default='None', 
                        help='when using slack communication, input your webhook url')
    parser.add_argument('-p', '--path', type=str, default='log_pic/', 
                        help='Save capture image path, default "log_pic/"')

    args = parser.parse_args()
    mode = args.mode
    token = args.token
    url = args.url
    path = args.path
    
    print("----------------------------------")
    print("-------CHECK YOUR PC STATUS-------")
    print("----------------------------------")
    
    print()
    print("----------------------------------")
    print("--#Initializing HW TEST")
    text_form = check_HW_status(mode=-1)
    print("----->DONE")
    print()

    print("----------------------------------")
    print("--#Initializing CAM TEST")
    frame = capture(mode=-1)
    cur_time = time.localtime()
    cur_time = f"{cur_time[0]}{cur_time[1]}{cur_time[2]}{cur_time[3]}{cur_time[4]}{cur_time[5]}"
    full_name = path + cur_time + '_initializing_img.jpg'
    cv2.imwrite(full_name,frame)
    print("----->DONE")
    print()

    print("----------------------------------")
    print("--#Initializing Communication TEST")
    post_process(mode=-1, token=token, url=url, text_form=text_form)
    print("----->DONE")
    print()

    print("----------------------------------")
    print("--#Initializing Thread")
    