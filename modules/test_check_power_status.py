import ctypes
from ctypes import wintypes
import time

class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
    ]

SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
GetSystemPowerStatus.restype = wintypes.BOOL

status = SYSTEM_POWER_STATUS()
if not GetSystemPowerStatus(ctypes.pointer(status)):
    raise ctypes.WinError()

# print('ACLineStatus', status.ACLineStatus)
# print('BatteryFlag', status.BatteryFlag)
# print('BatteryLifePercent', status.BatteryLifePercent)
# print('BatteryLifeTime', status.BatteryLifeTime)
# print('BatteryFullLifeTime', status.BatteryFullLifeTime)

user32 = ctypes.windll.User32
#
#print(user32.GetForegroundWindow())
#
for _ in range(150):
    print(user32.GetForegroundWindow(), end=' ')
    if (user32.GetForegroundWindow() % 10 == 0): print(f'Locked')
    # 10553666 - return code for unlocked workstation1
    # 0 - return code for locked workstation1
    #
    # 132782 - return code for unlocked workstation2
    # 67370 -  return code for locked workstation2
    #
    # 3216806 - return code for unlocked workstation3
    # 1901390 - return code for locked workstation3
    #
    # 197944 - return code for unlocked workstation4
    # 0 -  return code for locked workstation4
    #
    else: print('Unlocked')
    time.sleep(1)
