from machine import Pin, PWM
import time

# --- Configuración del servo ---
SERVO_PIN = 2
servo = PWM(Pin(SERVO_PIN), freq=50)

def servo_angle(angle):
    duty = int((angle / 180) * 100 + 25)
    servo.duty(duty)
    time.sleep(0.5)

# --- Configuración del LED ---
LED_PIN = 5
led = Pin(LED_PIN, Pin.OUT)

# --- Configuración del sensor ultrasónico ---
TRIG_PIN = 14
ECHO_PIN = 15

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def medir_distancia():
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    timeout_us = 30000  # 30 ms
    pulse_start = time.ticks_us()
    
    while echo.value() == 0:
        if time.ticks_diff(time.ticks_us(), pulse_start) > timeout_us:
            return -1
    
    pulse_start_time = time.ticks_us()

    while echo.value() == 1:
        if time.ticks_diff(time.ticks_us(), pulse_start_time) > timeout_us:
            return -1

    pulse_end_time = time.ticks_us()
    
    duration = time.ticks_diff(pulse_end_time, pulse_start_time)
    distance = (duration / 2) / 29.1
    
    return distance

# --- Bucle principal del programa ---
while True:
    dist = medir_distancia()
    
    if dist != -1:
        print("Distancia:", dist, "cm")

        if dist < 50:
            print("Objeto detectado.")
            servo_angle(90)
            led.on()  # Enciende el LED
        else:
            print("No hay objeto.")
            servo_angle(0)
            led.off() # Apaga el LED
    else:
        print("Error al medir la distancia")
        servo_angle(0)
        led.off() # Apaga el LED por seguridad
    
    time.sleep(1)