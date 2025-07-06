import network
import time

ssid = 'nombre-de-red'
password = 'xxxx'

estacion = network.WLAN(network.STA_IF)
estacion.active(True)

estacion.connect(ssid, password)

print('Conectando ...', end="")

while not estacion.isconnected():
    print('.', end="")
    time.sleep(0.1)

config = estacion.ifconfig()

print()
print('Conectado')
print("-"*40)
print('Configuración de red:')
print(f"IP: {config[0]}")
print(f"Mascara de red: {config[1]}")
print(f"Gateway: {config[2]}")
print(f"DNS: {config[3]}")

estacion.active(False)