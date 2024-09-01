import sys

import pyautogui
import time

import get_location
import global_Var
import next_round

flag = 0


# 默认出牌策略，优先打24的狂气，其次打1费、0费卡,0费卡有掉血异常卡，尽量不打
def way1():
    region1 = (10, 10, 150, 150)
    region2 = (250, 800, 1350, 150)
    location = get_location.way3('attack.png', region1)
    if location is None:
        location = get_location.way3('cost1_1.png', region2)
        if location is None:
            location = get_location.way3('cost1_2.png', region2)
            if location is None:
                location = get_location.way3('cost0_1.png', region2)
                if location is None:
                    return None
    else:
        global flag
        flag = 1
    return location


def work(max_cards=7):
    global flag
    location = None
    while not global_Var.g.if_out():  # 监控每个回合的情况
        cards = 0
        # 一回合只打7张牌
        while cards <= max_cards and not global_Var.g.if_out():  # 监控当前回合情况
            card_location = way1()
            if card_location is not None:
                if flag == 1:
                    pyautogui.click(card_location.x, card_location.y, duration=0.1)
                    card_location = get_location.way1('attack_.png')
                    pyautogui.click(card_location.x, card_location.y, duration=0.1)
                    flag = 0
                    time.sleep(4)
                else:
                    pyautogui.moveTo(card_location.x, card_location.y, duration=0.1)
                    pyautogui.dragRel(0, -400, 1, button='left')
                    cards += 1
                    time.sleep(1)
                location = next_round.way1()
                if location is not None:
                    break
            else:  # 没牌可打，费用还有多
                break
        if location is None:
            location = next_round.way2()
            if location is None:
                time.sleep(5)
                if not global_Var.g.if_out():
                    print('error:无法进入下一回合')
                    global_Var.g.set_1()
                    sys.exit(1)
                else:
                    sys.exit(0)
        pyautogui.click(location.x, location.y, duration=0.3)
        time.sleep(8)
