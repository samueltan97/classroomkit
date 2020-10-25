from RFID import RFID

def log(id):
	print(id)

scanner = RFID(log)
scanner.start()
