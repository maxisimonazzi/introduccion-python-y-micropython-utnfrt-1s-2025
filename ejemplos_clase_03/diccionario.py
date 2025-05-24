diccionario = {
    "nombre": "Juan",
    "edad": 30,
    "ciudad": "Madrid",
    "profesion": "Ingeniero"
    }

print(f"El diccionario es: {diccionario}")
print(f"El tipo del diccionario es: {type(diccionario)}")
print("--"*20)
print(diccionario["nombre"])
print(diccionario["profesion"])
print("--"*20)
print(diccionario.get("pais", "Esa clave no existe"))