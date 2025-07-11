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
   
        respuesta = "Hola curso desde el ESP32!"
        
        # Enviar respuesta
        cliente.send(respuesta)
        
    except Exception as e:
        print('Error:', e)
    finally:
        cliente.close()