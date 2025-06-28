import machine
from neopixel import NeoPixel
from time import sleep_ms

#Crea un objeto led de la clase NeoPixel en el pin 16
led = NeoPixel(machine.Pin (13),16)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (138, 43, 226)
COLORS = (RED, YELLOW, GREEN, BLUE, INDIGO, VIOLET)

while True:
    for color in COLORS:
        for i in range(len(led)):
            led[i]=color
        led.write()
        sleep_ms(100)
