# i2c_lcd.py
from lcd_api import LcdApi
from machine import I2C
from time import sleep_ms

class I2cLcd(LcdApi):
    LCD_I2C_ADDR = 0x27
    LCD_NUM_LINES = 2
    LCD_NUM_COLUMNS = 16

    ENABLE_MASK = 0b00000100
    READ_WRITE_MASK = 0b00000010
    REGISTER_SELECT_MASK = 0b00000001

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self._backlight = 0x08
        self._write_byte(0)
        sleep_ms(20)
        self._write_init()
        super().__init__(num_lines, num_columns)
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)
        self.clear()

    def _write_byte(self, data):
        self.i2c.writeto(self.i2c_addr, bytes([data | self._backlight]))

    def _pulse_enable(self, data):
        self._write_byte(data | self.ENABLE_MASK)
        sleep_ms(1)
        self._write_byte(data & ~self.ENABLE_MASK)
        sleep_ms(1)

    def _write_init(self):
        cmds = [0x30, 0x30, 0x30, 0x20]
        for cmd in cmds:
            self._write_byte(cmd)
            self._pulse_enable(cmd)

    def hal_write_command(self, cmd):
        high = cmd & 0xF0
        low = (cmd << 4) & 0xF0
        self._write_byte(high)
        self._pulse_enable(high)
        self._write_byte(low)
        self._pulse_enable(low)

    def hal_write_data(self, data):
        high = data & 0xF0 | self.REGISTER_SELECT_MASK
        low = (data << 4) & 0xF0 | self.REGISTER_SELECT_MASK
        self._write_byte(high)
        self._pulse_enable(high)
        self._write_byte(low)
        self._pulse_enable(low)

    def hal_sleep_ms(self, ms):
        sleep_ms(ms)
