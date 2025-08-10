from machine import Pin, PWM
from time import sleep, sleep_us, ticks_us, ticks_diff


servo = PWM(Pin(19))
servo.freq(50)
#Sensor
trig = Pin(13, Pin.OUT)
echo = Pin(12, Pin.IN)

#funcion para medir la distancia
def medir_distancia():
     tiempo1 = 0
     tiempo2 = 0

     #enviar señal al "Trig"
     trig.value(0) 
     sleep_us(2) #se esperan 2ms para que se estabilice en nivel bajo antes de ponerlo en nivel alto y evitar fallas
     trig.value(1)
     sleep_us(10) #se mantiene la señal por 10us
     trig.value(0)


#tiempo que tarda en activarse
     while echo.value()==0:
        tiempo1 = ticks_us() #tiempo de inicio
    
#tiempo que dura activo
     while echo.value()==1:
        tiempo2 = ticks_us() #tiempo de finalizacion

     duracion = ticks_diff(tiempo2, tiempo1)
     distancia = duracion*0.034/2
#0.034cm es la velocidad a la que viaja el sonido cada 1us
#se divide en 2 porque el sonido va y vuelve
     return distancia

#bucle para mover el servo
while True:
     d = medir_distancia()

     if d < 20:
        servo.duty_ns(1474326) #90°
     else:
        servo.duty_ns(456703) #0°
    
     sleep(2)