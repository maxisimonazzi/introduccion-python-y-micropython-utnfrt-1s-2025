# 🛰️ Sistema de Rastreo GPS Neo-7 basado en ESP32 y MicroPython

## 📌 Descripción General
Este proyecto implementa un sistema de rastreo GPS utilizando un módulo **Neo-7** y una **ESP32** programada en **MicroPython**.  
El sistema recibe las tramas **NMEA** desde el GPS, las procesa y muestra en consola la información de ubicación, fecha, hora y otros datos relevantes.

---

## 🛠 Componentes Utilizados
- **ESP32** (Placa de desarrollo con soporte MicroPython)
- **Módulo GPS Neo-7**

---

## 🔌 Diagrama de Conexión
```
## ESP32    GPS Neo-7

3V3   --->  VCC
GND   --->  GND
TX(16) ---> RX
RX(17) ---> TX

```
![Esquema de conexión ESP32 ↔ GPS Neo-7](https://i.postimg.cc/yx5PRGKw/Circuito-GPS-ESP32.png)

![Montaje ESP32 y GPS Neo-7](https://i.postimg.cc/PrpKHdzh/Montaje-ESP32-GPS.jpg)

---

## 📡 Funcionamiento
El sistema:
1. Inicializa la comunicación UART con el módulo GPS.
2. Lee continuamente las tramas **NMEA**.
3. Filtra la trama `$GNGGA` para obtener latitud, longitud y otros datos de posición.
4. Convierte las coordenadas de formato NMEA a formato decimal.
5. Muestra en consola la información procesada.

### Video del funcionamiento

<div align="center">

  [![Video de funcionamiento](https://img.youtube.com/vi/gx2VcwsKnis/hqdefault.jpg)](https://youtu.be/gx2VcwsKnis)

</div>

---

## 📜 Información sobre la Trama NMEA
El módulo GPS envía datos en formato **NMEA** (National Marine Electronics Association), que son cadenas de texto ASCII con información de posición y estado.  
Ejemplo de trama:

```

\$GNGGA,210628.000,2715.29137,S,06532.24465,W,1,08,0.9,545.4,M,46.9,M,,\*47

````

Estructura simplificada de la trama `$GNGGA`:
1. **$GNGGA** → Tipo de trama (Global Positioning System Fix Data)
2. **210628.000** → Hora UTC (HHMMSS.SSS)
3. **2715.29137,S** → Latitud y hemisferio
4. **06532.24465,W** → Longitud y hemisferio
5. **1** → Calidad de la señal GPS (0=no fix, 1=fijación GPS, 2=DGPs)
6. **08** → Número de satélites utilizados
7. **0.9** → Precisión horizontal (HDOP)
8. **545.4,M** → Altitud sobre el nivel del mar (en metros)
9. **46.9,M** → Separación geoidal
10. **,,*47** → Datos no utilizados y checksum

---

## 💻 Código para lectura de tramas NMEA
```python
import machine
from time import sleep

# Inicialización UART (puertos según conexión)
gps_serial = machine.UART(2, baudrate=9600, tx=21, rx=22)

while True:
    if gps_serial.any():
        try:
            line = gps_serial.readline()
            if line:
                try:
                    decoded_line = line.decode('utf-8')
                except UnicodeError:
                    decoded_line = line.decode('utf-8', 'ignore')

                print(decoded_line.strip())  # Mostrar trama completa
        except Exception as e:
            print("Error leyendo GPS:", e)
    sleep(0.5)
````
---

## 💻 Código para procesar y mostrar datos separados

```python
import machine
from time import sleep

def nmea_to_decimal(coord, direction):
    # Conversión de coordenadas NMEA a decimal
    if not coord or not direction:
        return None
    degrees = float(coord[:2])
    minutes = float(coord[2:])
    decimal = degrees + (minutes / 60)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

gps_serial = machine.UART(2, baudrate=9600, tx=21, rx=22)

while True:
    if gps_serial.any():
        try:
            line = gps_serial.readline()
            if line:
                try:
                    decoded_line = line.decode('utf-8')
                except UnicodeError:
                    decoded_line = line.decode('utf-8', 'ignore')

                if decoded_line.startswith('$GNGGA'):
                    parts = decoded_line.strip().split(',')
                    if len(parts) >= 10:
                        hora_utc = parts[1]
                        lat = nmea_to_decimal(parts[2], parts[3])
                        lon = nmea_to_decimal(parts[4], parts[5])
                        calidad = parts[6]
                        satelites = parts[7]
                        altitud = parts[9]

                        print(f"Hora UTC: {hora_utc}")
                        print(f"Latitud: {lat}")
                        print(f"Longitud: {lon}")
                        print(f"Calidad señal: {calidad}")
                        print(f"Satélites: {satelites}")
                        print(f"Altitud: {altitud} m")
                        print("-" * 30)
        except Exception as e:
            print("Error procesando GPS:", e)
    sleep(1)
```

---

## ▶️ Cómo Usar

1. Instalar **MicroPython** en la ESP32.
2. Usar **Thonny** o **rshell** para subir el código.
3. Conectar el GPS Neo-7 según el diagrama.
4. Ejecutar el código para leer y procesar las tramas NMEA.
5. Observar en la consola la ubicación y demás datos.

![Ensayo ESP32 con GPS Neo-7](https://i.postimg.cc/KcsQC1TJ/Ensayo-ESP32-GPS.jpg)

---

## 📌 Conclusión

Este proyecto demuestra cómo integrar un módulo GPS Neo-7 con una ESP32 usando MicroPython para recibir, procesar y mostrar datos de ubicación en tiempo real.
La lectura y decodificación de tramas NMEA permite obtener información precisa que puede integrarse en sistemas de rastreo, monitoreo de vehículos o proyectos IoT.

---

## 👥 Integrantes

- Pacheco, Rocío Ahaní
- Lobo, Ángel Tiago Lobo

---
