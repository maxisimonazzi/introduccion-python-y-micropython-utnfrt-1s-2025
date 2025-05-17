"""Escriba un codigo que permita hacer un descuento del 10%
si paga en efectivo y un recargo del 5% si paga con tarjeta de credito."""

# Definimos las variables
precio = int(input("Ingrese el precio del producto: "))
forma_de_pago = input("Ingrese E si paga en efectivo o T si paga con tarjeta de credito: ").upper()

if forma_de_pago == "E":
    precio_final = precio * 0.9  # Descuento del 10%
    print(f"El precio final es: {precio_final}")
elif forma_de_pago == "T":
    precio_final = precio * 1.05
    print(f"El precio final es: {precio_final}")
else:
    print("Forma de pago no válida")