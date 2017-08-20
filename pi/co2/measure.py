import RPi.GPIO as GPIO
import dht11
import time
import datetime

result_path = "/home/pi/co2/logs/sensor.log"

PIN_PWM = 21
PIN_DHT11 = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_PWM,GPIO.IN)
time.sleep(0.2)

sensor = dht11.DHT11(pin=PIN_DHT11)

def write_result(co2, temp, shi):
  now = datetime.datetime.now()
  obs_time = now.strftime("%Y-%m-%d %H:%M:%S")
  with open(result_path, "a") as f:
    f.write("{},{},{},{}\n".format(obs_time, co2, temp, shi))

def measure_temp():
  result = sensor.read()
  if result.is_valid():
    temp = result.temperature
    shi = result.humidity
  else:
    temp = -1
    shi = -1
  return temp, shi

def measure():
  while GPIO.input(PIN_PWM) == 1:
    last_high = time.time()
  while GPIO.input(PIN_PWM) == 0:
    last_low = time.time()
  while GPIO.input(PIN_PWM) == 1:
    last_high = time.time()
    
  span_high = (last_high - last_low) * 1000
  #print("span_high : " + str(span_high))
    
  while GPIO.input(PIN_PWM) == 0:
    last_low = time.time()
  while GPIO.input(PIN_PWM) == 1:
    last_high = time.time()
  while GPIO.input(PIN_PWM) == 0:
    last_low = time.time()

  span_low = (last_low - last_high) * 1000
  #print("span_low : " + str(span_low))

  #print("Cycle : " + str(span_high + span_low))

  co2 = 5000*(span_high - 2)/(span_high+span_low-4)
  temp, shi = measure_temp()
  write_result(co2, temp, shi)

while 1:
  measure()
  time.sleep(1)

GPIO.cleanup()

