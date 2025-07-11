##########################################
#             Importaciones              #
##########################################

from datos import red, contrasena
import time
import socket
from machine import Pin, PWM, reset
import network

##########################################
#          Definicion de pines           #
##########################################

# Defino pines de los LEDs y botones
led_pins = [
    Pin(14, Pin.OUT),
    Pin(27, Pin.OUT),
    Pin(26, Pin.OUT),
    Pin(25, Pin.OUT)
    ]
boton_pins = [
    Pin(15, Pin.IN, Pin.PULL_UP),
    Pin(4, Pin.IN, Pin.PULL_UP),
    Pin(5, Pin.IN, Pin.PULL_UP),
    Pin(18, Pin.IN, Pin.PULL_UP)
    ]

##########################################
#        Definicion de funciones         #
##########################################

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    ssid = "xxx"
    password = "yyy"
    
    print('Conectando a WiFi...')
    wlan.connect(ssid, password)
    
    # Esperar conexión con timeout
    contador = 0
    while not wlan.isconnected() and contador < 10:
        print('.', end='')
        time.sleep(1)
        contador += 1
    
    if wlan.isconnected():
        print('\nConectado!')
        config = wlan.ifconfig()
        print(f'IP: {config[0]}')
        print(f'Gateway: {config[2]}')
        return wlan
    else:
        print('\nError: No se pudo conectar')
        return None

def web_page():

    icon_off = '''<svg class="svg-icon" style="width: 3em; height: 3em; vertical-align: middle; fill: currentColor; overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M512 256a170.666667 170.666667 0 0 0-170.666667 170.666667v256H256v85.333333h128v213.333333h85.333333v-213.333333h85.333334v213.333333h85.333333v-213.333333h128v-85.333333h-85.333333v-256a170.666667 170.666667 0 0 0-170.666667-170.666667M85.333333" fill="gray" /></svg>'''

    icon_led0_on = '''<svg class="svg-icon" style="width: 3em; height: 3em; vertical-align: middle; fill: currentColor; overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M469.333333 0v170.666667h85.333334V0h-85.333334m311.466667 97.706667l-130.56 128 59.733333 60.586666 130.56-128-59.733333-60.586666m-537.173333 0L183.04 158.293333l128 128 60.586667-60.586666-128-128M512 256a170.666667 170.666667 0 0 0-170.666667 170.666667v256H256v85.333333h128v213.333333h85.333333v-213.333333h85.333334v213.333333h85.333333v-213.333333h128v-85.333333h-85.333333v-256a170.666667 170.666667 0 0 0-170.666667-170.666667M85.333333 384v85.333333h170.666667V384H85.333333m682.666667 0v85.333333h170.666667V384h-170.666667z" fill="red" /></svg>'''

    icon_led1_on = '''<svg class="svg-icon" style="width: 3em; height: 3em; vertical-align: middle; fill: currentColor; overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M469.333333 0v170.666667h85.333334V0h-85.333334m311.466667 97.706667l-130.56 128 59.733333 60.586666 130.56-128-59.733333-60.586666m-537.173333 0L183.04 158.293333l128 128 60.586667-60.586666-128-128M512 256a170.666667 170.666667 0 0 0-170.666667 170.666667v256H256v85.333333h128v213.333333h85.333333v-213.333333h85.333334v213.333333h85.333333v-213.333333h128v-85.333333h-85.333333v-256a170.666667 170.666667 0 0 0-170.666667-170.666667M85.333333 384v85.333333h170.666667V384H85.333333m682.666667 0v85.333333h170.666667V384h-170.666667z" fill="yellow" /></svg>'''

    icon_led2_on = '''<svg class="svg-icon" style="width: 3em; height: 3em; vertical-align: middle; fill: currentColor; overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M469.333333 0v170.666667h85.333334V0h-85.333334m311.466667 97.706667l-130.56 128 59.733333 60.586666 130.56-128-59.733333-60.586666m-537.173333 0L183.04 158.293333l128 128 60.586667-60.586666-128-128M512 256a170.666667 170.666667 0 0 0-170.666667 170.666667v256H256v85.333333h128v213.333333h85.333333v-213.333333h85.333334v213.333333h85.333333v-213.333333h128v-85.333333h-85.333333v-256a170.666667 170.666667 0 0 0-170.666667-170.666667M85.333333 384v85.333333h170.666667V384H85.333333m682.666667 0v85.333333h170.666667V384h-170.666667z" fill="green" /></svg>'''

    icon_led3_on = '''<svg class="svg-icon" style="width: 3em; height: 3em; vertical-align: middle; fill: currentColor; overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M469.333333 0v170.666667h85.333334V0h-85.333334m311.466667 97.706667l-130.56 128 59.733333 60.586666 130.56-128-59.733333-60.586666m-537.173333 0L183.04 158.293333l128 128 60.586667-60.586666-128-128M512 256a170.666667 170.666667 0 0 0-170.666667 170.666667v256H256v85.333333h128v213.333333h85.333333v-213.333333h85.333334v213.333333h85.333333v-213.333333h128v-85.333333h-85.333333v-256a170.666667 170.666667 0 0 0-170.666667-170.666667M85.333333 384v85.333333h170.666667V384H85.333333m682.666667 0v85.333333h170.666667V384h-170.666667z" fill="blue" /></svg>'''

    icon_led0_off = icon_led1_off = icon_led2_off = icon_led3_off = icon_off


    if led_pins[0].value() == 0:
        estado_led0 = "OFF"
        icono_led0 = icon_led0_off
    else:
        estado_led0 = "ON"
        icono_led0 = icon_led0_on
    if led_pins[1].value() == 0:
        estado_led1 = "OFF"
        icono_led1 = icon_led1_off
    else:
        estado_led1 = "ON"
        icono_led1 = icon_led1_on
    if led_pins[2].value() == 0:
        estado_led2 = "OFF"
        icono_led2 = icon_led2_off
    else:
        estado_led2 = "ON"
        icono_led2 = icon_led2_on
    if led_pins[3].value() == 0:
        estado_led3 = "OFF"
        icono_led3 = icon_led3_off
    else:
        estado_led3 = "ON"
        icono_led3 = icon_led3_on
    
    html = """
        <html>

    <head>
    <title>Servidor ESP UTN</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
        html {
            font-family: Helvetica;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        h1 {
            color: #0F3376;
            padding: 2vh;
        }

        p {
            font-size: 1.5rem;
        }

        .button {
            display: inline-block;
            background-color: #45ad00;
            border: none;
            border-radius: 4px;
            color: white;
            padding: 16px 40px;
            text-decoration: none;
            font-size: 30px;
            margin: 2px;
            cursor: pointer;
            width: 250px;
        }

        .button2 {
            display: inline-block;
            background-color: #ff2626;
            border: none;
            border-radius: 4px;
            color: white;
            padding: 16px 40px;
            text-decoration: none;
            font-size: 30px;
            margin: 2px;
            cursor: pointer;
            width: 250px;
        }

        .tg {
            border:none;
            border-collapse:collapse;
            border-spacing:0;
            margin-left: auto;
            margin-right: auto;
        }

        .tg td {
            border-style:solid;
            border-width:0px;
            font-family:Arial, sans-serif;
            font-size:14px;
            overflow:hidden;
            padding:10px 5px;
            word-break:normal;
        }

        .tg th {
            border-style:solid;
            border-width:0px;
            font-family:Arial, sans-serif;
            font-size:14px;
            font-weight:normal;
            overflow:hidden;
            padding:10px 5px;
            word-break:normal;
        }

        .tg .tg-0lax {
            text-align:center;
            vertical-align:top
        }        
    </style>
    </head>
    <body>
        <h1>Servidor ESP - Curso introduccion a Micropython</h1>

        <table class="tg"><thead>
            <tr>
                <th class="tg-0lax"><p>Estado del led 3: <strong>""" + estado_led3 + """</strong></p></th>
                <th class="tg-0lax"><p>Estado del led 2: <strong>""" + estado_led2 + """</strong></p></th>
                <th class="tg-0lax"><p>Estado del led 1: <strong>""" + estado_led1 + """</strong></p></th>
                <th class="tg-0lax"><p>Estado del led 0: <strong>""" + estado_led0 + """</strong></p></th>
            </tr></thead>
            <tbody>
            <tr>
                <td class="tg-0lax"><h1><strong>""" + icono_led3 + """</strong></h1></td>
                <td class="tg-0lax"><h1><strong>""" + icono_led2 + """</strong></h1></td>
                <td class="tg-0lax"><h1><strong>""" + icono_led1 + """</strong></h1></td>
                <td class="tg-0lax"><h1><strong>""" + icono_led0 + """</strong></h1></td>
            </tr>
            <tr>
                <td class="tg-0lax"><p><a href="/?led3=on"><button class="button">ON</button></a></p></td>
                <td class="tg-0lax"><p><a href="/?led2=on"><button class="button">ON</button></a></p></td>
                <td class="tg-0lax"><p><a href="/?led1=on"><button class="button">ON</button></a></p></td>
                <td class="tg-0lax"><p><a href="/?led0=on"><button class="button">ON</button></a></p></td>
            </tr>
            <tr>
                <td class="tg-0lax"><p><a href="/?led3=off"><button class="button button2">OFF</button></a></p></td>
                <td class="tg-0lax"><p><a href="/?led2=off"><button class="button button2">OFF</button></a></p></td>
                <td class="tg-0lax"><p><a href="/?led1=off"><button class="button button2">OFF</button></a></p></td>
                <td class="tg-0lax"><p><a href="/?led0=off"><button class="button button2">OFF</button></a></p></td>
            </tr>
            </tbody>
        </table>
    </body>

    </html>
  """
    return html

# Crear servidor web para controlar LEDs
def servidor_web(wlan):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    
    print(f'Servidor activo en: http://{wlan.ifconfig()[0]}')
    print('Presiona Ctrl+C para detener')
    
    while True:
        try:
            conn, addr = s.accept()
            print('Se conecto un usuario desde la IP %s' % str(addr))
            request = conn.recv(1024)
            request = str(request)

            # Procesar comandos de LEDs
            if request.find('/?led0=on') == 6:
                led_pins[0].value(1)
                print('LED 0 ON')
            if request.find('/?led0=off') == 6:
                led_pins[0].value(0)
                print('LED 0 OFF')
            if request.find('/?led1=on') == 6:
                led_pins[1].value(1)
                print('LED 1 ON')
            if request.find('/?led1=off') == 6:
                led_pins[1].value(0)
                print('LED 1 OFF')
            if request.find('/?led2=on') == 6:
                led_pins[2].value(1)
                print('LED 2 ON')
            if request.find('/?led2=off') == 6:
                led_pins[2].value(0)
                print('LED 2 OFF')
            if request.find('/?led3=on') == 6:
                led_pins[3].value(1)
                print('LED 3 ON')
            if request.find('/?led3=off') == 6:
                led_pins[3].value(0)
                print('LED 3 OFF')

            respuesta = "HTTP/1.1 200 OK\r\n"
            respuesta += "Content-Type: text/html; charset=UTF-8\r\n"
            respuesta += "Content-Length: {}\r\n".format(len(web_page()))
            respuesta += "Connection: close\r\n"
            respuesta += "\r\n"
            respuesta += web_page()
            conn.sendall(respuesta)
            time.sleep(0.5)
            conn.close()
            
        except KeyboardInterrupt:
            print('\nDeteniendo servidor...')
            break
        except OSError as e:
            print('OSError:', e)
            if 'conn' in locals():
                conn.close()
        except Exception as e:
            print('Error:', e)
            if 'conn' in locals():
                conn.close()
    
    s.close()

# Programa principal
def main():
    wlan = conectar_wifi()
    if wlan:
        servidor_web(wlan)
    else:
        print('No se pudo iniciar el servidor')

if __name__ == '__main__':
    main()