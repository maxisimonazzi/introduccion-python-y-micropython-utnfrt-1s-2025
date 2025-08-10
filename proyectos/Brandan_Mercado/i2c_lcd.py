from lcd_api import LcdApi
from machine import I2C
import time

class I2cLcd(LcdApi):
    MASK_RS = 0x01
    MASK_RW = 0x02
    MASK_E  = 0x04
    MASK_BACKLIGHT = 0x08

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = self.MASK_BACKLIGHT
        time.sleep_ms(20)
        self.hal_write_init_nibble(0x03)
        time.sleep_ms(5)
        self.hal_write_init_nibble(0x03)
        time.sleep_ms(1)
        self.hal_write_init_nibble(0x03)
        self.hal_write_init_nibble(0x02)
        LcdApi.__init__(self, num_lines, num_columns)
        self.hal_write_command(self.LCD_FUNCTION | self.LCD_FUNCTION_2LINES)
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)
        self.clear()

    def hal_write_init_nibble(self, nibble):
        byte = (nibble << 4) & 0xF0
        self.hal_write_byte(byte)

    def hal_backlight_on(self):
        self.backlight = self.MASK_BACKLIGHT
        self.hal_write_byte(0)

    def hal_backlight_off(self):
        self.backlight = 0x00
        self.hal_write_byte(0)

    def hal_write_command(self, cmd):
        self.hal_write(cmd, 0)

    def hal_write_data(self, data):
        self.hal_write(data, self.MASK_RS)

    def hal_write(self, data, mode):
        high = data & 0xF0
        low = (data << 4) & 0xF0
        self.hal_write_byte(high | mode)
        self.hal_write_byte(low | mode)

    def hal_write_byte(self, byte):
        self.i2c.writeto(self.i2c_addr, bytes([byte | self.backlight | self.MASK_E]))
        time.sleep_us(500)
        self.i2c.writeto(self.i2c_addr, bytes([byte | self.backlight]))
        time.sleep_us(500)