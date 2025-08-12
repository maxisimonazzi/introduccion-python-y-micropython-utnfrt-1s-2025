from machine import Pin, ADC
import time

# Define el pin analógico donde está conectado el sensor
sensor_pin = 34  # Por ejemplo, en un ESP32, GPIO34 es un pin analógico

# Inicializa el ADC
adc = ADC(Pin(sensor_pin))
adc.atten(ADC.ATTN_11DB)  # Configura la atenuación para un rango completo

# Se definen los valores de referencia (se recomienda calibrar), estos valores deben ser ajustados para un sensor específico y entorno
humedad_seco = 4095  # Valor máximo (suelo seco)
humedad_humedo = 1500  # Valor mínimo (suelo muy húmedo)

#SENSOR DE HUMEDAD DEL SUELO
def medir_humedad():
  valor_analogico = adc.read() #Mide la humedad del suelo y devuelve un valor entre 0 y 100
  humedad = int(((humedad_seco - valor_analogico) / (humedad_seco - humedad_humedo)) * 100) # Mapea el valor analógico a un rango de humedad
  humedad = max(0, min(humedad, 100)) # Asegura que la humedad esté entre 0 y 100
  return humedad

#BOMBA DE AGUA Y RELE
while True:
  humedad = medir_humedad()
  print("Humedad del suelo:", humedad, "%")
  time.sleep(1)

  # BOMBA DE AGUA
  bomba = Pin(2, Pin.OUT)
  if humedad <= 65:
   bomba.on()
  if humedad > 65:
   bomba.off()