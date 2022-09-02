import subprocess
import time
from ppadb.client import Client as AdbClient
from common_func import *
import pygetwindow as gw
import pywinauto


def android_develop():
    subprocess.call(["./platform_tools/adb.exe"])


def android_display():
    subprocess.Popen(['./scrcpy/scrcpy.exe'])
    time.sleep(2)
    win = gw.getWindowsWithTitle('SM-G930S')[0]
    win.moveTo(1380, 0)


def last_picture():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    device = devices[0]
    file_listing = device.shell("ls -p /sdcard/DCIM/Camera/").split('  ')
    file_list = []
    for i in file_listing:
        i = i.strip('\n')
        if i != '':
            file_list.append(i)
    file_list = sorted(file_list)
    img_dir = f"/sdcard/DCIM/Camera/{file_list[-1]}"
    device.pull(f"/sdcard/DCIM/Camera/{file_list[-1]}", f"./DLP_temp/{file_list[-1]}")
    return f"./DLP_temp/{file_list[-1]}"


def android_picture():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    device = devices[0]
    now_display = device.shell("dumpsys activity activities | grep -i run")
    if 'camera' in now_display and 'GalleryActivity' not in now_display:
        device.shell("input swipe 385 285 385 285 1000")
        time.sleep(1)
        device.shell("input keyevent 27")
    else:
        device.shell("am start -W -c android.intent.category.HOME -a android.intent.action.MAIN")
        time.sleep(1)
        device.shell("input keyevent 27")
        device.shell("input swipe 385 285 385 285 1000")
        time.sleep(1)
        device.shell("input keyevent 27")

#컴퓨터 및 안드로이드 바꼇을 경우 장비번호 알아보는 함수
def connect():
    client = AdbClient(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037
    devices = client.devices()

    if len(devices) == 0:
        print('No devices')
        quit()

    device = devices[0]
    print(f'Connected to {device}')
    return device, client