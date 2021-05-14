############
# Test program for the BME280.py Micropython pyboard module.
#
# The 'main()' function uses an infinite loop to display the measurements.
#
# The 'main_timer()' function illustrates the use of the 'raw_measure' and
# the 'compensation' functions to read the measurements in the service routine
# of a timer and schedule its display in the REPL.
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2019 -- 2021-05-12
# This software is licensed under the Eclipse Public License 2.0
############
import machine
import utime
import micropython
from BME280 import BME280
import sys

# BME280 sensor
bme = None
# 8 bute buffer for storing raw measurement data
data_buffer = None

# Common intializations
def init() :
  global bme, data_buffer
  
  data_buffer = bytearray(8)
  if sys.platform == 'esp32':
    # BME280 sensor at address 0x70 on I2C bus with SCL on pin 4 and SDA on pin 0
    bme = BME280(machine.SoftI2C(scl=machine.Pin(4), sda=machine.Pin(0)), 0x76)
  elif sys.platform == 'pyboard':
    # BME280 sensor at address 0x70 on I2C bus 1
    # I2C(1) has SCL on pin X9 and SDA on pin X10 on the pyboard
    bme = BME280(machine.I2C(1), 0x76)
  else:
    print("Unknown platform: ", sys.platform)
    return
  bme.humidity_mode(BME280.OVRSAMP_16)
  bme.temperature_mode(BME280.OVRSAMP_16)
  bme.pressure_mode(BME280.OVRSAMP_16)
  bme.normalmode(BME280.HUNDREDTWENTYFIVE_MS)
  bme.filtering(BME280.IIR_16)

def print_measures(m):
  print("Temperature = {:5.2f} °C".format(m['temp'] / 100))
  print("Atmospheric pressure = {:7.2f} hPa".format(m['press'] / 100))
  # Compute the sea level pressure assuming an altitude of 80m
  qnh = BME280.sealevel_pressure(m, 80)
  print("Seal level pressure = {:7.2f} hPa".format(qnh / 100))
  # Compute the altitude (should be 80m) given the sea level pressure
  print("Altitude = {:d} m".format(round(BME280.altitude(m, qnh))))
  print("Relative humidity = {:5.2} %".format(m['hum'] / 100))

# Main program with an infinite loop to display measurements
def main() :
  global bme
  
  init()
  while True :
    print_measures(bme.measure())
    utime.sleep_ms(1000)
    print()

# Function to print the measurements that have been recorded
# in an interrupt service routine
def print_raw_measures(buffer) :
  global bme
  
  print_measures(bme.compensation(buffer))

# Interrupt service routine of our timer
# No memory allocation can be performed here, so we just get the raw
# data and store it in a preallocated buffer. Then we schedule the
# 'print_measures' function to be called as soon as possible in a
# normal context where memory can be allocated.
def timer_isr(t) :
  bme.raw_measure(data_buffer)
  micropython.schedule(print_raw_measures, data_buffer)

# Main program which sets up a timer to trigger a measurement
# every 1.5 second and display the results
def main_timer() :
  init()
  timer = machine.Timer(-1)
  timer.init(mode=machine.Timer.PERIODIC, period=1500, callback=timer_isr)

print("Either call 'bme280_test.main()' or 'bme280_test.main_timer()' to test the module")
