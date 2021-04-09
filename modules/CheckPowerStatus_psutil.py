import psutil
import ctypes

def get_power_status():
    result = dict()
    sensors_battery = psutil.sensors_battery()
    result['ACLineStatus'] = sensors_battery[2]
    result['BatteryLifePercent'] = sensors_battery[0]
    result['BatteryLifeTime'] = sensors_battery[1]

    user32 = ctypes.windll.User32
    if (user32.GetForegroundWindow() % 10 == 0):
        result['windowlocked'] = 1
        # print(f'Locked')
    else: 
        # print('Unlocked')
        result['windowlocked'] = 0

    return result

#test mode
if __name__ == "__main__":
    print(get_power_status())
