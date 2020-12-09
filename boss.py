
import os, time, sys
import util
import ocr_manager

boss_alive_head_img = "4.png"
back_img = "back.png"
choose_img = "choose.png"
login_img = "login.png"

confidence = 0.8

boss_alive_head_img_path = os.getcwd() + "/img_base/" + boss_alive_head_img
back_img_path = os.getcwd() + "/img_base/" + back_img
choose_img_path = os.getcwd() + "/img_base/" + choose_img
login_img_path = os.getcwd() + "/img_base/" + login_img

current_charcter_index = 1

# 找到boss存活时 目标图片区域证据
boss_find_out_test = os.getcwd() + "/img_out/"

# 获取boss死亡头像中间点坐标
def find_boss_alive_center(screen_path):
	find_result = util.find_match_img(screen_path, boss_alive_head_img_path, confidence)
	if find_result == None:
		util.debug("No boss found in the current screen")
		return
	center_result = find_result
	return center_result

def find_back_btn_center(screen_path):
	find_result = util.find_match_img(screen_path, back_img_path, confidence)
	if find_result == None:
		util.debug("No back button found in the current screen")
		return
	else:
		center_result = find_result
		return center_result

def find_choose_btn_center(screen_path):
	find_result = util.find_match_img(screen_path, choose_img_path, confidence)
	if find_result == None:
		util.debug("No choose button found in the current screen")
		return
	else:
		center_result = find_result
		return center_result
def find_login_btn_center(screen_path):
	find_result = util.find_match_img(screen_path, login_img_path, confidence)
	if find_result == None:
		util.debug("No login button found in the current screen")
		return
	else:
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

def choose_next_character():
	global current_charcter_index;
	current_charcter_index += 1
	offset = 10 + 73*current_charcter_index
	if offset > 1080:
		util.error("当前页面角色已经全部完成，结束任务")
		return False

	choose_btn = None
	find_count = 0
	while find_count < 20 and choose_btn == None:
		sys.stdout.write("\rScreen scanning, waiting for the charcter choose btn{}".format("." * (find_count % 3 + 1)))
		sys.stdout.flush()

		screen_path = util.screenshots()
		choose_btn = find_choose_btn_center(screen_path)
		time.sleep(1)
	if choose_btn == None:
		return False
	x = choose_btn[0]
	y = choose_btn[1] + offset
	util.mouse_to(x, y)
	util.mouse_left_click()
	util.info("已经选中下一个角色，编号{}".format(current_charcter_index))

	login_btn = None
	find_count = 0
	while find_count < 20 and login_btn == None:
		sys.stdout.write("\rScreen scanning, waiting for the login btn{}".format("." * (find_count % 3 + 1)))
		sys.stdout.flush()

		screen_path = util.screenshots()
		login_btn = find_login_btn_center(screen_path)
		time.sleep(1)
	if login_btn == None:
		return False
	x = login_btn[0]
	y = login_btn[1]
	util.mouse_to(x, y)
	util.mouse_left_click()

	util.info("已经点击进入游戏按钮，loading...")
	time.sleep(30)
	return True

def switch_character():
	util.info("开始切换角色")

	back_btn = None
	find_count = 0
	while find_count < 20 and back_btn == None:
		sys.stdout.write("\rScreen scanning, waiting for the back btn{}".format("." * (find_count % 3 + 1)))
		sys.stdout.flush()

		util.back_menu()
		screen_path = util.screenshots()
		back_btn = find_back_btn_center(screen_path)
		if back_btn == None:
			util.back_menu()
		time.sleep(1)
	if back_btn == None:
		return False

	# check_pic(back_btn, screen_path)
	x = back_btn[0]
	y = back_btn[1]
	util.mouse_to(x, y)
	util.mouse_left_click()
	util.info("already click back btn, waiting back...")
	time.sleep(30)
	return choose_next_character()