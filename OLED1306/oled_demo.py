from oled128x64 import OLED128x64
from machine import Pin, I2C, SoftI2C
import sys

def main():
  if sys.platform == 'esp32':
    # Use software I2C bus with SCL on pin 4 and SDA on pin 0
    i2c = SoftI2C(scl=Pin(4), sda=Pin(0))
  elif sys.platform == 'pyboard':
    # Use I2C bus 1, with SCL on pin X9 and SDA on pin X10 on the pyboard
    i2c = I2C(1)
  else:
    print("Unknown platform: ", sys.platform)
    return

  s = OLED128x64(i2c)
  s.text("Hello World!", 0,  0)
  s.text("Micropython ", 0, 20)
  s.text(sys.version + " on " + sys.platform, 0, 30)
  s.text("Version {}.{}.{}".format(
                  sys.implementation[1][0],
                     sys.implementation[1][1],
                        sys.implementation[1][2]), 0, 40)
  s.show()

main()
