INTRODUCCIÓN 
Este proyecto permite controlar cuatro LED conectados a un ESP32 a través de un celular. Se conecta a una red WiFi, levanta un servidor HTTP y muestra una página web desde la que se pueden encender o apagar los LED
Cada LED tiene su propio botón ON/OFF en la web.
COMPONENTES
•	ESP32 
•	4 LEDS
•	4 Resistencias
•	Sensor ultrasónico 
•	Servo motor 
•	Cables y protoboard
•	Fuente de alimentación 
 DESCRIPCIÓN
•	Conexión WiFi: función conectar_wifi() activa el WiFi en modo estación y conecta con timeout, imprimiendo IP y gateway si conecta correctamente.
•	Servidor web:  servidor_web(wlan) crea socket TCP escuchando en puerto 80, recibe peticiones, identifica comandos para encender/apagar LEDs, cambia estado de pines .
•	Página web: función web_page() genera HTML dinámico .
•	Control servo + sensor: ejemplo básico en un loop que mide distancia con HC-SR04 
COMO USAR
1.	Flashea MicroPython en tu ESP32.
2.	Conecta los LEDs a GPIO14, 27, 26 y 25 con resistencias adecuadas.
3.	Conecta sensor ultrasónico y servo según pines indicados.
4.	Copia el script principal en main.py al ESP32.
5.	Ajusta SSID y contraseña WiFi en la función conectar_wifi().
6.	Ejecuta el código y espera a que conecte a la red WiFi.
7.	Abre el navegador y escribe la IP que muestra en consola para acceder a la web y controlar los LEDs.
CONCLUSIÓN 
Este proyecto sirve para entender cómo controlar dispositivos como LEDs y servo mediante un servidor web en un microcontrolador con MicroPython. Incorpora conceptos de red, sockets, HTML dinámico, y uso de sensores y PWM.
