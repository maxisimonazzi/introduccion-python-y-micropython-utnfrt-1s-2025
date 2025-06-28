import machine
from neopixel import NeoPixel

#Crea un objeto led de la clase NeoPixel en el pin 16
led = NeoPixel(machine.Pin (13),16)

led[0]=(255, 0, 0)
led.write ()

led[1]=(0, 0, 255)
led.write ()

led[2]=(0, 255, 0)
led.write ()