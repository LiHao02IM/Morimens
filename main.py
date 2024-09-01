import sys
import threading
import pyautogui
import time
import xlrd

import get_location
import global_Var
import play


def monitor():
    region = (1450, 930, 390, 100)
    while not global_Var.g.if_out():
        location = get_location.way3('end.png', region)
        if location is not None:
            print('出现停止信号')
            pyautogui.click(location.x, location.y, duration=0.3)
            global_Var.g.set_0()
            sys.exit(0)


def dataCheck(sheet1):
    checkCmd = True
    # 行数检查
    if sheet1.nrows < 2:
        print("没有命令")
        checkCmd = False
    # 每行数据检查
    i = 1
    while i < sheet1.nrows:
        # 第1列 操作类型检查
        cmdType = sheet1.row(i)[0]
        if cmdType.ctype != 2:
            print('第', i + 1, "行,第1列数据有毛病")
            checkCmd = False
        # 第2列 内容检查
        cmdValue = sheet1.row(i)[1]
        # 读图点击类型指令、拖动类型指令，内容必须为字符串类型
        if cmdType.value == 1.0 or cmdType.value == 2.0:
            if cmdValue.ctype != 1:
                print('第', i + 1, "行,第2列数据有毛病")
                checkCmd = False
        i += 1
    return checkCmd


def cmd_list(command):
    i = 1
    while i < command.nrows and not global_Var.g.if_out():
        # 特别，第一次移动需要延长反应时间
        if i == 6:
            time.sleep(5)
        # 取本行指令的操作类型
        cmdType = command.row(i)[0]
        if cmdType.value == 1.0:  # 移动
            img_name = command.row(i)[1].value
            location = get_location.way1(img_name)
            if location is not None:
                pyautogui.click(location.x, location.y, duration=0.3)
            else:
                print('error:未找到指定地点，无法移动')
                global_Var.g.set_1()
                sys.exit(1)
        elif cmdType.value == 2.0:  # 拖动
            img_name = command.row(i)[3].value
            location = get_location.way1(img_name)
            if location is not None:
                pyautogui.moveTo(100, 540, duration=0.1)
                cmd_val = command.row(i)[1].value
                _index = cmd_val.find(',')
                x = int(cmd_val[1:_index])
                y = int(cmd_val[_index + 1:-1])
                pyautogui.dragRel(x, y, 2, button='left')
            else:
                time.sleep(5)
                if not global_Var.g.if_out():
                    print('error:请找到启始点重启程序')
                    global_Var.g.set_1()
                    sys.exit(1)
                else:
                    sys.exit(0)
        elif cmdType.value == 3.0:  # 打牌
            time.sleep(7)
            play.work(8)
        print(str(command.row(i)[2].value))
        i = i + 1
        time.sleep(1)
    sys.exit(0)


if __name__ == '__main__':

    global_Var.create()
    times = 0

    print('正在读取命令表')
    file = 'cmd.xls'
    wb = xlrd.open_workbook(filename=file)
    work1 = wb.sheet_by_index(0)
    print('读取命令表成功')

    print('正在检查命令表')
    checkCmd = dataCheck(work1)
    print('命令表正确')

    if checkCmd:
        key = input('\n输入要循环的次数 \n')
        key = int(key)
        print('2s后自动最小化当前界面')
        time.sleep(2)
        pyautogui.hotkey('alt', 'space', 'n')
        time.sleep(2)
        while key != 0 and not global_Var.g.if_error():
            global_Var.g.init_0()
            t1 = threading.Thread(target=cmd_list, args=(work1,))
            t2 = threading.Thread(target=monitor)

            t1.start()
            t2.start()

            t1.join()
            t2.join()

            time.sleep(2)

            key = key - 1
            times = times + 1
            if key != 0 and not global_Var.g.if_error():
                print('2s后进入新一轮')
        if key != 0:
            print('因异常退出')
    else:
        print('输入有误或者已经退出!')
    print('已运行' + str(times) + '轮，截止时间：' + time.strftime("%Y-%m-%d %H:%M:%S"))
    pyautogui.hotkey('alt', 'tab')
