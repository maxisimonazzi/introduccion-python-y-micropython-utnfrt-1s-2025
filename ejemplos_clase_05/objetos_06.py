class Persona():
    def __init__(self, cnombre, cedad, ccabello):
        self.nombre = cnombre
        self.edad = cedad
        self.cabello = ccabello

    def quiensoy(self):
        print(f"Hola, soy {self.nombre}, tengo {self.edad} años y mi cabello es {self.cabello}.")


persona1 = Persona("Juan", 30, "canoso")
persona1.quiensoy()