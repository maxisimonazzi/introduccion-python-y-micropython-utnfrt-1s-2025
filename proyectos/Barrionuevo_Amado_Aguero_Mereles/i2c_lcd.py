# i2c_lcd.py
from lcd_api import LcdApi
from machine import I2C
import time

class I2cLcd(LcdApi):
    # Controladores del LCD I2C
    MASK_RS = 0x01
    MASK_RW = 0x02
    MASK_E = 0x04
    MASK_BACKLIGHT = 0x08

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.i2c.writeto(self.i2c_addr, bytearray([0]))
        self.backlight = self.MASK_BACKLIGHT
        time.sleep_ms(20)
        self.hal_write_init_nibble(0x03)
        time.sleep_ms(5)
        self.hal_write_init_nibble(0x03)
        time.sleep_ms(1)
        self.hal_write_init_nibble(0x03)
        time.sleep_ms(1)
        self.hal_write_init_nibble(0x02)
        time.sleep_ms(1)
        super().__init__(num_lines, num_columns)

    def hal_write_init_nibble(self, nibble):
        self.hal_write_byte(nibble << 4)

    def hal_backlight_on(self):
        self.backlight = self.MASK_BACKLIGHT
        self.i2c.writeto(self.i2c_addr, bytearray([self.backlight]))

    def hal_backlight_off(self):
        self.backlight = 0
        self.i2c.writeto(self.i2c_addr, bytearray([self.backlight]))

    def hal_write_command(self, cmd):
        self.hal_write_byte(cmd & 0xF0)
        self.hal_write_byte((cmd << 4) & 0xF0)

    def hal_write_data(self, data):
        self.hal_write_byte((data & 0xF0) | self.MASK_RS)
        self.hal_write_byte(((data << 4) & 0xF0) | self.MASK_RS)

    def hal_write_byte(self, byte):
        self.i2c.writeto(self.i2c_addr, bytearray([byte | self.backlight | self.MASK_E]))
        time.sleep_us(1)
        self.i2c.writeto(self.i2c_addr, bytearray([(byte | self.backlight) & ~self.MASK_E]))
        time.sleep_us(50)
