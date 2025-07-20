from machine import Pin, SPI
import network
import socket
import st7789
import vga1_8x8 as font
import time

# Pines sensores
sensor_puerta = Pin(27, Pin.IN, Pin.PULL_UP)
sensor_pir = Pin(26, Pin.IN, Pin.PULL_UP)
sensor_rotura = Pin(25, Pin.IN, Pin.PULL_UP)

# Relé sirena
rele_sirena = Pin(2, Pin.OUT)
rele_sirena.value(1)

# Pantalla
spi = SPI(1, baudrate=40000000, sck=Pin(18), mosi=Pin(19))
tft = st7789.ST7789(spi, 135, 240,
                    reset=Pin(23, Pin.OUT),
                    cs=Pin(5, Pin.OUT),
                    dc=Pin(16, Pin.OUT),
                    backlight=Pin(4, Pin.OUT),
                    rotation=1)
tft.init()

# Wi-Fi
ssid = "Luzmi"
password = "40696991"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    time.sleep(1)
print("Conectado! IP:", wlan.ifconfig()[0])

alarma_activada = False

# Estados previos para detectar cambios
prev_estado = {
    "alarma": None,
    "puerta": None,
    "pir": None,
    "rotura": None
}

def draw_text(label, value, y, color=st7789.WHITE):
    tft.fill_rect(10, y, 220, 20, st7789.BLACK)  # borrar solo la línea
    tft.text(font, f"{label}: {value}", 10, y, color)

def actualizar_pantalla():
    # alarma activada/desactivada
    if prev_estado["alarma"] != alarma_activada:
        texto = "Alarma ACTIVADA" if alarma_activada else "Alarma DESACTIVADA"
        color = st7789.GREEN if alarma_activada else st7789.RED
        draw_text("Estado", texto, 10, color)
        prev_estado["alarma"] = alarma_activada

    # zona1 puerta
    estado_puerta = sensor_puerta.value()
    if prev_estado["puerta"] != estado_puerta:
        txt = "Abierta" if estado_puerta else "Cerrada"
        draw_text("Zona1 Puerta", txt, 40)
        prev_estado["puerta"] = estado_puerta

    # zona2 pir
    estado_pir = sensor_pir.value()
    if prev_estado["pir"] != estado_pir:
        txt = "Detectado" if estado_pir else "No"
        draw_text("Zona2 PIR", txt, 60)
        prev_estado["pir"] = estado_pir

    # zona3 rotura
    estado_rotura = sensor_rotura.value()
    if prev_estado["rotura"] != estado_rotura:
        txt = "Detectada" if estado_rotura else "No"
        draw_text("Zona3 Rotura", txt, 80)
        prev_estado["rotura"] = estado_rotura

def generar_web():
    html = f"""
    <html>
    <head>
        <title>Alarma</title>
        <meta http-equiv="refresh" content="2">
    </head>
    <body>
    <h1>Alarma {"ACTIVADA" if alarma_activada else "DESACTIVADA"}</h1>
    <p>Zona1 Puerta: {"Abierta" if sensor_puerta.value() else "Cerrada"}</p>
    <p>Zona2 PIR: {"Detectado" if sensor_pir.value() else "No"}</p>
    <p>Zona3 Rotura: {"Detectada" if sensor_rotura.value() else "No"}</p>
    <a href="/activar"><button>Activar</button></a>
    <a href="/desactivar"><button>Desactivar</button></a>
    </body></html>"""
    return html

# Web server no bloqueante
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
s.setblocking(False)
print('Servidor web listo')

last_screen_update = 0

while True:
    # Lógica alarma
    if alarma_activada:
        if sensor_puerta.value()==1 or sensor_pir.value()==1 or sensor_rotura.value()==1:
            rele_sirena.value(0)
        else:
            rele_sirena.value(1)
    else:
        rele_sirena.value(1)

    # actualizar pantalla cada 0,2 seg
    now = time.ticks_ms()
    if time.ticks_diff(now, last_screen_update) > 200:
        actualizar_pantalla()
        last_screen_update = now

    # atender web rápido
    try:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        if '/activar' in request:
            alarma_activada = True
        if '/desactivar' in request:
            alarma_activada = False
        response = generar_web()
        conn.send('HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n')
        conn.sendall(response)
        conn.close()
    except:
        pass

    time.sleep(0.05)
