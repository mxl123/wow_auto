import json, os, random, sys, time
import util
import boss

# 默认服务器所属区（按照json顺序）
default_server_index = 0
# 默认服务器（按照json顺序）
default_sub_server_index = 0
# 默认角色
default_character_index = 0

img_servers_json_path = os.getcwd() + "/img_servers.json"
choose_img_path = os.getcwd() + "/img_base/choose.png"
login_img_path = os.getcwd() + "/img_base/login.png"
exit_img_path = os.getcwd() + "/img_base/back.png"

cache_json_path = os.getcwd() + "/progress_cache.json"

json_data = None
servers = None
with open(img_servers_json_path) as servers_obj:
	json_data = json.load(servers_obj)
servers = json_data["servers"]


cache_json_data = None
cache_servers = None
with open(cache_json_path) as cache_servers_obj:
	cache_json_data = json.load(cache_servers_obj)
cache_current_area = cache_json_data["current_area"]
cache_current_server = cache_json_data["current_server"]
cache_current_character = cache_json_data["current_character"]
cache_update_time = cache_json_data["update_time"]

if cache_current_area != -1:
	default_server_index = cache_current_area
if cache_current_server != -1:
	default_sub_server_index = cache_current_server
if cache_current_character != -1:
	default_character_index = cache_current_character

area_finished = False

def save_cache():
	time_stamp = time.time()
	cache = { \
		'current_area' : default_server_index, \
		'current_server' : default_sub_server_index, \
		'current_character' : default_character_index, \
		'update_time' : time_stamp \
	}
	util.info(cache)
	with open(cache_json_path, "w") as update_obj:
		json.dump(cache, update_obj, sort_keys=True, indent=4)

def get_current_server():
	if default_server_index >= len(servers):
		return None
	server = servers[default_server_index]
	# util.info("获取到当前大区:{}".format(server))
	return server

def get_current_sub_servers():
	current_server = get_current_server()
	if current_server == None:
		return None
	sub_servers = current_server["servers"]
	return sub_servers

def get_current_sub_server():
	current_servers = get_current_sub_servers()
	if current_servers == None:
		return None
	if default_sub_server_index >= len(current_servers):
		return None
	sub_server = current_servers[default_sub_server_index]
	# util.info("获取到当前服务器:{}".format(sub_server))
	return sub_server

def finish_current_server():
	global default_server_index
	global default_sub_server_index
	global default_character_index
	global area_finished
	if default_server_index + 1 >= len(servers):
		util.info("当前账号大区已经全部完成")
		area_finished = True
		return False
	default_server_index += 1
	default_sub_server_index = 0
	default_character_index = 0
	save_cache()
	util.info("大区缓存更新成功")
	return True

def finish_current_sub_server():
	global default_sub_server_index
	global default_character_index
	sub_servers = get_current_sub_servers()
	if sub_servers == None:
		return False
	if default_sub_server_index + 1 >= len(sub_servers):
		util.info("当前大区服务器已经全部完成")
		finish_current_server()
		return False
	default_sub_server_index += 1
	default_character_index = 0
	save_cache()
	util.info("服务器缓存更新成功")
	return True

def finish_current_character():
	global default_character_index
	sub_server = get_current_sub_server()
	if sub_server == None:
		return False
	count = sub_server["count"]

	if default_character_index + 1 >= count:
		util.info("当前服务器角色已经全部完成")
		finish_current_sub_server()
		return False
	default_character_index += 1
	save_cache()
	util.info("角色缓存更新成功")
	return True

def get_current_server_match_img():
	current_server = get_current_server()
	if current_server == None:
		return None
	match_img = current_server["match_img"]
	util.info("获取到大区 {} 的匹配图片".format(current_server["area_name"]))
	return match_img

def get_current_sub_server_match_img():
	sub_server = get_current_sub_server()
	if sub_server == None:
		return None
	util.info("获取到服务器 {} 的匹配图片".format(sub_server["name"]))
	return sub_server["match_img"]

def get_current_character_index():
	sub_server = get_current_sub_server()
	if sub_server == None:
		return None
	count = sub_server["count"]
	if default_character_index >= count:
		return None
	util.info("获取到角色下标：{}".format(default_character_index))
	return default_character_index

def get_server_img_path(img_name):
	img_path = os.getcwd() + "/img_servers/" + img_name
	return img_path

def click_with_images(images):
	if images == None:
		return False
	for img in images:
		img_path = get_server_img_path(img)
		target_btn = util.find_target_btn_in_screen(img_path)
		if target_btn == None:
			continue
		x = target_btn[0]
		y = target_btn[1]
		util.mouse_to(x, y)
		util.mouse_left_click()
		break
	return True


def login_area():
	area_image = get_current_server_match_img()
	result = click_with_images(area_image)
	if result:
		util.info("已经选择大区，等待进入...")
	else:
		util.info("没有可用大区")
	return result

def login_server():
	server_image = get_current_sub_server_match_img()
	result = click_with_images(server_image)
	if result:
		util.info("已经选择服务器，等待进入...")
	else:
		util.info("没有可用服务器选择")
	return result

def login_character():
	current_index = get_current_character_index()
	if current_index == None:
		return False
	choose_btn = util.find_target_btn_in_screen(choose_img_path)
	if choose_btn == None:
		return False
	offset = 10 + 73*current_index
	x = choose_btn[0]
	y = choose_btn[1] + offset
	util.mouse_to(x, y)
	util.mouse_left_click()
	util.info("已经选中角色")

	login_btn = util.find_target_btn_in_screen(login_img_path)
	if login_btn == None:
		return False

	x = login_btn[0]
	y = login_btn[1]
	util.mouse_to(x, y)
	util.mouse_left_click()
	util.info("已经点击进入游戏按钮")
	return True

def attack():
	attack_not_end = True
	count = 0;
	while attack_not_end:
		time_space = random.random() / 2.0
		sys.stdout.write("\rScreen scanning, waiting for the boss{}".format("."*(count % 6 + 1)))
		sys.stdout.flush()
		screen_path = util.screenshots()
		boss.attack()
		boss_alive = boss.find_boss_alive_center(screen_path)
		if boss_alive != None:
			boss.attack_alive
			attack_not_end = False
		os.remove(screen_path)
		count += 1
		time.sleep(time_space)
	return True

def exit_game():
	exit_btn = util.find_target_btn_in_screen(exit_img_path)
	if exit_btn == None:
		return False
	x = exit_btn[0]
	y = exit_btn[1]
	util.mouse_to(x, y)
	util.mouse_left_click()
	util.info("已经点击退出游戏按钮")
	finish_current_character()
	return True

# while area_finished == False:
# 	get_current_server_match_img()
# 	get_current_sub_server_match_img()
# 	get_current_character_index()
# 	finish_current_character()

# while area_finished:
# 	login_area()
# 	login_server()
# 	login_character()
# 	attack()
# 	exit_game()


