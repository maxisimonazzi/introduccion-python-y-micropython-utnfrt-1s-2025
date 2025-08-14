import machine
from time import sleep

# ==== CONFIGURACIÓN UART ====
gps_serial = machine.UART(1, baudrate=9600, tx=34, rx=12, timeout=1000)

# ==== FUNCIÓN PARA CONVERTIR NMEA A DECIMAL ====
def nmea_to_decimal(coord, direction):
    if not coord or coord == "0" or coord == "":
        return None
    try:
        deg_len = 2 if direction in ['N', 'S'] else 3
        deg = int(coord[:deg_len])
        minutes = float(coord[deg_len:])
        decimal = deg + minutes / 60
        if direction in ['S', 'W']:
            decimal *= -1
        return decimal
    except ValueError:
        return None

# ==== LOOP PRINCIPAL ====
while True:
    if gps_serial.any():
        line = gps_serial.readline()
        if line:
            try:
                line = line.decode('ascii')
                if line.startswith('$GNGGA'):
                    parts = line.split(',')
                    
                    # Verificar que haya al menos 10 campos para evitar IndexError
                    if len(parts) >= 10:
                        lat = nmea_to_decimal(parts[2], parts[3])
                        lon = nmea_to_decimal(parts[4], parts[5])
                        sats = parts[7] if len(parts) > 7 else "0"
                        alt = parts[9] if len(parts) > 9 else "0"

                        if lat is not None and lon is not None:
                            print("Lat:", lat, "Lon:", lon, "Satélites:", sats, "Altitud:", alt, "m")
                        else:
                            print("Esperando fix GPS...")
                    else:
                        print("Trama GNGGA incompleta")
            except UnicodeError:
                pass
    sleep(0.5)
