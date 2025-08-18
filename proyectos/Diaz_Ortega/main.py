from machine import Pin, PWM, ADC 
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import utime
import machine                       #librerias necesarias para el programa

#Configuracion del Servo

servo = PWM(Pin(15)) #Configura el pin donde se conectara la
servo.freq(50)  #el servo motor para ser usado como PMW

#Configuracion del potenciometro                                   
pote = ADC(Pin(35))

#configuracion de los pines y caracteristicas de la pantalla LCD
i2c = machine.SoftI2C(sda=machine.Pin(21), scl=machine.Pin(22), freq=1000000) 
lcd = I2cLcd(i2c, 0x27, 2, 16)

while True:
    lcd.clear() #Limpia la pantalla LCD
    #Lee el valor analogico en el pin 34 y lo convierte en un angulo
    angulo=int(pote.read()*(180/4095))
    #convierte el angulo en un valor duty
    val=int((101/180)*angulo+51)
    #Escribe el angulo deseado en el PMW
    servo.duty(int(val))
    #Imprime el angulo en la pantalla I2C
    lcd.move_to(0,0)
    lcd.putstr("Angulo")
    lcd.move_to(0,1)
    lcd.putstr(str(angulo))

    utime.sleep_ms(70)
    