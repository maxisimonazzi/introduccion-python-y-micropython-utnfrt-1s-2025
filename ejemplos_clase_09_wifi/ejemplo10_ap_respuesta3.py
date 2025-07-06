import network
import socket

ap = network.WLAN(network.AP_IF)
ap.active(True)

nombre = 'Mi_ESP32_AP'
contrasena = '1234567890'

ap.config(essid=nombre, password=contrasena, authmode=network.AUTH_WPA_WPA2_PSK)

ip = '10.0.0.15'
mascara_subred = '255.255.255.0'
puerta_enlace = '10.0.0.15'
dns = '10.0.0.15'

ap.ifconfig((ip, mascara_subred, puerta_enlace, dns))

print('Punto de acceso configurado:')
print("-"*40)
print('SSID:', nombre)
print('IP:', ap.ifconfig()[0])
print('Máscara de red:', ap.ifconfig()[1])
print('Puerta de enlace:', ap.ifconfig()[2])
print('DNS:', ap.ifconfig()[3])
print("-"*40)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)

print()
print('Servidor web en ejecución...')
print("-"*40)

while True:
    cliente, addr = s.accept()
    print('Cliente conectado desde', addr)
    
    try:
        # Leer la petición del cliente
        request = cliente.recv(1024).decode('utf-8')
        print('Petición recibida:')
        print(request)
        
        # Crear respuesta HTTP válida
        html = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 AP</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>¡Hola mundo desde ESP32!</h1>
    <p>Servidor web funcionando correctamente en modo Access Point</p>
    <p>IP del servidor: 10.0.0.15</p>
</body>
</html>"""
        
        # Headers HTTP válidos
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html; charset=UTF-8\r\n"
        response += "Content-Length: {}\r\n".format(len(html))
        response += "Connection: close\r\n"
        response += "\r\n"
        response += html
        
        # Enviar respuesta
        cliente.send(response.encode('utf-8'))
        
    except Exception as e:
        print('Error:', e)
    finally:
        cliente.close()
