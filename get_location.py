import pyautogui
import time

import global_Var


# 获取图片位置，会持续寻找5秒，没有则返回空,用于寻找主重要位置
def way1(img_name):
    times = 0
    img_location = 'cmd\\' + img_name
    while times <= 50 and not global_Var.g.if_out():
        location = pyautogui.locateCenterOnScreen(img_location, confidence=0.9)
        if location is not None:
            return location
        else:
            times += 1
            time.sleep(0.1)
    return None


# 获取图片位置，只找一遍，没有则返回空，用于寻找不太重要位置
def way2(img_name):
    img_location = 'cmd\\' + img_name
    if not global_Var.g.if_out():
        location = pyautogui.locateCenterOnScreen(img_location, confidence=0.9)
        if location is not None:
            return location
    return None


# 获取指定区域内的图片位置，没有则返回空，用于出牌
def way3(img_name, region):
    img_location = 'cmd\\' + img_name
    if not global_Var.g.if_out():
        location = pyautogui.locateCenterOnScreen(img_location, confidence=0.9, region=region)
        if location is not None:
            return location
    return None
