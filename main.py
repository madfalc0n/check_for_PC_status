# from modules.CheckPowerStatus import get_power_status
from modules.CheckPowerStatus_psutil import get_power_status
from modules.PostToSlack import post_slack
from modules.PostToTelegram import telegram_bot
from modules.SaveCam import capture
import time
import cv2
from threading import Thread, Lock
import argparse
import keyboard

lock = Lock()

def check_HW_status(mode=1):
    global text_form
    global status_field, status_new_field
    global system_kill, system_op

    if mode == -1:
        PC_status = get_power_status()
        for key, val in PC_status.items():
                print(f"----->{key} : {val}")
        text_form = f"POWER Line Status : {PC_status['ACLineStatus']} \nWindow Locked : {PC_status['windowlocked']}"
        status_field = PC_status.copy()
        status_new_field = PC_status.copy()

    elif mode == 1:
        while True:
            if system_kill == 1:
                print("--$BREAKING FUNCTION : CHECK_HW_STATUS")
                break
            if system_op == 1:
                PC_status = get_power_status()
                status_field = PC_status.copy()
                text_form = f"POWER Line Status : {PC_status['ACLineStatus']} \nWindow Locked : {PC_status['windowlocked']}"
                system_op += 1
                # print(f"DEBUG : index : {i+1} : {text_form}")
                # print(f"DEBUG : POWER CHECK FUNCTION COUNT : {(i%10)+1}")
            time.sleep(0.01)
        


def post_process(mode=1,token=None,url=None):
    """
    mode 0 : Slack communication
    mode 1 : Telegram communication
    """
    global text_form
    global system_kill, system_op


    if mode == -1: ##initializing TEST
        initializing_text = "---INITIALIZING TEST MODE---\n"
        tb = telegram_bot(token)
        tb.post_telegram(initializing_text + text_form)
        user_info = tb.receive_msg()
        print(f"----->Current User Count : {len(user_info)}")

    elif mode == 0: ##Slack 
        # url = 'YOUR SLACK WORKSPACE URL'
        slack_post_result = post_slack(url,text_form)
        # print(slack_post_result)
    
    elif mode == 1: ##Telegram
        # token = 'YOUR TELEGRAM BOT TOKEN'
        while True:
            if system_kill == 1:
                print("--$BREAKING FUNCTION : POST_PROCESS")
                break
            if system_op == 2:
                tb = telegram_bot(token)
                tb.post_telegram(text_form)
                # print(f"DEBUG : SEND TO TELEGRAM FUNCTION COUNT : {(i%10)+1}")
                system_op += 1
            time.sleep(0.01)
        


def status_check():
    global status_field, status_new_field
    global system_kill, system_op


    while True:
        if system_kill == 1:
            print("--$BREAKING FUNCTION : STATUS_CHECK")
            break
        if system_op == 3:
            cur_time = time.localtime()
            cur_time = f"{cur_time[0]}-{cur_time[1]}-{cur_time[2]} {cur_time[3]}:{cur_time[4]}:{cur_time[5]}"
            print("----------------------------------")
            print(f"CUR TIME : {cur_time}")
            print(f"POWER Line Status : {status_field['ACLineStatus']} : {status_new_field['ACLineStatus']}")
            print(f"Window Locked : {status_field['windowlocked']} : {status_new_field['windowlocked']}")
            print("----------------------------------")
            print()
            system_op = 0
        time.sleep(0.01)
    
        
        

def system_input_check():
    global system_kill, system_op, check_timer


    time_val = 100
    i = 0
    while True:
        # key = 
        # print(f"You pressed : {key}")
        if keyboard.is_pressed('q'):
            lock.acquire()
            try:
                print("----------------------------------")
                print("SYSTEM STOPPING BY KEY PRESSED('Q')")
                print("----------------------------------")
                print("--$BREAKING FUNCTION : SYSTEM_INPUT_CHECK")
                system_kill = 1                
            finally:
                lock.release()
            break
        i += 1
        # print(f"CUR INDEX : {i}")
        if i == check_timer * time_val :
            system_op += 1
            i = 0
        time.sleep(1/time_val)
    


if __name__ == "__main__":
    #main.py 실행시 옵션을 설정할 수 있도록 argparse 객체 지정 
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=int, default=1, 
                        help='choice using "telegram" or "slack"')
    parser.add_argument('-t', '--token', type=str, default='1750354982:AAEnceNQ8u_8IBLDXbdEr4RDEXc1Nie0I64', 
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

    #global
    text_form = ''
    status_field = {}
    status_new_field = {}
    check_timer = 5
    system_kill = 0
    system_op = 0
    
    print("----------------------------------")
    print("-------CHECK YOUR PC STATUS-------")
    print("----------------------------------")
    print()

    print("----------------------------------")
    print("--$Initializing HW TEST")
    check_HW_status(mode=-1)
    print("-----> DONE")
    print()

    print("----------------------------------")
    print("--$Initializing CAM TEST")
    frame = capture(mode=-1)
    cur_time = time.localtime()
    cur_time = f"{cur_time[0]}{cur_time[1]}{cur_time[2]}{cur_time[3]}{cur_time[4]}{cur_time[5]}"
    full_name = path + cur_time + '_initializing_img.jpg'
    cv2.imwrite(full_name,frame)
    print("-----> DONE")
    print()

    print("----------------------------------")
    print("--$Initializing Communication TEST")
    
    post_process(mode=-1, token=token, url=url)
    print("-----> DONE")
    print()

    print("----------------------------------")
    print("--$Initializing Thread")
    print("-----> READY...", end='')
    th_hwcheck_1 = Thread(target=check_HW_status, args=(mode,))
    th_hwcheck_1.setDaemon(True)
    
    th_post_1 = Thread(target=post_process, args=(mode, token,url))
    th_post_1.setDaemon(True)

    th_status_1 = Thread(target=status_check)
    th_status_1.setDaemon(True)


    th_status_2 = Thread(target=system_input_check)
    th_status_2.setDaemon(True)
    
    print("DONE")
    print("-----> START")
    print()
    
    th_hwcheck_1.start()
    th_post_1.start()
    th_status_1.start()
    th_status_2.start()

    th_hwcheck_1.join()
    th_post_1.join()
    th_status_1.join()
    th_status_2.join()


