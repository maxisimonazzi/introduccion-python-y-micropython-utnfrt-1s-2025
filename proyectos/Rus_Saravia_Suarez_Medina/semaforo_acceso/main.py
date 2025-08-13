from machine import Pin
from time import sleep

ledr = Pin(18, Pin.OUT)
leda = Pin(19, Pin.OUT)
ledv = Pin(21, Pin.OUT)  
ledb = Pin(33, Pin.OUT)

sensor= Pin(34, Pin.IN, Pin.PULL_UP)

estado = 0			
contador = 0

while True:
    #Control luz blanca
    if sensor.value() == 1:
        ledb.on()
    else:
        ledb.off()

    #Control del semáforo
    if estado == 0: 
        ledr.on()
        leda.off()
        ledv.off()
        contador += 1
        if contador >= 3: 
            estado = 1
            contador = 0

    elif estado == 1: 
        ledr.off()
        leda.on()
        ledv.off()
        contador += 1
        if contador >= 1:
            estado = 2
            contador = 0

    elif estado == 2:  # Verde
        ledr.off()
        leda.off()
        ledv.on()
        contador += 1
        if contador >= 5:  # 3 segundos en verde
            estado = 0
            contador = 0

    sleep(1)
