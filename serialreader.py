import serial, datetime

# This class reads the serial port
class Reader:
    # define the port name
    portname = 'COM4'
    # define the communication speed here. This should match your Arduino speed.
    # possible values are: 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200, 230400
    baudrate = 115200
    # make and configure the Serial Port
    com = serial.Serial()
    com.port = portname
    com.baudrate = baudrate
    com.timeout = 20
    com.setDTR(False) #prevents resetting the Arduino
    com.open()

    def read(self):
        port = self.com
        # starts a loop that receives a line of text, adds a timestamp and
        # yields the array so users can iterate over it like a list.
        while port.is_open:
            # create an array and add a timestamp
            data = str(datetime.datetime.now())
            data += ';' + port.readline().rstrip()
            # Yield the new line of data to iterate over
            yield data