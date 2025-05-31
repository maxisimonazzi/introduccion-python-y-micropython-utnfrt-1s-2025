# definir la funcion

def obtenerDescuento(precio, descuento):
    descuento = precio * descuento/100
    precioFinal = precio - descuento
    print()
    print(f"Precio original: ${precio:.2f}")
    print(f"Descuento aplicado: ${descuento:.2f}")
    print(f"Precio final: ${precioFinal:.2f}")
    print()
    print("Gracias por su compra")


# programa principal

print("Bienvenido a la tienda")
precio = int(input("Ingrese el precio del producto: "))
descuento = int(input("Ingrese el porcentaje de descuento: "))
obtenerDescuento(precio, descuento)