############
# HCSR04_test.py test/demo of the HCSR04 module
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2019-08-28 -- 2021-05-13
# This software is licensed under the Eclipse Public License 2.0
############
from HCSR04 import HCSR04
import utime
import machine

import sys

if sys.platform == 'esp32':
	trig = 12
	echo = 13
	tmp36 = 32
	i2c = machine.I2C(0) # SCL = 18, SDA = 19
elif sys.platform == 'pyboard':
	trig = 'X11'
	echo = 'X12'
	tmp36 = 'Y12'
	i2c = machine.I2C(1) # SCL = X9, SDA = X10
else:
	print("Unknown platform: ", sys.platform)
	sys.exit()

def main() :
  telemeter = HCSR04(trig, echo)
  
  while True :
    print('D:', telemeter.measure(), 'cm')
    utime.sleep_ms(500)

def main_tmp() :
  from TMP36 import TMP36
  
  tmp = TMP36(tmp36)
  telemeter = HCSR04(trig, echo, tmp36 = tmp)
  
  while True :
    print('D:', telemeter.measure(), 'cm')
    print('T:', tmp.measure()/10, '°C')
    utime.sleep_ms(500)

def main_bme() :
  from BME280 import BME280
  
  bme = BME280(i2c)
  bme.normalmode()
  telemeter = HCSR04(trig, echo, bme280 = bme)
  
  while True :
    print('D:', telemeter.measure(), 'cm')
    print('T:', bme.measure()['temp']/100, '°C')
    utime.sleep_ms(500)

# Try one of these according to the temperature sensor you have
print("Try one of HCSR04_test.main(), HCSR04_test.main_tmp(), or HCSR04_test.main_bme()")
