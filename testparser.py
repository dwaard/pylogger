import parser
import os
import serial, datetime


p = parser.build()

l1 = "2025-04-09 20:36:36.494404;25.00;21.30;100.00;5.00"
l2 = "2025-04-09 20:36:sxddfsdfflsd36.494404;25.00;21.30;100.00;5.00"

valid, data = p.parse(l2)

print("Bytesize")
print(serial.FIVEBITS)
print(serial.SIXBITS)
print(serial.SEVENBITS)
print(serial.EIGHTBITS)

print("Parity")
print(serial.PARITY_NONE)
print(serial.PARITY_EVEN)
print(serial.PARITY_ODD)
print(serial.PARITY_MARK)
print(serial.PARITY_SPACE)

print("Stopbits")
print(serial.STOPBITS_ONE)
print(serial.STOPBITS_ONE_POINT_FIVE)
print(serial.STOPBITS_TWO)

print("XonXoff")
print(serial.XON)
print(serial.XOFF)
