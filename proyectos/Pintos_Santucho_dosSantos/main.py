##################################################
#  Programa para abrir cerradura con 2 botones   #
##################################################
#             Importaciones              #
##########################################
from machine import Pin
from time import sleep

##########################################
#          Definicion de pines           #
##########################################

# Defino pines de los LEDs y botones
led = Pin(15, Pin.OUT) # Led de control de apertura
  
boton1 = Pin(25, Pin.IN, Pin.PULL_UP)  # Botón 1 → Boton Negro (1 binario), valor 0 al presionar
boton2 = Pin(26, Pin.IN, Pin.PULL_UP) # Botón 2 → Boton rojo (0 binario) valor 0 al presionar

# Iniciacion de variable de registro #
registro = [0, 0, 0, 0]  # 4 bits
posicion = 0             # Posición actual para escribir el bit
# Número a previamente seteado como clave a comparar ====
comparar = [1, 0, 1, 0]  # Pass prefijada: 1010
##########################################
#        Definicion de funciones         #
##########################################
# Función para comparar #
def coincide(a, b):
    return a == b
print("Iniciando... Presiona botones para formar el registro binario.")

while True:
    # Botón 1 presionado → agrega 1
    if boton1.value() == 0:  # activo en bajo
        registro[posicion] = 1
        posicion += 1
        print(f"Bit {posicion}: 1")
        sleep(0.3)  # Antirrebote

    # Botón 2 presionado → agrega 0
    if boton2.value() == 0: # activo en bajo
        registro[posicion] = 0
        posicion += 1
        print(f"Bit {posicion}: 0")
        sleep(0.3)  # Antirrebote
        
        # Si ya se llenaron los 4 bits
    if posicion >= 4:
        print("Registro ingresado:", ''.join(str(b) for b in registro))

        if coincide(registro, comparar):
            print("Coincide con Clave, Apertura")
            led.value(1)  # Enciende LED
        else:
            print("No coincide con clave, nuevo intento")
            led.value(0)  # Apaga LED

        # Reset para siguiente intento
        registro = [0, 0, 0, 0]
        posicion = 0
        sleep(1)
