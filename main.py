import time, os, random, sys
import util, boss

count = 0

time_space = 0
def start_loop():
	global count
	global time_space
	time_space = random.random() / 2.0
	# util.norml("---------------------")
	sys.stdout.write("\rScreen scanning, waiting for the boss{}".format("."*(count % 6 + 1)))
	sys.stdout.flush()
	# util.info("\rbegin the round {} screen scanning, time interval:{}".format(count, time_space))
	count += 1

def boss_end_loop(pic_path):
	os.remove(pic_path)
	global time_space
	time.sleep(time_space)
	return True

def boss_alive_end_loop(screen_path):
	util.info("Find boss in current screen, attack!")
	boss.attack_alive()
	util.info("Finish attack, redirect to character choose page")
	switch_result = boss.switch_character(screen_path)
	if switch_result == False:
		util.error("Failed exchange character")
		return False
	boss_end_loop(screen_path)
	return True

def loop_ocr():
	track = True
	# util.info("Screen scanning, waiting for the boss...")
	while track:
		start_loop()
		screen_path = util.screenshots()
		boss_alive = boss.find_boss_alive_center(screen_path)
		boss.attack()
		if boss_alive == None:
			track = boss_end_loop(screen_path)
		else:
			track = boss_alive_end_loop(screen_path)
		
loop_ocr()


