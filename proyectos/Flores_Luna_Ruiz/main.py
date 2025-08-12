from machine import Pin, PWM, ADC
import time
import onewire, ds18x20

# --- Estados y salidas de la MEF ---
Q0 = 0 #Ideal
Q1 = 1 #Control de temperatura 
Q2 = 2 #Volteo
Q3 = 3 #Eclosion

S0 = 0  # sin acción
S1 = 1  # lámpara
S2 = 2  # ventilador
S3 = 3  # humidificador
S4 = 4  # volteo
S5 = 5  # luz roja (fin de ciclo)

# --- Tablas de transición y salida ---
tablaTran = [
    [Q1, Q1, Q1, Q3],
    [Q1, Q1, Q1, Q3],
    [Q1, Q1, Q1, Q3],
    [Q1, Q1, Q1, Q3],
    [Q0, Q0, Q0, Q3],
    [Q1, Q1, Q1, Q3],
    [Q1, Q1, Q1, Q3],
    [Q1, Q1, Q1, Q3],
    [Q1, Q1, Q1, Q3],
    [Q2, Q2, Q2, Q3],
    [Q3, Q3, Q3, Q3]
]

tablaSalida = [
    [S1, S1, S1, S5],  # fila 0
    [S1, S1, S1, S5],  # fila 1
    [S1, S1, S1, S5],  # fila 2
    [S3, S3, S0, S5],  # fila 3 
    [S0, S0, S0, S5],  # fila 4
    [S2, S2, S0, S5],  # fila 5 
    [S2, S2, S2, S5],  # fila 6
    [S2, S2, S2, S5],  # fila 7
    [S2, S2, S2, S5],  # fila 8
    [S4, S4, S4, S5],  # fila 9 
    [S5, S5, S5, S5]   # fila 10 
]

# --- Pines de hardware ---
servo          = PWM(Pin(18), freq=50)
lampara        = Pin(5,  Pin.OUT)
ventilador     = Pin(2,  Pin.OUT)
humidificador  = Pin(4, Pin.OUT)
led_rojo       = Pin(15, Pin.OUT)

pot_adc = ADC(Pin(35))
pot_adc.width(ADC.WIDTH_12BIT)

ow   = onewire.OneWire(Pin(12))
ds   = ds18x20.DS18X20(ow)
roms = ds.scan()

# --- Variables de control ---
servo_pos      = 0
lastVolteoTime = time.ticks_ms()
startTime      = time.ticks_ms()
estado         = Q0

def servo_write(angle):
    duty = int((angle / 180) * 75 + 40)
    servo.duty(duty)

def lectura_entradas():
    global startTime

    # Evento final de incubación (54 segundos)
    E = time.ticks_diff(time.ticks_ms(), startTime) >= 54000
    if E:
        return 10, None  # forzar fila 10 (luz roja)

    # --- Humedad desde potenciómetro (promedio de 5 muestras) ---
    muestras = [pot_adc.read() for _ in range(5)]
    raw_pot = sum(muestras) / len(muestras)
    nivel   = raw_pot * (100 / 4095)

    if nivel < 20:
        H = 0
    elif nivel < 80:
        H = 1
    else:
        H = 2

    print(f"Potencia: {nivel:.1f}% → H = {H}")

    # --- Temperatura DS18B20 ---
    ds.convert_temp()
    time.sleep_ms(750)
    temp = ds.read_temp(roms[0])
    print(f"Temperatura {temp:.1f}°C")

    # Clasificación de temperatura
    if temp < 36.0:
        T = 0
    elif temp <= 39.0:
        T = 1
    else:
        T = 2

    fila = T * 3 + H
    return fila, H

def escritura_salidas(fila, est, H):
    salida = tablaSalida[fila][est]
    print(f"Fila {fila} | Estado Q{est} | H={H} → Salida S{salida}")

    # Reset de salidas
    lampara.value(0)
    ventilador.value(0)
    humidificador.value(0)
    led_rojo.value(0)

    if salida == S0:
        print("Sin acción")
    elif salida == S1:
        lampara.value(1)
        print("Lámpara ON")
    elif salida == S2:
        ventilador.value(1)
        print("Ventilador ON")
    elif salida == S3:
        humidificador.value(1)
        print("Humidificador ON")
    elif salida == S5:
        led_rojo.value(1)
        print("Luz roja ON")

# --- Bucle principal ---
print("Arrancando incubadora con servo cada segundo...")

# Inicializaciones previas
lastVolteoTime = time.ticks_ms()
servo_pos       = 0
estado          = 0   # estado inicial Q0

while True:
    fila, H = lectura_entradas()

    if fila != 10 and time.ticks_diff(time.ticks_ms(), lastVolteoTime) >= 1000:
        servo_pos = 180 if servo_pos == 0 else 0
        print("Volteo servo a", servo_pos)
        servo_write(servo_pos)
        lastVolteoTime = time.ticks_ms()

    escritura_salidas(fila, estado, H)
    new_estado = tablaTran[fila][estado]
    print(f"Fila {fila}  Humedad H={H}  → transición Q{estado} → Q{new_estado}")
    estado = new_estado

    time.sleep(0.5)
