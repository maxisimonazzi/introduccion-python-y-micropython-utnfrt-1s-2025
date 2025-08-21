from machine import Pin
from time import sleep, sleep_ms

#SEMÁFORO 1 
rojo1 = Pin(12, Pin.OUT)
amarillo1 = Pin(14, Pin.OUT)
verde1 = Pin(27, Pin.OUT)

# SEMÁFORO 2 
rojo2 = Pin(15, Pin.OUT)
amarillo2 = Pin(4, Pin.OUT)
verde2 = Pin(5, Pin.OUT)

#BOTÓN DE CRUCE
boton = Pin(18, Pin.IN, Pin.PULL_DOWN)

while True:
    
    verde1.value(1)
    rojo1.value(0)
    amarillo1.value(0)
    rojo2.value(1)
    amarillo2.value(0)
    verde2.value(0)
    sleep(5)

    if boton.value() == 1:  
        verde1.value(0); amarillo1.value(0); rojo1.value(1)
        verde2.value(0); amarillo2.value(0); rojo2.value(1)
        sleep(5)

    verde1.value(0)
    amarillo1.value(1)
    sleep(2)

    if boton.value() == 1:  
        verde1.value(0); amarillo1.value(0); rojo1.value(1)
        verde2.value(0); amarillo2.value(0); rojo2.value(1)
        sleep(5)

    amarillo1.value(0)
    rojo1.value(1)
    verde2.value(1)
    rojo2.value(0)
    sleep(5)

    if boton.value() == 1:  
        verde1.value(0); amarillo1.value(0); rojo1.value(1)
        verde2.value(0); amarillo2.value(0); rojo2.value(1)
        sleep(5)

    verde2.value(0)
    amarillo2.value(1)
    sleep(2)

    if boton.value() == 1:  
        verde1.value(0); amarillo1.value(0); rojo1.value(1)
        verde2.value(0); amarillo2.value(0); rojo2.value(1)
        sleep(5)

    amarillo2.value(0)
    rojo2.value(1)
    rojo1.value(0)
    verde1.value(1)
    sleep(5)

    if boton.value() == 1:  
        verde1.value(0); amarillo1.value(0); rojo1.value(1)
        verde2.value(0); amarillo2.value(0); rojo2.value(1)
        sleep(5)

