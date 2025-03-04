import sys
import drvCom
import win32file
import muPlay

PlayDrvName = "KbdMouFiltr"	
RecordDrvName = "KbLogger"

#avoid play
def Play(chars):
	drvCom.Play(PlayDrvName)
	hDev = win32file.CreateFile("\\\\.\\KbdMouFiltr", 0x80000000 , 0, None, 3, 0, None)
	
	if hDev == None :
		print("Failed to open handle to device")
		return

	i = 1
	while i < len(chars):
		muPlay.sendInputToDev(hDev, chars[i], chars[i+1])
		i += 2
	drvCom.SysOp(PlayDrvName, drvCom.STOP_SYS)

if( len(sys.argv) < 3):
	print("Usage .\\screenRec <char>")
	exit()

print("0: Record \n1: Play \n2: Exit")
c = sys.stdin.read(1)

if(c == '0'):
	drvCom.Record(RecordDrvName)
elif(c == '1'):
	Play(sys.argv)
elif(c == '2'):
	print("Quitting")
else:
	print("Wrong input")
