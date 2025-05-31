def raizn(numero, raiz):
    resultado = numero ** (1 / raiz)
    print(f"La raíz {raiz} de {numero} es: {resultado}")

# programa principal
print("Bienvenido al calculador de raíces")
numero = float(input("Ingrese el número: "))
raiz = int(input("Ingrese el valor de la raíz: "))
raizn(numero, raiz)