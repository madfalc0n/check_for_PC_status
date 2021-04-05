from modules.CheckPowerStatus import get_power_status
from modules.PostToSlack import post_slack
import time

def main_process():
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

        url = 'YOUR SLACK WORKSPACE URL'
        text_form = f"POWER Line Status : {Battery_connected} \nWindow Locked : {window_status}"

        slack_post_result = post_slack(url,text_form)
        print(slack_post_result)
        count += 1
        time.sleep(40)


if __name__ == "__main__":
    print("----------------------------")
    print("CHECK YOUR PC STATUS")
    print("----------------------------")
    main_process()