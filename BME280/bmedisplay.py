############
# bmedisplay.py
# A simple weather station that displays the temperature, the pressure and the humidity
# read from a BME280 sensor onto a 7-segment 4 digit display with HT16K33 backpack/
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2019-08-26
# This software is licensed under the Eclipse Public License 2.0
############
from BME280 import BME280
from HT16K334x7 import HT16K334x7
import machine
import utime
import sys

def main() :
  if sys.platform == 'esp32':
    # BME280 sensor at address 0x70 on I2C bus with SCL on pin 4 and SDA on pin 0
    i2c = machine.SoftI2C(scl=machine.Pin(4), sda=machine.Pin(0))
  elif sys.platform == 'pyboard':
    # I2C(1) has SCL on pin X9 and SDA on pin X10 on the pyboard
    i2c = machine.I2C(1)
  else:
    print("Unknown platform: ", sys.platform)
    return
  bme = BME280(i2c, 0x76)
  display = HT16K334x7(i2c, 0x70)
  
  bme.normalmode()
  bme.filtering(BME280.IIR_8)
  bme.humidity_mode(BME280.OVRSAMP_4)
  bme.pressure_mode(BME280.OVRSAMP_4)
  bme.temperature_mode(BME280.OVRSAMP_4)

  display.on()
  # Clear all digits
  display.clear()
  
  while True:
    m = bme.measure()
    display.displayNumber(m['temp'], 1)
    utime.sleep_ms(1000)
    display.displayNumber(m['press']//100)
    utime.sleep_ms(1000)
    display.displayNumber(m['hum'], 1)
    utime.sleep_ms(1000)
    display.clear()
    utime.sleep_ms(1500)

main()
