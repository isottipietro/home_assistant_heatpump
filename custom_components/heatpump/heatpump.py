import serial
#import time
import struct
import os
from colorama import Fore, Style
import asyncio


# Com Connection
async def is_packet_ok(data):
	if len(data) > 0:
		Head = data [0:4]
		Lenght = data [20:24]
		Lenght_int = int.from_bytes(bytes.fromhex(Lenght), byteorder="little")
		Trail = data[len(data)-2:len(data)]
		if Head == "aa55" and Trail == "3a" and Lenght_int < len(data)/2:
			return True
		else:
			return False

async def decode_packet(data):
	SensorValue = []
	Lenght = data [20:24]
	Lenght_int = int.from_bytes(bytes.fromhex(Lenght), byteorder="little")
	try:
		for i in range(26,Lenght_int*2-2,8):
			value = struct.unpack('<f',bytes.fromhex(data [i+4:i+8])+bytes.fromhex(data [i:i+4]))
			Value, = value
			SensorValue.append(round(Value,1))
	except:
		print('ERROR: Decode exception')
	else:
		return SensorValue
	
async def encode_packet(data):
	# TODO encode packet from int to hex to byte
	return

class SerialMonitor:
	async def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.serial = None
	
	async def open(self):
		print('Initializing serial monitor...')
		os.system('socat pty,link=/dev/virtualcom0,raw tcp:'+ self.ip + ':' + self.port +'&')
		await asyncio.sleep(3)
		if not os.path.exists('/dev/virtualcom0'):
			print('Error creating serial connection')
			raise Exception('Error')
		try:
			self.serial = serial.Serial('/dev/virtualcom0', 9600, timeout=0.1, inter_byte_timeout=0.1)
		except:
			print('ERROR: Serial error')
			quit()
		else:
			print('Created serial connection')
			self.serial.reset_input_buffer()
			self.serial.reset_output_buffer()

	async def read_sensors(self):
		self.serial.reset_input_buffer()
		while True:
			Data_hex = self.serial.read(1200).hex()
			if is_packet_ok(Data_hex):
				Cmd = Data_hex [24:26]
				if  Cmd == "01":
					#print("Packet received: " + Fore.GREEN + "OK" + Style.RESET_ALL)
					return Data_hex
	
	async def read_parameters(self):
		self.serial.reset_input_buffer()
		while True:
			Data_hex = self.serial.read(1200).hex()
			if is_packet_ok(Data_hex):
				Cmd = Data_hex [24:26]
				if Cmd == "02":
					#print("Packet received: " + Fore.GREEN + "OK" + Style.RESET_ALL)
					return Data_hex

	async def read(self):
		self.serial.reset_input_buffer()
		while True:
			Data_hex = self.serial.read(1200).hex()
			if is_packet_ok(Data_hex):
				return Data_hex

	async def test_connection(self):
		if self.serial is None:
			open()
		self.serial.reset_input_buffer()
		while True: ## TODO timeout per test connessione fallito
			Data_hex = self.serial.read(1200).hex()
			if is_packet_ok(Data_hex):
				return True


if False:
	pdc = SerialMonitor('192.168.188.4', '8899')
	print('Testing connection...')
	if pdc.test_connection():
		print('Connection ok')
	while True:
		print('Wait for sensor state:')
		sensor = decode_packet(pdc.read_sensors())
		print(sensor)
		print('Wait for parameter:')
		params = decode_packet(pdc.read_parameters())
		print(params)
