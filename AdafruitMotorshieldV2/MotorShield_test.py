############
# MotorShield_test.py test/demo of the adamotshv2fb module
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2018-02-25 -- 2021-05-13
# This software is licensed under the Eclipse Public License 2.0
############
import pca9685fb
import adamotshv2fb
import sys
import utime

if sys.platform == 'pyboard':
  import pyb
  # On the pyboard, use I2C bus 1 (SCL=X9, SDA=X10)
  i2c = pyb.I2C(1, pyb.I2C.MASTER)
elif sys.platform == 'esp32': 
  import machine
  # On the ESP32, use I2C bus 0 (SCL=18, SDA=19)
  i2c = machine.I2C(0)
else:
  print("Unknown platform: ", sys.platform)
  sys.exit()

# Create a PCA9685 on the I2C bus
pca = pca9685fb.PCA9685(i2c)
# Start the PWM timers
pca.start()

# Create a stepper motor on ports M1 and M2
s = adamotshv2fb.Stepper(pca, 1)

print('Full steps forward')
# fullStep(# of steps, # of ms between steps)
s.fullStep(200, 50)
print('Full steps backwards')
s.fullStep(-200, 50)

print('Half steps forward')
# halfStep(# of steps, # of ms between steps)
s.halfStep(400, 20)
print('Half steps backwards')
s.halfStep(-400, 20)

print('Micro steps forward')
# microStep(# of steps, # of ms between steps)
s.microStep(3200, 5)
print('Micro steps backwards')
s.microStep(-3200, 5)

print('Release stepper')
# release the motor (let it turn freely)
s.release()

# Create a DC motor on port M3
m = adamotshv2fb.DCMotor(pca, 3)
print('Half throttle')
# Make it run at half throttle
m.throttle(2048)
utime.sleep_ms(2000)
print('Reverse')
# Reverse the rotation
m.throttle(-2048)
utime.sleep_ms(2000)
print('Brake')
# Brake (this stops the motor more quickly than m.throttle(0)
m.brake()
utime.sleep_ms(1000)

print('Full throttle')
# Make the motor run at full speed
m.throttle(4096)
utime.sleep_ms(2000)
print('Stop without braking')
# Let it stop by itself (without braking)
m.throttle(0)
utime.sleep_ms(1000)

# Create a servo motor on PWM output 0 with the default timing settings
s = adamotshv2fb.Servo(pca, 0)
# Make the servo move
print('Position 0')
s.position(0)
utime.sleep_ms(1000)
print('Position 180')
s.position(180)
utime.sleep_ms(1000)
print('Position 90')
s.position(90)
utime.sleep_ms(1000)
print('Position 0')
s.position(0)
utime.sleep_ms(1000)
print('Release servo')
# Release the servo (it may vibrate a lot at the default 200Hz PWM frequency)
s.release()
