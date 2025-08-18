from machine import Pin, ADC
import time

pin_ntc = 34
pin_led_verde = 2
pin_led_rojo = 15

sensor_ntc = ADC(Pin(pin_ntc))
sensor_ntc.atten(ADC.ATTN_11DB)
led_verde = Pin(pin_led_verde, Pin.OUT)
led_rojo = Pin(pin_led_rojo, Pin.OUT)

umbral_adc = 2600

while True:
    lectura_adc = sensor_ntc.read()
    print("Lectura ADC:", lectura_adc, "| Umbral:", umbral_adc)
    
    if lectura_adc > umbral_adc:
        print("Temperatura baja. LED verde ON")
        led_verde.value(1)
        led_rojo.value(0)
    else:
        print("Temperatura alta. LED rojo ON")
        led_verde.value(0)
        led_rojo.value(1)
    
    time.sleep(2)