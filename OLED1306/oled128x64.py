from ssd1306x import SSD1306_I2C

class OLED128x64(SSD1306_I2C):
	def __init__(self, i2c):
		super().__init__(128, 64, i2c)
