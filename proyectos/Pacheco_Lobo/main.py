# main.py
# Proyecto: Lectura GPS Neo-7 en ESP32 con MicroPython
# Integrantes: Rocio Pacheco, Lobo Tiago

from machine import UART
import time

# Configurar UART1 (puertos pueden variar según tu ESP32)
gps = UART(1, baudrate=9600, tx=17, rx=16)  # Cambiar pines según conexión

def parse_nmea(sentence):

    if sentence.startswith('$GPGGA'):
        parts = sentence.split(',')
        hora = parts[1]
        lat = parts[2]
        lat_dir = parts[3]
        lon = parts[4]
        lon_dir = parts[5]
        sats = parts[7]
        alt = parts[9]

        return {
            'hora': hora,
            'latitud': f"{lat} {lat_dir}",
            'longitud': f"{lon} {lon_dir}",
            'satélites': sats,
            'altitud_m': alt
        }
    return None

print("Esperando datos del GPS...")
time.sleep(2)

while True:
    if gps.any():
        line = gps.readline()
        try:
            sentence = line.decode('utf-8').strip()
            data = parse_nmea(sentence)
            if data:
                print(f"Hora UTC: {data['hora']}")
                print(f"Latitud: {data['latitud']}")
                print(f"Longitud: {data['longitud']}")
                print(f"Satélites: {data['satélites']}")
                print(f"Altitud: {data['altitud_m']} m")
                print("----------------------------")
        except Exception as e:
            print("Error al leer trama:", e)
    time.sleep(1)
