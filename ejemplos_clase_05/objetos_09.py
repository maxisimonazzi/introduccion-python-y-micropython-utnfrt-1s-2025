class Persona():
    def __init__(self, cnombre, cedad, ccabello):
        self.nombre = cnombre
        self.edad = cedad
        self.cabello = ccabello

    def __str__(self):
        return f"Hola, soy {self.nombre}, tengo {self.edad} años y mi cabello es {self.cabello}."
    
    def __del__(self):
        print(f"Hola, soy {self.nombre} y este es mi ultimo aliento, voy a desaparecer.")


persona4 = Persona("María", 35, "castaño")
persona1 = Persona("Juan", 30, "canoso")
persona2 = Persona("Ana", 25, "rubio")
persona3 = Persona("Luis", 40, "negro")

print(persona1)


input("Presiona Enter para continuar...")
input("Presiona Enter para continuar...")
input("Presiona Enter para continuar...")


input("Presione enter para terminar el programa y eliminar el objeto.")
