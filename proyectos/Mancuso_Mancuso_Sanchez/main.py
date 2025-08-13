from machine import Pin, ADC, PWM
from time import sleep_ms


servoX = PWM(Pin(5))
servoX.freq(50)
servoY = PWM(Pin(18))
servoY.freq(50)
adc = ADC(Pin(13))



joyX = ADC (Pin(25))
joyY = ADC (Pin(33))
joyX.atten(ADC.ATTN_11DB)  
joyY.atten(ADC.ATTN_11DB)

deadZone = 500

anguloX = 90
anguloY = 90

def mover_servo(servo, angle):
    min_us = 500
    max_us = 2500
    us = min_us + (max_us - min_us) * angle / 180
    servo.duty_ns(int(us*1000))
 
mover_servo(servoX, anguloX)
mover_servo(servoY, anguloY)

while True:
    ejeX = joyX.read()
    ejeY = joyY.read()

    print("X:", ejeX, " Y:", ejeY)

    if ejeX < (2048 - deadZone) and anguloX < 180:
        anguloX += 1
    elif ejeX > (2048 + deadZone) and anguloX > 0:
        anguloX -= 1
    mover_servo(servoX, anguloX)

    if ejeY < (2048 - deadZone) and anguloY < 180:
        anguloY += 1
    elif ejeY > (2048 + deadZone) and anguloY > 0:
        anguloY -= 1
    mover_servo(servoY, anguloY)

    sleep_ms(15)