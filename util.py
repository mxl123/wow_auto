from PIL import ImageGrab, Image, ImageEnhance
import numpy as np
import time, os
import cv2
# import keymouse

red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
plain='\033[0m'

key_attack = '1'
key_attack_target_clear = '2'
key_open_back_menu = 'esc'


key_dic = {
	key_attack : 'attack boss',
	key_attack_target_clear : 'clear target',
	key_open_back_menu : 'open back menu'
}

log_debug = False

screenshots_dic = os.getcwd() + "/img_tmp_cache/tmp_screen/"

def norml(mes):
    print("{} {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), mes))
def info(mes):
    print("{}{} {}{}".format(green, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), plain, mes))
def warn(mes):
    print("{}{} {}{}".format(yellow, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), plain, mes))
def error(mes):
    print("{}{} {}{}".format(red, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), plain, mes))
def debug(mes):
    if log_debug:
        print("{} {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), mes))

# my_keymouse = keymouse.Keymouse()
def click(key):
    key_mes = key
    if key in key_dic:
        key_mes = key_dic[key]
    debug("press (and up) the key:{}".format(key_mes))
    # my_keymouse.click(key)

def mouse_to(x, y):
    debug("move mouse to point ({}, {})".format(x, y))
    # my_keymouse.mouse_to(x, y)

def mouse_left_click():
    debug("click mouse left btn")
    # my_keymouse.mouse_left_click()

def get_image_path(dic):
    name = time.strftime("%Y-%m-%d---%H:%M:%S", time.localtime()).replace(':', '-')
    return dic + name + ".png"

def screenshots():
    path = get_image_path(screenshots_dic)
    pic = ImageGrab.grab()
    pic.save(r'%s' % path)
    return path

def back_menu():
    click(key_attack_target_clear)
    click(key_open_back_menu)

def find_match_img(imgsrc, imgobj, confidence=0.8):
    source_img_s = cv2.imread(imgsrc, cv2.IMREAD_COLOR)
    source_img = cv2.cvtColor(source_img_s, cv2.COLOR_BGR2GRAY)

    # res_img = os.getcwd() + "/img_base/res.png"
    # cv2.imwrite(res_img, source_img)
    # return

    target_img = cv2.imread(imgobj, cv2.IMREAD_COLOR)
    target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

    w, h = target_img.shape[::-1]

    method = cv2.TM_CCOEFF_NORMED
    result = cv2.matchTemplate(source_img, target_img, method)

    # 一个点
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    #     top_left = min_loc
    # else:
    #     top_left = max_loc
    # center_point = (top_left[0]+w/2, top_left[1]+h/2)
    # info("最大相似度为{}".format(max_val))

    # 多个点并标记
    threshold = confidence
    center_point = None
    loc = np.where(result >= threshold)
    count = 0
    for pt in zip(*loc[::-1]):
        print(pt)
        cv2.rectangle(source_img_s, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        if count == 0:
            center_point = (pt[0] + w/2, pt[1] + h/2)
    if center_point != None:
        res_img = os.getcwd() + "/img_base/res.png"
        cv2.imwrite(res_img, source_img_s)
    return center_point

def find_matches(haystack, needle):
    arr_h = np.asarray(haystack)
    arr_n = np.asarray(needle)

    y_h, x_h = arr_h.shape[:2]
    y_n, x_n = arr_n.shape[:2]

    xstop = x_h - x_n + 1
    ystop = y_h - y_n + 1

    matches = []
    for xmin in range(0, xstop):
        for ymin in range(0, ystop):
            xmax = xmin + x_n
            ymax = ymin + y_n

            arr_s = arr_h[ymin:ymax, xmin:xmax]     # Extract subimage
            arr_t = (arr_s == arr_n)                # Create test matrix
            if arr_t.all():                         # Only consider exact matches
                matches.append((xmin,ymin))

    return matches

# tmp_sub_img = os.getcwd() + "/img_base/back.png"
# tmp_img = os.getcwd() + "/img_base/1.png"
# print(test_find_match_img(tmp_img, tmp_sub_img))
