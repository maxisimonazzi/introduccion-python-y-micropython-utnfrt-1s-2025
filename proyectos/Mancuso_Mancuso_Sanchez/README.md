# 🏗️ Proyecto: Grúa controlada con Joystick (ESP32 + MicroPython)

## 🔧 Descripción general
Este proyecto implementa una grúa didáctica controlada mediante un **módulo joystick** y **dos servomotores** usando un **ESP32**. El joystick envía las posiciones de los ejes X e Y para mover los servos que simulan el desplazamiento horizontal y vertical de la grúa. Se aplica una zona muerta para evitar movimientos indeseados por ruido del joystick.

---

## 🛠 Componentes utilizados
- ESP32 (DevKit v1 o similar)
- 2 servomotores (SG90 o similares)
- Módulo joystick analógico (ejes X e Y)
- Cables, protoboard y alimentación 5V

---

## 🔌 Diagrama de conexión
- Joystick:
  - VCC → 3V3
  - GND → GND
  - Eje X (VRx) → `GPIO25` (ADC)
  - Eje Y (VRy) → `GPIO33` (ADC)
- Servomotores:
  - Servo eje X: señal PWM → `GPIO5`, VCC 5V, GND común
  - Servo eje Y: señal PWM → `GPIO18`, VCC 5V, GND común

> Importante: usa 5V estables para los servos y comparte GND con el ESP32. Considera fuente externa si los servos demandan corriente.

---

## 📲 Funcionamiento
- Se leen continuamente los valores analógicos de `joyX` y `joyY` (0–4095) con atenuación `ADC.ATTN_11DB`.
- Se aplica una zona muerta (`deadZone = 500`) centrada en 2048 para evitar jitter.
- Para cada eje:
  - Si el valor está por debajo de `2048 - deadZone`, el ángulo aumenta (hasta 180°).
  - Si está por encima de `2048 + deadZone`, el ángulo disminuye (hasta 0°).
- Los servos se inicializan en 90° y se actualizan con pasos de 1° cada 15 ms, logrando un movimiento suave.

---

## 🧩 Explicación del código
- PWM para servos a 50 Hz con `machine.PWM(Pin(...))`.
- Conversión ángulo → pulso en µs con `mover_servo(servo, angle)` que mapea 0–180° a 500–2500 µs (`duty_ns`).
- Lectura analógica de joystick en `GPIO25` y `GPIO33` con `ADC.ATTN_11DB` (rango completo ~3.3V).
- Variables `anguloX` y `anguloY` mantienen el estado y se actualizan según la posición del joystick.

---

## ▶️ Cómo usar
1. Flashea MicroPython en tu ESP32 (por ejemplo con Thonny).
2. Conecta el circuito según el diagrama y usa una fuente de 5V adecuada para los servos.
3. Copia `main.py` a la raíz del ESP32.
4. Ajusta `deadZone`, límites de ángulo o mapeos si tu joystick/servos requieren calibración.
5. Ejecuta `main.py` y controla la grúa moviendo el joystick en ambos ejes.

---

## 🎥 Video
https://youtu.be/bRjtQjNJUL8

---

## ✅ Conclusión
Un proyecto ideal para aprender control de **PWM**, lectura **ADC** y filtrado básico (zona muerta), con aplicación práctica en control de movimiento con servos.

## 👥 Integrantes
- Mancuso Meuli, Nahuel
- Mancuso Meuli, Tomas
- Sanchez, Leandro
