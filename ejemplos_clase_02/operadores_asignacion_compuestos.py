sumador = 0

# Aqui vamos a ver el ejemplo de un acumulador que guarda internamente la suma de los números que se le van ingresando

"""Aqui vamos a ver el ejemplo de un acumulador que 
guarda internamente la suma de los números que se le van ingresando"""

sumador += int(input("Ingrese un número: "))   # Suma el primer número
sumador += int(input("Ingrese otro número: "))  # Suma el segundo número
sumador += int(input("Ingrese otro número: "))  # Suma el tercer número

print(f"La suma es: {sumador}")
