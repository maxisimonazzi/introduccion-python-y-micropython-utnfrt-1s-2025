from machine import Pin, PWM, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep, sleep_ms

# Inicializo I2C para el LCD
i2c = SoftI2C(sda=Pin(19), scl=Pin(18), freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# Pines de botones
boton_verde    = Pin(27, Pin.IN, Pin.PULL_UP)
boton_azul     = Pin(14, Pin.IN, Pin.PULL_UP)
boton_amarillo = Pin(12, Pin.IN, Pin.PULL_UP)
boton_rojo     = Pin(13, Pin.IN, Pin.PULL_UP)

# PWM para el buzzer
buzzer = PWM(Pin(15))
buzzer.duty(0)
# Mostrar texto en LCD (limpia antes)
def mostrar(frase):
    lcd.clear()
    lcd.putstr(frase)

# Sonar buzzer
def sonar(freq, tiempo=0.3):
    buzzer.freq(freq)
    buzzer.duty(512)
    sleep(tiempo)
    buzzer.duty(0)

# Bucle principal
while True:
    if boton_verde.value() == 0:
        mostrar("Hola, como\nestas?")
        sonar(440)
        sleep_ms(300)

    if boton_azul.value() == 0:
        mostrar("Bienvenidos al\nmundo digital")
        sonar(523)
        sleep_ms(300)

    if boton_amarillo.value() == 0:
        mostrar("Codifica con\nimaginacion")
        sonar(587)
        sleep_ms(300)

    if boton_rojo.value() == 0:
        mostrar("Proyecto\nMicroPython")
        sonar(659)
        sleep_ms(300)
