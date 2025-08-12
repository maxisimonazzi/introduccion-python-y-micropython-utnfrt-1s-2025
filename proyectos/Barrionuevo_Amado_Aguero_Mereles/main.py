from machine import Pin, ADC, SoftI2C
import network
import time
import urequests
import dht
from i2c_lcd import I2cLcd

adc_suelo = ADC(Pin(34))
adc_suelo.atten(ADC.ATTN_11DB) 
adc_suelo.width(ADC.WIDTH_12BIT)  

sensor_dht = dht.DHT22(Pin(15))

wifi_nombre = "Wokwi-GUEST"
wifi_clave = ""

api_key = "thingspeak_api_key"
url_envio = "https://api.thingspeak.com/update"

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
pantalla = I2cLcd(i2c, 0x27, 2, 16)
pantalla.clear()

red = network.WLAN(network.STA_IF)
red.active(True)
red.connect(wifi_nombre, wifi_clave)
print("Conectando a WiFi", end="")
while not red.isconnected():
    print(".", end="")
    time.sleep(0.5)
print("\nWiFi conectado:", red.ifconfig())

rele_bomba = Pin(5, Pin.OUT)
rele_foco = Pin(13, Pin.OUT)
rele_ventilador = Pin(4, Pin.OUT)

def rele_encender(pin):
    pin.value(0)

def rele_apagar(pin):
    pin.value(1)

rele_apagar(rele_bomba)
rele_apagar(rele_foco)
rele_apagar(rele_ventilador)

def enviar_datos(t, h, s):
    try:
        datos = f"{url_envio}?api_key={api_key}&field1={t}&field2={h}&field3={s}"
        r = urequests.get(datos)
        r.close()
        print("Enviado a ThingSpeak")
    except Exception as e:
        print("Error enviando a ThingSpeak:", e)

contador = 0
intervalo_envio = 15  

while True:
    try:
        sensor_dht.measure()
        t = sensor_dht.temperature()
        h = sensor_dht.humidity()
    except Exception as e:
        print("Error leyendo DHT22:", e)
        t = 0
        h = 0

    valor_adc = adc_suelo.read()
    s = int((valor_adc / 4095) * 100)

    if s < 40:
        rele_apagar(rele_bomba)     
    else:
        rele_encender(rele_bomba)  

    if t > 30:
        rele_apagar(rele_foco)
        rele_encender(rele_ventilador)
    else:
        rele_encender(rele_foco)
        rele_apagar(rele_ventilador)

    pantalla.clear()
    pantalla.putstr(f"T:{t}C H:{h}%\nSuelo:{s}%")

    if contador % intervalo_envio == 0:
        enviar_datos(t, h, s)

    contador += 1
    time.sleep(1) 
