import sys
import threading
import pyautogui
import time
import xlrd

stop_event = threading.Event()
stop_event_error = threading.Event()


def monitor():
    while not stop_event.is_set() and not stop_event_error.is_set():
        location = pyautogui.locateCenterOnScreen('cmd\\end.png', confidence=0.9)
        if location is not None:
            print('出现停止信号')
            pyautogui.click(location.x, location.y, clicks=1, interval=0.2, duration=0.1, button='left')
            stop_event.set()
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


def mouseClick(clickTimes, img_name):
    lOrR = 'left'
    times = 0
    img_location = 'cmd\\' + img_name
    while not stop_event.is_set():
        if times == 50:
            print('未找到图片' + img_name + '，出现错误，运行终止')
            stop_event_error.set()
            sys.exit(0)
        location = pyautogui.locateCenterOnScreen(img_location, confidence=0.9)
        if location is not None:
            pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.1, button=lOrR)
            break
        print('未找到匹配图片' + img_name + ',0.1秒后重试')
        times = times + 1
        time.sleep(0.1)
    return


def cmd_list(command):
    i = 1
    while i < command.nrows:
        # while i < 5:
        # 特别，第一次移动需要延长反应时间
        if i == 6: time.sleep(5)
        # 取本行指令的操作类型
        cmdType = command.row(i)[0]
        if cmdType.value == 1.0:  # 点击图片
            img_name = command.row(i)[1].value
            mouseClick(1, img_name)
        elif cmdType.value == 2.0:  # 拖动
            pyautogui.moveTo(100, 540, duration=0.1)  # 移动到 (100,540)
            cmd_val = command.row(i)[1].value
            _index = cmd_val.find(',')
            x = int(cmd_val[1:_index])
            y = int(cmd_val[_index + 1:-1])
            pyautogui.dragRel(x, y, 2, button='left')
        elif cmdType.value == 3.0:  # 打牌
            time.sleep(5)
            play()
        print(str(command.row(i)[2].value))
        i = i + 1
        time.sleep(1)
    sys.exit(0)


def next_round():
    location = pyautogui.locateCenterOnScreen('cmd\\next1.png', confidence=0.9)
    if location is None:
        location = pyautogui.locateCenterOnScreen('cmd\\next2.png', confidence=0.9)
        if location is None:
            print('牌数达到上限，却无法进入下回合，运行终止')
            stop_event_error.set()
            sys.exit(0)
        else:
            next = 'next2.png'
    else:
        next = 'next1.png'
    return next


def play():
    region = (250, 800, 1200, 200)
    cards = 0
    while not stop_event.is_set():
        # 一回合只打7张牌
        time.sleep(2)
        if cards >= 7:
            mouseClick(1, next_round())
            cards = 0
            time.sleep(7)
            continue
        # 优先打24的狂气，其次打1费卡,0费卡有异常卡，尽量不打
        location = pyautogui.locateCenterOnScreen('cmd\\attack.png', confidence=0.9)
        if location is None:
            location = pyautogui.locateCenterOnScreen('cmd\\cost1_1.png', region=region, confidence=0.9)
            if location is None:
                location = pyautogui.locateCenterOnScreen('cmd\\cost1_2.png', region=region, confidence=0.9)
                if location is None:
                    location = pyautogui.locateCenterOnScreen('cmd\\cost0_1.png', region=region, confidence=0.9)
                    if location is None:
                        # 没牌打了就下一回合
                        time.sleep(2)
                        mouseClick(1, next_round())
                        cards = 0
                        time.sleep(7)
                        continue
            pyautogui.moveTo(location.x, location.y, duration=0.1)
            pyautogui.dragRel(0, -400, 1, button='left')
            cards = cards + 1
        else:
            mouseClick(1, 'attack.png')
            mouseClick(1, 'attack_.png')
            time.sleep(3)


if __name__ == '__main__':
    file = 'cmd.xls'
    # 打开文件
    wb = xlrd.open_workbook(filename=file)
    # 通过索引获取表格sheet页
    work1 = wb.sheet_by_index(0)
    print('读取命令表成功，下面是检查命令表')
    # 数据检查
    checkCmd = dataCheck(work1)
    if checkCmd:
        # key = input('命令表正确\n输入要循环的次数 \n')
        # key = int(key)
        key = 2
        time.sleep(5)
        while key != 0 and not stop_event_error.is_set():
            t1 = threading.Thread(target=cmd_list, args=(work1,))
            t2 = threading.Thread(target=monitor)

            t1.start()
            t2.start()

            t1.join()
            t2.join()

            time.sleep(2)
            print('等待2秒')
            key = key - 1
            stop_event = threading.Event()
            stop_event_error = threading.Event()
    else:
        print('输入有误或者已经退出!')
