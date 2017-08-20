import RPi.GPIO as GPIO
import dht11
import time
import datetime

PIN_NUM = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(PIN_NUM,GPIO.IN)
GPIO.cleanup()

sensor = dht11.DHT11(pin=PIN_NUM)

result = sensor.read()
if result.is_valid():
  print(result.temperature)
  print(result.humidity)

