import sys
import pyautogui
import time

import global_Var


def way1(img_name):
    lOrR = 'left'
    times = 0
    img_location = 'cmd\\' + img_name
    while not global_Var.g.if_out():
        if times == 50:
            print('未找到图片' + img_name + '，出现错误，运行终止')
            global_Var.g.set_1()
            sys.exit(0)
        location = pyautogui.locateCenterOnScreen(img_location, confidence=0.9)
        if location is not None:
            pyautogui.click(location.x, location.y, duration=0.1, button=lOrR)
            break
        print('未找到匹配图片' + img_name + ',0.1秒后重试')
        times = times + 1
        time.sleep(0.1)
    return


def way2(location):
    pyautogui.click(location.x, location.y, duration=0.1, button='left')
