from machine import Pin, PWM
from time import sleep
from hcsr04 import HCSR04

servo = PWM(Pin(19))
servo.freq(40)

sensor = HCSR04(trigger_pin=4, echo_pin=5)

while True:
     distancia = sensor.distance_cm()
    
     if distancia < 30:
        servo.duty_ns(1474326)
     else:
        servo.duty_ns(456703)
    
     sleep(2)