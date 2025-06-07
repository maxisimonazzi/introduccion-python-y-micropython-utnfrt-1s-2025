class Cuadrado:
    def __init__(self, largo_lado):
        self.largo_lado = largo_lado
    def area(self):
        print(f"El área del cuadrado es {self.largo_lado ** 2}.")
    def perimetro(self):
        print(f"El perímetro del cuadrado es {self.largo_lado * 4}.")
    


cuadrado1 = Cuadrado(5)
cuadrado2 = Cuadrado(10)
cuadrado3 = Cuadrado(15)

cuadrado1.area()
cuadrado2.area()
cuadrado3.area()

cuadrado1.perimetro()
cuadrado2.perimetro()
cuadrado3.perimetro()
