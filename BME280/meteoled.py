############
# bmedisplay.py
# A simple weather station that displays the temperature, the pressure and the humidity
# read from a BME280 sensor onto an OLED 128x64 display
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2021-05-11
# This software is licensed under the Eclipse Public License 2.0
############
from BME280 import BME280
from oled128x64 import OLED128x64
from machine import Pin, I2C, SoftI2C
import utime
import sys

def main() :
  if sys.platform == 'esp32':
    # Use software I2C bus with SCL on pin 4 and SDA on pin 0
    i2c = SoftI2C(scl=Pin(4), sda=Pin(0))
  elif sys.platform == 'pyboard':
    # Use I2C bus 1, with SCL on pin X9 and SDA on pin X10 on the pyboard
    i2c = I2C(1)
  else:
    print("Unknown platform: ", sys.platform)
    return

  bme = BME280(i2c, address=0x76)
  display = OLED128x64(i2c)
  
  bme.normalmode()
  bme.filtering(BME280.IIR_8)
  bme.humidity_mode(BME280.OVRSAMP_4)
  bme.pressure_mode(BME280.OVRSAMP_4)
  bme.temperature_mode(BME280.OVRSAMP_4)

  display.poweron()
  
  while True:
    display.fill(0)
    m = bme.measure()
    display.text("T {}.{} C".format(m['temp']//100, m['temp']%100), 0, 0)
    display.text("P {}.{} hPa".format(m['press']//100, m['press']%100), 0, 10)
    display.text("H {}.{} %".format(m['hum']//100, m['hum']%100), 0, 20)
    
    display.text("Micropython{}".format(sys.version), 0,40)
    display.text("Version {}.{}.{}".format(
                          sys.implementation[1][0],
                             sys.implementation[1][1],
                                sys.implementation[1][2]), 0, 50)
    display.show()
    utime.sleep_ms(1500)

main()
