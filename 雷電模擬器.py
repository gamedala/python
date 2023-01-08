import time
 
from Dnconsole import Dnconsole
import cv2 as cv
 
 
def compare_status(st0: list, st1: list) -> bool:  # True相同 False不同
    if len(st0) != len(st1):
        return False
    for i in range(len(st0)):
        if len(st0[i]) != len(st1[i]):
            return False
        for j in range(len(st0[i])):
            if st0[i][j] != st1[i][j]:
                return False
    return True
 
 
def copy_statu(status: list) -> list:
    result = list()
    for line in status:
        result.append([line[0], line[1], line[2], line[3]])
    return result
 
 
def read_num(area: tuple, screen: str, template: list) -> int:
    scr = cv.imread(screen)
    cur_area = scr[area[1]:area[3], area[0]:area[2]]  # 前面是y轴 后面是x轴
    for i, tmp in enumerate(template):
        tp = cv.imread(tmp)
        try:
            result = cv.matchTemplate(cur_area, tp, cv.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if min_val < 0.001:
                return int(template[i].replace('2048/', '').replace('.png', ''))
        except cv.error:
            continue
    return -1
 
 
def get_cur_status() -> list:
    result = list()
    result.append([0, 0, 0, 0])
    result.append([0, 0, 0, 0])
    result.append([0, 0, 0, 0])
    result.append([0, 0, 0, 0])
    pos = [30, 260, 240, 470]  # , [300, 260, 510, 470], [570, 260, 780, 470], [840, 260, 1050, 470]]
    template = ['2048/0.png', '2048/2.png', '2048/4.png', '2048/8.png', '2048/16.png', '2048/32.png',
                '2048/64.png', '2048/128.png', '2048/256.png', '2048/512.png', '2048/1024.png']
    screen = 'E:/Project/PyCharmProj/Script/2048/share/2048.png'
    for i in range(4):
        for j in range(4):
            area = (pos[0] + 270 * j, pos[1] + 270 * i, pos[2] + 270 * j, pos[3] + 270 * i)
            result[i][j] = read_num(area, screen, template)
    return result
 
 
def swipe_up():
    Dnconsole.swipe(0, (540, 1280), (540, 260))
    print('上移')
 
 
def swipe_down():
    Dnconsole.swipe(0, (540, 260), (540, 1280))
    print('下移')
 
 
def swipe_left():
    Dnconsole.swipe(0, (1000, 770), (100, 770))
    print('左移')
 
 
def swipe_right():
    Dnconsole.swipe(0, (100, 770), (1000, 770))
    print('右移')
 
 
def get_null_count(status: list) -> int:
    if len(status) == 0:
        print('此方向移动无效')
        return -1
    result = 0
    for row in status:
        for node in row:
            if node == 0:
                result += 1
    return result
 
 
def get_sum(line: list) -> int:
    total = 0
    for i in range(len(line)):
        total += line[i]
    return total
 
 
def compress_line(line: list) -> list:
    # 压实一条数据
    length = len(line)
    result = line[:]
    if get_sum(line) == 0:  # 全零则直接返回
        return line
    for i in range(length):
        if get_sum(result[i:]) == 0:
            break
        while result[i] == 0:
            for j in range(i, length - 1):
                result[j] = result[j + 1]
                result[j + 1] = 0
    return result
 
 
def combine_line(line: list) -> list:
    # 合并一条数据
    length = len(line)
    result = line[:]
    for i in range(length - 1):
        if result[i] == result[i + 1]:
            result[i] *= 2
            result[i + 1] = 0
    return result
 
 
def deduction_up(status: list) -> list:
    result = copy_statu(status)
    # 先把数据压实,再合并
    for i in range(4):
        line = [result[0][i], result[1][i], result[2][i], result[3][i]]
        line = compress_line(line)  # 压实(去掉为0的格子)
        line = combine_line(line)  # 合并
        line = compress_line(line)  # 压实
        result[0][i], result[1][i], result[2][i], result[3][i] = line[0], line[1], line[2], line[3]
    if compare_status(result, status):
        return []
    return result
 
 
def deduction_down(status: list) -> list:
    result = copy_statu(status)
    # 先把数据压实,再合并
    for i in range(4):
        line = [result[3][i], result[2][i], result[1][i], result[0][i]]
        line = compress_line(line)  # 压实(去掉为0的格子)
        line = combine_line(line)  # 合并
        line = compress_line(line)  # 压实
        result[3][i], result[2][i], result[1][i], result[0][i] = line[0], line[1], line[2], line[3]
    if compare_status(result, status):
        return []
    return result
 
 
def deduction_left(status: list) -> list:
    result = copy_statu(status)
    # 先把数据压实,再合并
    for i in range(4):
        line = [result[i][0], result[i][1], result[i][2], result[i][3]]
        line = compress_line(line)  # 压实(去掉为0的格子)
        line = combine_line(line)  # 合并
        line = compress_line(line)  # 压实
        result[i][0], result[i][1], result[i][2], result[i][3] = line[0], line[1], line[2], line[3]
    if compare_status(result, status):
        return []
    return result
 
 
def deduction_right(status: list) -> list:
    result = copy_statu(status)
    # 先把数据压实,再合并
    for i in range(4):
        line = [result[i][3], result[i][2], result[i][1], result[i][0]]
        line = compress_line(line)  # 压实(去掉为0的格子)
        line = combine_line(line)  # 合并
        line = compress_line(line)  # 压实
        result[i][3], result[i][2], result[i][1], result[i][0] = line[0], line[1], line[2], line[3]
    if compare_status(result, status):
        return []
    return result
 
 
def run():
    if Dnconsole.is_running(0) is False:
        Dnconsole.launch(0)
    for i in range(120):
        if Dnconsole.is_running(0):
            time.sleep(10)
            break
        time.sleep(1)
    Dnconsole.invokeapp(0, 'com.digiplex.game')
    end_status = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
    if Dnconsole.wait_activity(0, 'com.digiplex.game/.MainActivity', 20) is True:
        while True:
            Dnconsole.dnld(0, 'screencap -p /sdcard/Pictures/2048.png')
            time.sleep(1)
            status = get_cur_status()
            if compare_status(end_status, status):
                print('结束')
                break
            print('status=', status)
            func = [deduction_up, deduction_down, deduction_left, deduction_right]
            swipe = [swipe_up, swipe_down, swipe_left, swipe_right]
            max_count = 0
            direction = -1
            for i in range(4):
                c = get_null_count(func[i](status))
                if c > max_count:
                    direction = i
                    max_count = c
            if direction == -1:
                print('结束')
                return
            swipe[direction]()
            time.sleep(1.5)