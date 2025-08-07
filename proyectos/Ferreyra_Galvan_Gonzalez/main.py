from machine import Pin
from time import sleep

# Pines
sensor = Pin(22, Pin.IN, Pin.PULL_UP)   # Sensor magnético en GPIO 22
led = Pin(4, Pin.OUT)                  # LED de estado en GPIO 4

# Estado del sistema
sistema_armado = True

print("Sistema de alarma activado")

while True:
    if sistema_armado:
        if sensor.value() == 1:  
            print("Puerta cerrada - sistema armado")
            sleep(0.5)

        else:
            led.on()  
            print("Puerta abierta")
            led.on()
            sleep(0.1)
            led.off()
            sleep(0.1)

