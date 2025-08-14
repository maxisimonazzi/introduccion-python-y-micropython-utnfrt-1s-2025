# ejemplo1.py
# Este codigo lee y muestra en consola las tramas NMEA crudas del GPS
# (por ejemplo $GPRMC, $GPGGA), sin parsearlas ni extraer campos.
# Integrantes: Rocio Pacheco, Lobo Tiago

import machine
from time import sleep

gps_serial = machine.UART(2, baudrate=9600, tx=21, rx=22)

while True:
    if gps_serial.any():
        line = gps_serial.readline()
        if line:
            try:
                line = line.decode('ascii')  # sin 'errors'
                print(line.strip())
            except UnicodeError:
                # Si la trama tiene bytes inválidos, se ignora
                pass
    sleep(0.5)