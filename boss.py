
import os, time
import util
import ocr_manager

boss_alive_head_img = "4.png"

boss_alive_head_img_path = os.getcwd() + "/img_base/" + boss_alive_head_img

# 找到boss存活时 目标图片区域证据
boss_find_out_test = os.getcwd() + "/img_out/"

# 获取boss死亡头像中间点坐标
def find_boss_alive_center(screen_path):
	find_result = util.find_match_img(screen_path, boss_alive_head_img_path, util.confidence)
	if find_result == None:
		util.debug("No boss found in the current screen")
		return
	center_result = find_result
	return center_result

static_count = 0
def attack():
	global static_count
	if static_count % 2 == 0 :
		util.click('space')
	util.click(util.key_attack)
	static_count += 1

def check_pic(alive_center, screen_path):
	x = alive_center[0]
	y = alive_center[1]
	ocr_manager.cut_image(screen_path, util.get_image_path(boss_find_out_test), (x-100, y-100, x+100, y+100))

# 攻击存活的boss
def attack_alive():
	count = 1;
	while count < 10:
		attack()
		count += 1
		time.sleep(0.5)
