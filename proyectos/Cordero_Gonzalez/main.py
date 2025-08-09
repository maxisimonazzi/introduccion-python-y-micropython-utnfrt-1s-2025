#=====Librerias=====
from machine import Pin
from time import sleep
import dht
import network
import BlynkLib

#=====Definir pines=====
#Sensor DHT11
sensor_dht11 = dht.DHT11(Pin(14))
#LEDs temperatura
ledV_t = Pin(25, Pin.OUT)
ledA_t = Pin(33, Pin.OUT)
ledR_t = Pin(32, Pin.OUT)
#LEDs humedad
ledV_h = Pin(4, Pin.OUT)
ledA_h = Pin(16, Pin.OUT)
ledR_h = Pin(17, Pin.OUT)
#Buzzer alerta temperatura
buzzer_t = Pin(19, Pin.OUT)
#Buzzer alerta humedad
buzzer_h = Pin(21, Pin.OUT)

#=====Inicializar variables=====
n = 1
registro_temp = 0.0
registro_hum = 0.0
cant_evaluada = 12
#Se definen valores iniciales estandar para que las condiciones no frenen el funcionamiento del programa mientras no se obtenga primer valor promedio
prom_temp = 25.0
prom_hum = 50.0

#=====Datos red WiFi=====
wifiName = "Contardo" #SSID
wifiPass = "Berlin#898" #PASSWORD

#=====Funcion para conectar ESP32 a WiFi=====
def do_connect(SSID, PASSWORD):
    redWifi = network.WLAN(network.STA_IF)
    redWifi.active(True)
    if not redWifi.isconnected():
        redWifi.connect(SSID, PASSWORD)
        print("Conectando a red WiFi...")
        while not redWifi.isconnected():
            pass
    print(f"Conectado a: {SSID}")


#***=====Inicio del programa=====***
do_connect(wifiName, wifiPass)

#Codigo de autentificacion otorgado por Blynk para el envio de datos a dashboard
BLYNK_AUTH = 's9CBTDsr2PzEy0-H_rjOgZ_8e4CshjjK'
blynk = BlynkLib.Blynk(BLYNK_AUTH)
#Inicializar Blynk
blynk.run()

while True:
    
    #Obtener datos de temperatura y humedad desde el sensor
    sensor_dht11.measure()
    temperatura = sensor_dht11.temperature()
    #temperatura = temperatura-50 #Forzar error
    #temperatura = temperatura+30 #Forzar error
    humedad = sensor_dht11.humidity()
    #humedad = humedad-80 #Forzar error
    #humedad = humedad-50 #Forzar error
    
    #Enviar dato temperatura a Blynk
    blynk.virtual_write(1, temperatura)
    #Enviar dato humedad a Blynk
    blynk.virtual_write(0, humedad)
    
    #Se genera un almacenamiento de los datos obtenidos para generar un promedio posteriormente
    registro_temp = registro_temp + temperatura
    registro_hum = registro_hum + humedad
    
    #Visualizacion en consola de datos obtenidos y la iteracion actual
    print(f"\nIteracion: {n}")
    print(f"Temperatura: {temperatura}°C")
    print(f"Humedad: {humedad}%")
    
    #Condiciones para encendido de LEDs de monitoreo de temperatura
    if(temperatura<=2):
        ledV_t.off()
        ledA_t.off()
        ledR_t.on()
        sleep(0.5)
        ledR_t.off()
    if(temperatura>2 and temperatura<=25):
        ledV_t.on()
        ledA_t.off()
        ledR_t.off()
    elif(temperatura>25 and temperatura<=35):
        ledV_t.off()
        ledA_t.on()
        ledR_t.off()
    elif(temperatura>35):
        ledV_t.off()
        ledA_t.off()
        ledR_t.on()
    
    #Condiciones para encendido de LEDs de monitoreo de humedad
    if(humedad>=50):
        ledV_h.on()
        ledA_h.off()
        ledR_h.off()
    elif(humedad>=10 and humedad<50):
        ledV_h.off()
        ledA_h.on()
        ledR_h.off()
    elif(humedad<10):
        ledV_h.off()
        ledA_h.off()
        ledR_h.on()
    
    #Generar un valor promedio de temperatura y humedad en un tiempo definido, en este caso 1 minuto (12 iteraciones)
    if (n==cant_evaluada):
        prom_temp = registro_temp/float(cant_evaluada) #Promedio temperatura
        prom_hum = registro_hum/float(cant_evaluada) #Promedio humedad
        print(f"Promedio temperatura: {prom_temp:.2f}°C")
        blynk.virtual_write(2, prom_temp) #Envio de valor a Blynk
        print(f"Promedio humedad: {prom_hum:.2f}%")
        blynk.virtual_write(3, prom_hum) #Envio de valor a Blynk
        #Se reinician las variables para mantener el funcionamiento de la condicion
        n = 1
        registro_temp = 0
        registro_hum = 0
    else:
        n = n + 1
        
    #Condiciones notificaciones Blynk y alerta con buzzer
    if(prom_temp>=35):
        blynk.log_event("temperatura_alta")
    if(prom_temp<=2):
        blynk.log_event("riesgo_helada")
        buzzer_t.on()
        sleep(1)
        buzzer_t.off()
    if(prom_temp<=0):
        blynk.log_event("helada_inminente")
        
    if(prom_hum<=10):
        blynk.log_event("humedad_baja")
        buzzer_h.on()
        sleep(1)
        buzzer_h.off
               
    sleep(5)