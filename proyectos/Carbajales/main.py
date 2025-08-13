import dht
from machine import Pin, I2C, PWM
import time
from i2c_lcd import I2cLcd

# Configuración del DHT22
sensor = dht.DHT22(Pin(15))

# Configuración LCD I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
LCD_I2C_ADDR = 0x27  # Cambia a 0x3F si tu LCD usa otra dirección
lcd = I2cLcd(i2c, LCD_I2C_ADDR, 2, 16)

# Configuración LED y buzzer
led = Pin(2, Pin.OUT)
buzzer = PWM(Pin(4))

TEMP_LIMITE = 30  # °C para alarma

def alarma():
    buzzer.freq(1000)
    buzzer.duty(512)
    time.sleep(0.5)
    buzzer.duty(0)

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        lcd.clear()
        if temp > TEMP_LIMITE:
            lcd.move_to(0, 0)
            lcd.putstr("Temperatura Alta")
            lcd.move_to(0, 1)
            lcd.putstr("T:{:.1f}C H:{:.1f}%".format(temp, hum))
            led.on()
            alarma()
        else:
            lcd.move_to(0, 0)
            lcd.putstr("Temp: {:.1f}C".format(temp))
            lcd.move_to(0, 1)
            lcd.putstr("Hum: {:.1f}%".format(hum))
            led.off()
            buzzer.duty(0)

        print("Temp: {:.1f} C | Hum: {:.1f} %".format(temp, hum))

    except OSError:
        print("Error al leer el sensor")

    time.sleep(2)
