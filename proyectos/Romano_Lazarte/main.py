from machine import Pin
import dht
import time

# sensor DHT11
sensor = dht.DHT11(Pin(14))

# Relé conectado en el pin GPIO12
rele = Pin(12, Pin.OUT)
rele.value(0)  # rele apagado al inicio

# Temperatura límite en grados Celsius
Limite_temperatura = 30

while True:
    try:
        sensor.measure() # Leemos los valores del sensor
        temperatura = sensor.temperature() # Obtenemos la temperatura
        humedad = sensor.humidity() # Obtenemos la humedad
       

        print("Temperatura: {}°C  Humedad: {}%".format(temperatura, humedad))

        # Prendido y apagado del ventilador
        if temperatura >= Limite_temperatura:
            rele.value(1)  # relé prendido (activar ventilador)
            print("Temperatura alta. Ventilador encendido.")
        else:
            rele.value(0)  # relé apagado
            print("Temperatura normal. Ventilador apagado.")

    except OSError as e:
        print("Error al leer del sensor:", e)

    time.sleep(2)