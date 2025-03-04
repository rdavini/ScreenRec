import drvCom
import time
import screen
from char import Char
from random import randrange

monitoredChars = []

def muHelper(hDev, place):
	print(f"place: {place} ")
	drvCom.StartAction(hDev, place)

	i = 0
	while(True) :
		if screen.cmpImgs("no_warp.png", (925, 618, 200, 8), 0.9, 1) > 0.9 :
			drvCom.StartAction(hDev, "CancelMuHelper")
			return False

		max_val = screen.cmpImgs('no_spot.png', (842, 263, 20, 18), 0.9, 1)
		max_val2 = screen.cmpImgs('yes_spot.png', (842, 263, 20, 18), 0.9, 1)
		
		print("no spot: ", max_val)
		print("yes spot: ", max_val2)
		
		if max_val > 0.8 and max_val > max_val2:
			print("MuHelper no free spot")
			return False
		elif max_val2 > 0.8 and max_val2 > max_val:
			time.sleep(1)
			i+=1
			print(f"Searching spot i: {i}")
			if i> 4:
				print("Spot found")
				return True

def getFirstFreeSrv():
	f = open(f"vinputs\\ServerPos.txt", "rb")
	if f == None:
		print("ServerPos file not found")
		return
	
	ServerPos = f.read()
	
	time.sleep(1)
	ret = screen.cmpImgs('servers\\servers_full.png', (1090, 559, 190, 232), 0.9, 1)
	print(f"Ref {ret}")
	if ret > 0.9 :
		print("Servers full")
		return
	num = 6	
	while(num <= 14):
		max_val = screen.cmpImgs(f"servers\\mid{num}_not_full.png", (1090, 560 + (num-6)*25, 190, 25), 0.9, 1)
		max_val2 = screen.cmpImgs(f"servers\\mid{num}_full.png", (1090, 560 + (num-6)*25, 190, 25), 0.9, 1)

		print("max val: ", max_val)
		print("max val2: ", max_val2)

		if max_val > 0.8 and max_val > max_val2:
			print(f"Server {num} empty")
			return num
		elif max_val2 > 0.8 and max_val2 > max_val:
			print(f"Server {num} full")
			num += 1
		else:
			time.sleep(2)
			print("Trying again")

def sendInputToDev(hDev, char, action):
	#open handle to device
	#maybe move the open handle to drvCom
	if hDev == None:
		print("Failed to open handle to device")
		return
	
	f = open(f"vinputs\\{char}\\{action}.txt", "rb")
	
	if f == None :
		print("Failed to open file")

	#parse file
	#0 start action
	#1 is action finished
	#2 sleep
	#3 end of file
	#4 connectToEmptySrv
	#while True:
	lines = f.readlines()
	for i in range(0, len(lines)) :
		print(lines[i].decode()[0])
		if lines[i].decode()[0] == '#':
			continue
		str_line = lines[i].split()
		cmd = int(str_line[0])
		fargs = str_line[1:]
		match(cmd):
			case 0: #startAction
				drvCom.StartAction(hDev, fargs[0].decode())
			case 1: #isActionFinished
				#it should search for ',' and not use -4
				ret = screen.cmpImgs(fargs[0].decode(), tuple(map(int, fargs[1].decode().split(','))), float(fargs[2]), int(fargs[3]))
				
				#this should be generic such as an goto inside the file
				if ret < float(fargs[2]):
					drvCom.StartAction(hDev, "login2Minimize")
					break
			case 2: #2 sleep
				time.sleep(int(fargs[0]))
			case 3: #end of file
				print("End of file")
				break
			case 4:
				if fargs[0].decode() == "connect_srv":
					time.sleep(0.5)
					#freeSrv = (len(fargs) > 1 and int(fargs[1])) or getFirstFreeSrv()
					#if freeSrv is None :
					#	print("All srvs are full")
					#	freeSrv = randrange(6, 14)
					freeSrv = 10
					drvCom.StartAction(hDev, f"connect_mid{freeSrv}")
				else :					
					spots = fargs[1:]
					j = 0
					while j < len(spots) and muHelper(hDev, spots[j].decode()) == False:
						j += 1
			case 5: #analyse screenshot
				Monitor(hDev)
			case 6:
				PrintMonitoredRes()
			case _:
				print(f"Unexpected action value {str_line}")
	f.close()


def GetCoords(pl_id):
	comma_place = [821, 812, 803]
	time.sleep(2)
	similarity = 0
	comma_id = 0

	#get y number of digits
	for i in range(0, 3):
		max_val = screen.cmpImgs(f'coords\\y{i}.png', (comma_place[i], 272, 5, 14), 0.9, 1)
		if max_val > similarity:
			similarity = max_val
			comma_id = i
			
	print(f"comma_id: {comma_id}")
	
	#get y
	y_pos = [826, 816, 807]
	for j in range(0, comma_id + 1):
		for n in range(0, 10):
			if screen.cmpImgs(f'coords\\numbers\\{n}.png', (y_pos[j], 261, 10, 18), 0.8, 1) > 0.8:
				print(f"y_{j}_{n}")
				#if coord_type == 'x':
				 #   monitoredChars[pl_id].x  += str(n)
				#else:
				monitoredChars[pl_id].y  += str(n)
				break
			
	#get x

	'''
	coord_xo = 687 if coord_type == 'x' else 706

	for i in range(0, 3):
		threshold = 0
		num_id  = -1
		for num in range (0, 9):
			similarity  = screen.cmpImgs(f'coords\\{num}.png', (coord_xo + i*6 , 256, 5, 14), 0.9, 1)
			if similarity > threshold:
				threshold = similarity
				num_id = num
		if coord_type == 'x':
			monitoredChars[pl_id].x  += str(num_id)
		else:
			monitoredChars[pl_id].y  += str(num_id)
	'''

def Monitor(hDev):
	print("Monitor")
	time.sleep(2)
	
	if screen.cmpImgs(f'mu_client.png', (560, 220 , 57, 30), 0.9, 1) < 0.9:
		return

	drvCom.StartAction(hDev, "kbd_c")
	time.sleep(1)

	f = open(f"vinputs\\config\\monitoredChars.txt")
	charNames = f.read().split()
	f.close()
	if 0 == len(monitoredChars):
		for name in charNames:
			monitoredChars.append(Char(name, Char.PL_FARM, False, False, False, False, False, 'unknown', '', ''))	

	#get pl
	max_val = 0
	pl_id = -1
	i = 0
	for monitoredChar in monitoredChars:
		similarity  = screen.cmpImgs(f'players\\pl_{monitoredChar.name}.png', (675, 288, 65, 13), 0.9, 1)
		if similarity > max_val :
			max_val = similarity
			pl_id = i

		i += 1
	monitoredChars[pl_id].connected = True

	drvCom.StartAction(hDev, "kbd_c")
	time.sleep(1)

	#get map
	f = open(f"vinputs\\config\\maps.txt")
	maps = f.read().split()
	f.close()
	threshold = 0

	for map in maps:
		similarity  = screen.cmpImgs(f'maps\\{map}.png', (622, 256, 65, 14), 0.9, 1)
		if similarity > threshold and similarity> 0.8:
			threshold = similarity
			monitoredChars[pl_id].spot = map

	#get coords
	GetCoords(pl_id)

	time.sleep(1)
	drvCom.StartAction(hDev, "kbd_a")
	time.sleep(1)

	max_val  = screen.cmpImgs('no_durability_skill.png', (577, 569, 25, 35), 0.8, 1)
	max_val2  = screen.cmpImgs('yes_durability_skill.png', (577, 569, 25, 35), 0.8, 1)

	if max_val2 > max_val:
		monitoredChars[pl_id].imp_expected = True

	drvCom.StartAction(hDev, "kbd_a")
	time.sleep(1)

	drvCom.StartAction(hDev, "kbd_v")
	time.sleep(1)

	#get zen status
	max_val = 0
	no_zen_cnt = 0
	for i in range(0, 3):
		if screen.cmpImgs('no_zen.png', (1153, 752, 6, 10), 0.9, 1) > 0.8:
			no_zen_cnt += 1

	monitoredChars[pl_id].zen = True if no_zen_cnt < 2 else False

	#check imp
	for i in range(0, 3):
		max_val  = screen.cmpImgs('no_imp.png', (1110, 322, 45, 45), 0.8, 1)
		max_val2  = screen.cmpImgs('yes_imp.png', (1110, 322, 45, 45), 0.8, 1)
		max_val3 = screen.cmpImgs('yes_imp_red.png', (1110, 322, 45, 45), 0.8, 1)

		if max_val < max_val2 or max_val < max_val3 :
			monitoredChars[pl_id].imp = True
			break

	drvCom.StartAction(hDev, "kbd_v")
	time.sleep(1)

	#check if pl is alive, market
	for i in range(0, 3):
		max_val  = screen.cmpImgs('on_spot.png', (796, 262, 20, 20), 0.8, 1)
		max_val2 = screen.cmpImgs('off_spot.png', (796, 262, 20, 20), 0.8, 1)
		if max_val > max_val2:
			monitoredChars[pl_id].alive = True
			break
	#if monitoredChars[pl_id].alive == False:
	#	drvCom.StartAction(hDev, 'muHelperOldFire')
	#if max_val > 0.8 else drvCom.StartAction(hDev, 'muHelperElb3Low') if monitoredChars[pl] else print("market player")
	time.sleep(1)	

def PrintMonitoredRes():
	header = ["name", "connected", "alive", "zen", "imp_expected", "imp", "spot", "x", "y"]
	for h in header:
		print(f"{h: >10}", end=" ")
	
	print()

	for char in monitoredChars:
		print(f"{char.name: >10} {char.connected: >10} {char.alive: >10} {char.zen: >10} {char.imp_expected: >10} {char.imp: >10} {char.spot: >10} {char.x: >10} {char.y: >10}")
		