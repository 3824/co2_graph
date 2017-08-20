import serial
import RPi.GPIO as GPIO
import time

#ser = serial.Serial("/dev/ttyAMA0")
#serial_dev = '/dev/ttyS0'
serial_dev = "/dev/ttyAMA0"
ser = serial.Serial(serial_dev,
                    baudrate=9600,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1.0)

print "Serial Connected!"
ser.flushInput()
time.sleep(1)

while 1:
  print("start loop")
#  result = ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
#  time.sleep(.01)
#  resp = ser.read(7)
#  high = ord(resp[3])
#  low = ord(resp[4])
#  co2 = (high*256) + low
#  print ""
#  print ""
#  print "Co2 = " + str(co2)
#  time.sleep(1)
  result=ser.write("\xff\x01\x86\x00\x00\x00\x00\x00\x79")
  print(result)
  s=ser.read(9)
  if s[0] == "\xff" and s[1] == "\x86":
    print( {'co2': ord(s[2])*256 + ord(s[3])})
  break


