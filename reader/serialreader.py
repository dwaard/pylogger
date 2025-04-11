import os
import serial, datetime

class SerialReader:

    def __init__(self):
        self.com = serial.Serial()
        self.com.port = os.getenv('SERIALPORT', 'COM1')
        self.com.baudrate = int(os.getenv('SERIALBAUDRATE', 9600))
        self.com.bytesize = int(os.getenv('SERIALBITESIZE', 8))
        self.com.parity = os.getenv('SERIALPARITY', 'N')
        self.com.stopbits = float(os.getenv('SERIALSTOPBITS', 1))
        self.com.timeout = int(os.getenv('SERIALTIMEOUT', 20))
        #TODO self.com.xonxoff = ?
        #TODO self.com.rtscts = ?
        #TODO self.com.dsrdtr = ?
        #TODO: can we remove: self.com.setDTR(os.getenv('SERIALDTR', False))
        self.com.open()
        self.com.reset_input_buffer()
        

    def read(self):
        port = self.com
        #port.open()
        while port.is_open:
            data = str(datetime.datetime.now())
            data += ';{}'.format(port.readline().rstrip().decode("utf-8"))
            yield data