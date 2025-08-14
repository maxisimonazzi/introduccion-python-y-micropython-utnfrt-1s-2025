from machine import Pin, PWM
from time import sleep
import dht

sensor = dht.DHT22(Pin(19))
buzzer_alarma = PWM(Pin(5), freq=750, duty=0)
rojo_temperatura = Pin(27, Pin.OUT)  
verde_humedad = Pin(25, Pin.OUT)

def activar_alarma():
    buzzer_alarma.freq(750)
    buzzer_alarma.duty(512)  

def desactivar_alarma():
    buzzer_alarma.duty(0)

while True:
    try:
        sensor.measure()
        temperatura = sensor.temperature()
        humedad = sensor.humidity()
        
        print("Temperatura: {:.1f} °C, Humedad: {:.1f}%".format(temperatura, humedad))
        
        alerta_temperatura = temperatura < 10 or temperatura > 13
        alerta_humedad = humedad < 85 or humedad > 95

        if alerta_temperatura or alerta_humedad:
            if alerta_temperatura:
                print("⚠️ Temperatura fuera de rango")
                rojo_temperatura.value(1)
            if alerta_humedad:
                print("⚠️ Humedad fuera de rango")
                verde_humedad.value(1)

            activar_alarma()
            sleep(2)  # Alarma se activa 2 segundos
            desactivar_alarma()
            rojo_temperatura.value(0)
            verde_humedad.value(0)

        sleep(1)  # Espera 1 segundo para volver a leer los datos del sensor

    except Exception as e:
        print("Error al leer el sensor:", e)
        sleep(2)
