from machine import Pin, I2C
from time import sleep
from i2c_lcd import I2cLcd

# Configuración I2C para LCD
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # Dirección I2C 0x27

# Configuración LEDs
led_rojo = Pin(14, Pin.OUT)
led_amarillo = Pin(27, Pin.OUT)
led_verde = Pin(26, Pin.OUT)

def encender_rojo():
    led_rojo.on()
    led_amarillo.off()
    led_verde.off()
    lcd.clear()
    lcd.putstr("  ALTO  ")
    sleep(2)

def encender_amarillo():
    led_rojo.off()
    led_amarillo.on()
    led_verde.off()
    lcd.clear()
    lcd.putstr("PRECAUCION")
    sleep(2)

def encender_verde():
    led_rojo.off()
    led_amarillo.off()
    led_verde.on()
    lcd.clear()
    lcd.putstr("  AVANZA  ")
    sleep(3)

def semaforo():
    while True:
        encender_rojo()
        encender_amarillo()
        encender_verde()

# Ejecutar
semaforo()