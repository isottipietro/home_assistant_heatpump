import serial
import time
import struct
import os
from colorama import Fore, Style

# Com Connection
def is_packet_ok(data):
	if len(data) > 0:
		Head = data [0:4]
		Lenght = data [20:24]
		Lenght_int = int.from_bytes(bytes.fromhex(Lenght), byteorder="little")
		Lenght_total = len(data)/2
		Trail = data[len(data)-2:len(data)]
		if Head == "aa55" and Trail == "3a":
			return True
		else:
			return False

def decode_packet(data):
	SensorValue = []
	Lenght = data [20:24]
	Lenght_int = int.from_bytes(bytes.fromhex(Lenght), byteorder="little")
	try:
		for i in range(26,Lenght_int*2-2,8):
			#print(Data_hex[i:i+8])
			value = struct.unpack('<f',bytes.fromhex(data [i+4:i+8])+bytes.fromhex(data [i:i+4]))
			Value, = value
			#	print(SensorName[int((i-26)/8)] + ":    " + str(Value))
			SensorValue.append(round(Value,1))
	except:
		print('ERROR: Decode exception')
	else:
		return SensorValue

class SerialMonitor:
	def __init__(self, ip, port):
		print('Initializing serial monitor...')
		os.system('socat pty,link=/dev/virtualcom0,raw tcp:'+ ip + ':' + port +'&')
		time.sleep(3)
		if not os.path.exists('/dev/virtualcom0'):
			print('Error creating serial connection')
			raise Exception('Error')
		else:
			time.sleep(2)
		try:
			self.device = serial.Serial('/dev/virtualcom0', 9600, timeout=0.1, inter_byte_timeout=0.1)
		except:
			print('ERROR: Serial error')
			quit()
		print('Created serial connection')
		self.device.reset_input_buffer()
		self.device.reset_output_buffer()

	def read_sensors(self):
		self.device.reset_input_buffer()
		while True:
			Data_hex = self.device.read(1200).hex()
			if is_packet_ok(Data_hex):
				Cmd = Data_hex [24:26]
				if  Cmd == "01":
					print("Packet received: " + Fore.GREEN + "OK" + Style.RESET_ALL)
					return Data_hex
	
	def read_parameters(self):
		self.device.reset_input_buffer()
		while True:
			Data_hex = self.device.read(1200).hex()
			if is_packet_ok(Data_hex):
				Cmd = Data_hex [24:26]
				if Cmd == "02":
					print("Packet received: " + Fore.GREEN + "OK" + Style.RESET_ALL)
					return Data_hex

	def test_connection(self):
		self.device.reset_input_buffer()
		i = 0
		while i < 100:
			Data = self.device.read(1200).hex()
			if is_packet_ok(Data):
				return True
			i += 1
		return False

try:
	pdc = SerialMonitor('192.168.188.4', '8899')
except:
	print('Impossible to initialize serial monitor, closing program.')
	quit()
else:
	while True:
		print('Wait for sensor state:')
		sensor = decode_packet(pdc.read_sensors())
		print(sensor)
		print('Wait for parameter:')
		params = decode_packet(pdc.read_parameters())
		print(params)
	#if Cmd == "02" and Head == "aa55" :
	#	try:
	#		print("=====================")
	#		print("HEAD: " + Head + " LENGHT: " + str(Lenght_int) + " COMMAND: " + Cmd)
			#SensorValue = []
			#for i in range(26,Lenght_int*2-2,8):
				#print(Data_hex[i:i+8])
			#	value = struct.unpack('<f',bytes.fromhex(Data_hex [i+4:i+8])+bytes.fromhex(Data_hex [i:i+4]))
			#	Value, = value
			#	print(SensorName[int((i-26)/8)] + ":    " + str(Value))
			#	SensorValue.append(round(Value,1))
	#	except:
	#		print('ERROR: Decode exception')
	#	else:
	#		print('ok')
			#upload(SensorValue)
			#time.sleep(30)

