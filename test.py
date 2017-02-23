import sys
import glob
import serial
from datetime import datetime


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    print "Platform: %s" % sys.platform
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except serial.SerialException as e:
            print "SerialException: %s" % e.message
        except IOError as e:
            print "IOError: %s" % e.message
    return result


if __name__ == '__main__':
    print "List all serial ports"
    print(serial_ports())


date = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
print "Nu is het:  " + date