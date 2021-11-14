import serial
import serial.tools.list_ports as sp
import time

class toArduino:
    def __init__(self):
        self.ser_num = None
        
        port_list = sp.comports()
        connected = []
        
        if port_list != None:
            for i in port_list:
                connected.append(i.device)

            print("Connected COM ports :", str(connected))
            comport = i.device
            self.ser = serial.Serial(comport, 9600, timeout=1)

    def read(self):
        response = self.ser_num.read()
        while 1:
            if self.ser_num.readable():
                response = self.ser_num.readline()
                print(response.decode()[:len(response) - 1])
                break
            time.sleep(2)

    def send(self, text):
        print('get com :', text)
        self.ser.write(text.encode())