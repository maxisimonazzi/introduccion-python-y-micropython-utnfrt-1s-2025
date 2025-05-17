# Sumar todos los numeros que se ingresan hasta que se ingrese un 0

# Definimos la variable
suma = 0
numero = 5

while numero != 0:
    numero = int(input("Ingrese un numero (0 para salir): "))
    suma = suma + numero

print(f"La suma total de todos los numeros es {suma}")