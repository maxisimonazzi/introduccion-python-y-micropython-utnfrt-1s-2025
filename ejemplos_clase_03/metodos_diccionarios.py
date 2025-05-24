diccionario = {
    "nombre": "Juan",
    "edad": 30,
    "ciudad": "Madrid",
    "profesion": "Ingeniero"
    }

print(diccionario.keys())
print(diccionario.values())
print("--"*20)
print(diccionario.items())
print("--"*20)
diccionario.update({"pais": "España", "edad": 31})
print(f"Diccionario actualizado: {diccionario}")
diccionario.pop("ciudad")
print(f"Diccionario actualizado despues de pop: {diccionario}")