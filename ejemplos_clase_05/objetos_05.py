class Persona():
    def constructor(self, cnombre, cedad, ccabello):
        self.nombre = cnombre
        self.edad = cedad
        self.cabello = ccabello

    def quiensoy(self):
        print(f"Hola, soy {self.nombre}, tengo {self.edad} años y mi cabello es {self.cabello}.")


# instanciacion del objeto a partir de la clase Persona

persona1 = Persona()
persona1.constructor("Juan", 30, "canoso")

persona1.quiensoy()
