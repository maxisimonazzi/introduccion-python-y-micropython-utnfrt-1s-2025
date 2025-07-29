from machine import Pin, PWM, ADC, I2C
from time import sleep
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

# LCD
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# Pulsadores
buttons = [Pin(13, Pin.IN, Pin.PULL_UP),
           Pin(12, Pin.IN, Pin.PULL_UP),
           Pin(14, Pin.IN, Pin.PULL_UP),
           Pin(27, Pin.IN, Pin.PULL_UP)]

# LEDs PWM
led_pins = [2, 4, 16, 17]
leds = [PWM(Pin(pin), freq=1000) for pin in led_pins]

# Potenciómetro
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

# Servo
servo = PWM(Pin(18), freq=50)

# Mensajes LCD
mensajes = ["Agua seleccionada", "Fanta seleccionada", "Coca seleccionada", "Sprite seleccionada"]

# Mensaje inicial
lcd.clear()
lcd.putstr("Elija su bebida \n1=Agua 2=Fanta \n3=Coca 4=Sprite")

# Función mover servo (simula 30 cm ida y vuelta)
def mover_servo():
    for i in range(40, 115):
        servo.duty(i)
        sleep(0.01)
    for i in range(115, 40, -1):
        servo.duty(i)
        sleep(0.01)

# Bucle principal
while True:
    brillo = int((pot.read() / 4095) * 1023)  # 0–1023

    for i, btn in enumerate(buttons):
        if not btn.value():
            # Apagar todos los LEDs
            for led in leds:
                led.duty(0)

            # Encender el LED correspondiente con brillo
            leds[i].duty(brillo)

            # Mostrar mensaje en pantalla
            lcd.clear()
            lcd.putstr(mensajes[i])

            # Mover servo
            mover_servo()
            
            sleep(2)

            # Reset visual
            lcd.clear()
            lcd.putstr("Elija su bebida:\n1=Agua 2=Fanta\n3=Coca 4=Sprite")

            # Apagar LEDs
            for led in leds:
                led.duty(0)

    sleep(0.1)
