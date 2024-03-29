# from modules.CheckPowerStatus import get_power_status
from modules.CheckPowerStatus_psutil import get_power_status
from modules.PostToSlack import post_slack
from modules.PostToTelegram import telegram_bot
from modules.logging import logging
from modules.SaveCam import capture
import time
from time import strftime, localtime, gmtime
import cv2
from threading import Thread, Lock
import argparse
import keyboard
import os, sys

lock = Lock()

def check_HW_status(mode=1):
    global text_form
    global status_field, status_old_field
    global system_kill, system_op

    if mode == -1:
        PC_status = get_power_status()
        for key, val in PC_status.items():
                print(f"-----> {key} : {val}")
        # text_form = f"POWER Line Status : {PC_status['ACLineStatus']} \nWindow Locked : {PC_status['windowlocked']}"
        text_form = f"POWER Line Status : {PC_status['ACLineStatus']}"
        status_field = PC_status.copy()
        status_old_field = PC_status.copy()

    elif mode == 1:
        while True:
            if system_kill == 1:
                print("--$ BREAKING FUNCTION : CHECK_HW_STATUS")
                break
            if system_op == 1:
                PC_status = get_power_status()
                status_field = PC_status.copy()
                # text_form = f"POWER Line Status : {PC_status['ACLineStatus']} \nWindow Locked : {PC_status['windowlocked']}"
                text_form = f"POWER Line Status : {PC_status['ACLineStatus']}"
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
    global user_id
    global full_name


    if mode == -1: ##initializing TEST
        initializing_text = "---INITIALIZING TEST MODE---\n"
        tb = telegram_bot(token)
        user_info = tb.receive_msg()
        print(f"-----> Current User Count : {len(user_info)}")
        user_id = list(user_info.keys())[0]
        print(f"-----> USER ID : {user_id}")
        print(f"-----> Send HW status......", end='')
        tb.post_telegram(user_id, initializing_text + text_form )
        print(f"DONE")
        print(f"-----> Send Captured image......", end='')
        tb.send_photo(full_name, user_id)
        print(f"DONE")

    elif mode == 0: ##Slack 
        # url = 'YOUR SLACK WORKSPACE URL'
        slack_post_result = post_slack(url,text_form)
        # print(slack_post_result)
    
    elif mode == 1: ##Telegram
        # token = 'YOUR TELEGRAM BOT TOKEN'
        while True:
            if system_kill == 1:
                print("--$ BREAKING FUNCTION : POST_PROCESS")
                break
            if system_op == 3:
                tb = telegram_bot(token)
                tb.post_telegram(user_id, text_form)
                # print(f"DEBUG : SEND TO TELEGRAM FUNCTION COUNT : {(i%10)+1}")
                system_op = 0
            time.sleep(0.01)
        


def status_check():
    global status_field, status_old_field
    global system_kill, system_op
    global stat_log_path

    while True:
        if system_kill == 1:
            print("--$ BREAKING FUNCTION : STATUS_CHECK")
            break
        if system_op == 2:
            cur_time = strftime("%a, %d %b %Y %H:%M:%S (KST)", localtime())
            print("----------------------------------")
            print(cur_time)
            # print(f"POWER Line Status : {status_field['ACLineStatus']} : {status_old_field['ACLineStatus']}")
            if status_field['ACLineStatus'] != status_old_field['ACLineStatus']:
                logtext = f"{cur_time} : POWER Line Status is Changed : {status_old_field['ACLineStatus']} -> {status_field['ACLineStatus']}" 
                print(f"POWER Line Status is Changed : {status_old_field['ACLineStatus']} -> {status_field['ACLineStatus']}")
                status_old_field['ACLineStatus'] = status_field['ACLineStatus']
            else:
                logtext = f"{cur_time} : POWER Line Status is not Changed : {status_field['ACLineStatus']}" 
                print(f"POWER Line Status is not Changed : {status_field['ACLineStatus']}")
            # print(f"Window Locked : {status_field['windowlocked']} : {status_old_field['windowlocked']}")
            print("----------------------------------")
            print()
            
            #logging
            full_name = stat_log_path + strftime("%Y%m%d", localtime()) + '_HW_log.log'
            logging(full_name, logtext)
            
            system_op += 1
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
                print("--$ BREAKING FUNCTION : SYSTEM_INPUT_CHECK")
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
    if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        os.system("cls")
    else:
        os.system("clear")
    
    print("----------------------------------")
    print("-------CHECK YOUR PC STATUS-------")
    print("----------------------------------")
    print()

    #main.py 실행시 옵션을 설정할 수 있도록 argparse 객체 지정 
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=int, default=1, 
                        help='choice using "telegram" or "slack"')
    parser.add_argument('-t', '--token', type=str, default='1750354982:AAEnceNQ8u_8IBLDXbdEr4RDEXc1Nie0I64', 
                        help='when using telegram communication, input your TelegramBot token')
    parser.add_argument('-u', '--url', type=str, default='None', 
                        help='when using slack communication, input your webhook url')
    parser.add_argument('-lp', '--pic_path', type=str, default='log_pic/', 
                        help='Save capture image path, default "log_pic/"')
    parser.add_argument('-ls', '--stat_path', type=str, default='log_stat/', 
                        help='Save HW status log path, default "log_stat/"')


    args = parser.parse_args()
    mode = args.mode
    token = args.token
    url = args.url
    pic_log_path = args.pic_path
    if not os.path.exists(pic_log_path):
        print(f"--$ INFO : There is no '{pic_log_path}' Create a new directory.")
        os.makedirs(pic_log_path)
    stat_log_path = args.stat_path
    if not os.path.exists(stat_log_path):
        print(f"--$ INFO : There is no '{stat_log_path}' Create a new directory.")
        os.makedirs(stat_log_path)

    #global
    text_form = ''
    status_field = {}
    status_old_field = {}
    check_timer = 5
    system_kill = 0
    system_op = 0
    user_id = ''
    
    print()
    print("----------------------------------")
    print("--$ Initializing HW TEST")
    check_HW_status(mode=-1)
    print("-----> DONE")
    print()

    print("----------------------------------")
    print("--$ Initializing CAM TEST")
    frame = capture(mode=-1)
    cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    full_name = pic_log_path  + cur_time + '_initializing_img.jpg'
    cv2.imwrite(full_name,frame)
    print("-----> DONE")
    print()

    print("----------------------------------")
    print("--$ Initializing Communication TEST")
    post_process(mode=-1, token=token, url=url)
    print("-----> DONE")
    print()

    print("----------------------------------")
    print("--$ Initializing Thread")
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


