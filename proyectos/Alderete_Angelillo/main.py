
from machine import Pin, time_pulse_us
import utime
import network
import socket

# -------- CONFIGURACIÓN WIFI ---------
ssid = 'SSID'
password = 'PASS'

# -------- VARIABLES GLOBALES --------
Largo_tanque = 11
estado_de_la_bomba = False
modo_manual = 0
bomba_encendida = 0

# -------- PINES --------
trig = Pin(5, Pin.OUT)
echo = Pin(4, Pin.IN)
# Usar GPIO14 (D5) y arrancar en LOW (apagado)
rele_bomba = Pin(14, Pin.OUT, value=0)

# -------- FUNCIONES --------
def medir_distancia():
    trig.value(0)
    utime.sleep_us(2)
    trig.value(1)
    utime.sleep_us(10)
    trig.value(0)
    try:
        duracion = time_pulse_us(echo, 1, 30000)
        if duracion < 0:
            return None
        distancia_cm = (duracion / 2) / 29.155
        return distancia_cm
    except Exception:
        return None

def medir_distancia_filtrada(n=5):
    mediciones = []
    for _ in range(n):
        d = medir_distancia()
        if d is not None and d > 0:
            mediciones.append(d)
        utime.sleep_ms(50)

    if len(mediciones) >= 3:
        mediciones.sort()
        return sum(mediciones[1:-1]) / len(mediciones[1:-1])
    elif mediciones:
        return sum(mediciones) / len(mediciones)
    else:
        return 0

def controlar_automatico(nivel):
    global estado_de_la_bomba
    if nivel < 30:
        estado_de_la_bomba = True
    elif nivel >= 85:
        estado_de_la_bomba = False

def controlar_manual(on_off):
    global estado_de_la_bomba
    estado_de_la_bomba = bool(on_off)

def eleccion_de_modo(nivel):
    if modo_manual:
        controlar_manual(bomba_encendida)
    else:
        controlar_automatico(nivel)

def conectar_wifi(ssid, password):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, password)
    print("Conectando a WiFi...")
    t0 = utime.time()
    while not sta.isconnected():
        if utime.time() - t0 > 15:
            print("Tiempo de espera agotado.")
            return None
        utime.sleep(0.02)
    print("Conectado a:", ssid)
    print("IP:", sta.ifconfig()[0])
    return sta

def generar_pagina(nivel_agua):
    modo_texto = "Manual" if modo_manual else "Automático"
    bomba_texto = "Encendida" if estado_de_la_bomba else "Apagada"
    bomba_color = "#4CAF50" if estado_de_la_bomba else "#f44336"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Control de Bomba - ESP8266</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="5">
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom right, #e0f7fa, #ffffff);
            color: #333;
            text-align: center;
            padding: 20px;
        }}
        h1 {{
            color: #00796B;
        }}
        .status {{
            font-size: 18px;
            margin: 10px 0;
        }}
        .nivel {{
            font-size: 24px;
            font-weight: bold;
            color: #0277BD;
            margin-bottom: 10px;
        }}
        .bomba {{
            color: white;
            background-color: {bomba_color};
            padding: 10px;
            border-radius: 8px;
            display: inline-block;
            margin: 10px 0;
        }}
        .barra-container {{
            width: 80%;
            height: 30px;
            background-color: #ddd;
            border-radius: 20px;
            overflow: hidden;
            margin: 0 auto 20px auto;
            box-shadow: inset 0 0 5px #aaa;
        }}
        .barra-nivel {{
            height: 100%;
            width: {nivel_agua}%;
            background: linear-gradient(to right, red, orange, yellow, green);
            transition: width 0.5s ease;
        }}
        button {{
            padding: 12px 24px;
            font-size: 16px;
            margin: 8px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        .on {{
            background-color: #4CAF50;
            color: white;
        }}
        .off {{
            background-color: #f44336;
            color: white;
        }}
    </style>
</head>
<body>
    <h1>Panel de Control del Tanque</h1>
    <div class="status"><strong>Modo actual:</strong> {modo_texto}</div>
    <div class="bomba"><strong>Bomba:</strong> {bomba_texto}</div>
    <div class="nivel">Nivel del tanque: {nivel_agua}%</div>
    <div class="barra-container">
        <div class="barra-nivel"></div>
    </div>
    <form>
        <button name="modo" value="manual" class="on">Modo Manual</button>
        <button name="modo" value="auto" class="on">Modo Automático</button><br>
        <button name="bomba" value="on" class="on">Encender Bomba</button>
        <button name="bomba" value="off" class="off">Apagar Bomba</button>
    </form>
</body>
</html>"""
    return html

# -------- INICIAR WIFI Y SERVIDOR --------
wlan = conectar_wifi(ssid, password)
if not wlan:
    raise RuntimeError("No se pudo conectar al WiFi")

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print("Servidor web en: http://" + wlan.ifconfig()[0])

# -------- LOOP PRINCIPAL --------
while True:
    distancia_sensor = medir_distancia_filtrada()
    dist_min = 3
    dist_max = 11
    nivel_agua = round(((dist_max - distancia_sensor) / (dist_max - dist_min)) * 100)
    if nivel_agua > 100:
        nivel_agua = 100
    elif nivel_agua < 0:
        nivel_agua = 0

    print(f"Nivel de agua: {nivel_agua}%")
    eleccion_de_modo(nivel_agua)

    # Relé activo en HIGH
    rele_bomba.value(1 if estado_de_la_bomba else 0)

    try:
        s.settimeout(3)
        cliente, addr = s.accept()
        request = cliente.recv(1024).decode()

        if "/api" in request:
            if "bomba=on" in request:
                bomba_encendida = 1
            elif "bomba=off" in request:
                bomba_encendida = 0
            if "modo=manual" in request:
                modo_manual = 1
            elif "modo=auto" in request:
                modo_manual = 0
            response = '{{"nivel": {nivel}, "bomba": "{bomba}", "modo": "{modo}"}}'.format(
                nivel=nivel_agua,
                bomba="Encendida" if estado_de_la_bomba else "Apagada",
                modo="Manual" if modo_manual else "Automático"
            )
            cliente.sendall("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + response)
        else:
            if "modo=manual" in request:
                modo_manual = 1
            elif "modo=auto" in request:
                modo_manual = 0
            if "bomba=on" in request:
                bomba_encendida = 1
            elif "bomba=off" in request:
                bomba_encendida = 0

            respuesta = generar_pagina(nivel_agua)
            cliente.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + respuesta)

        cliente.close()
    except Exception:
        pass

    utime.sleep(0.02)
