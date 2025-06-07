class Cuadrado:
    def __init__(self, largo_lado):
        self.largo_lado = largo_lado
    def area(self):
        return self.largo_lado ** 2
    def perimetro(self):
        return self.largo_lado * 4
    


cuadrado1 = Cuadrado(5)
cuadrado2 = Cuadrado(10)
cuadrado3 = Cuadrado(15)


area_total = cuadrado1.area() + cuadrado2.area()

print(f"El área total de los cuadrados 1 y 2 es {area_total}.")