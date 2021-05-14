############
# ESP32_BME280.py a Micropython ESP32 driver for the TMP36 temperature sensor.
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2019-08-01 -- 2021-05-13
# This software is licensed under the Eclipse Public License 2.0
############
import machine
import utime
import sys

class TMP36:
  """
  A class to read the temperature using a TMP36 sensor.
  
  Bottom view of the TMP36 (pin side)
     _________
    | 1  2  3 |
    \         /
     ---------
     
    1 = Vs   2 = Out   3 = Gnd

    The output is 750mV at 25°C with 10mV/1°C
    The range is -40°C (100mV) to 125°C (1.75V)

  Example: temp = TMP36(32)
           print(temp.temp()
  """
  offset = 750       # 750mV at 25°C
  refTemp = 25
  if sys.platform == 'esp32':
    vRef = 2000        # input scale 0 - 2.0V (calibrated on my ESP32)
    resolution = 4095  # 12 bits
  else:
    vRef = 3300        # input scale 0 - 3.3V
    resolution = 65535 # 16 bits
  
  def __init__(self, pin):
    """Initialize a sensor on the pin.
       The pin must be able to perform ADC.
    """
    if (sys.platform == 'esp32' and not pin in range(32,40)) :
      raise ValueError("ADC pins on the ESP32 are from 32 to 39")
    self.pin = machine.ADC(machine.Pin(pin))
    if sys.platform == 'esp32':
      self.pin.atten(machine.ADC.ATTN_6DB)    # Range is 0 - 2.00 V
      self.pin.width(machine.ADC.WIDTH_12BIT) # Max resolution is 12 bits
  
  def measure(self):
    """Perform one measure, the result is in tenth of °C to avoid using floats."""
    if sys.platform == 'esp32':
      val = self.pin.read()
    else:
      val = self.pin.read_u16()
    volt = (val * TMP36.vRef) // TMP36.resolution
    return 10*TMP36.refTemp + (volt - TMP36.offset)

  def temp(self):
    """Return the average of a series of measures, in tenth of °C."""
    temp = 0
    # Average of 10 measures
    for i in range(10):
      v = self.measure()
      temp += v
      utime.sleep_ms(15)
    return temp // 10

