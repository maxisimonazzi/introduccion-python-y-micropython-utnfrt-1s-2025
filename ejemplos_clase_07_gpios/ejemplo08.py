from machine import PWM, Pin
import utime
from dht import DHT22

servo =PWM(Pin(19))
servo.freq(50)
sensor = DHT22(Pin(13))

while True:
    # Para los valores del servo de este simulador
    # 456703 ns -> 0 grados
    # 1474326 ns -> 90 grados
    # 2491950 ns -> 180 grados

    sensor.measure() # Leemos los valores del sensor
    temperatura = sensor.temperature() # Obtenemos la temperatura
    humedad = sensor.humidity() # Obtenemos la humedad

    if temperatura < 40:
        servo.duty_ns(456703)   # 0 grados (0 a 40)
    if temperatura >= 40 and temperatura < 60:
        servo.duty_ns(1474326)  # 90 grados (40 a 60)
    if temperatura >= 60:
        servo.duty_ns(2491950)  # 180 grados (60 o superior)

    utime.sleep_ms(50)