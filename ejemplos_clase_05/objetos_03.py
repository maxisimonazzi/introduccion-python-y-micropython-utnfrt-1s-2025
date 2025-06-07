# primer ejemplo
class Persona:
    piernas = 2
    brazos = 2

    def caminar(self):
        print("Estoy caminando")



# instanciacion del objeto a partir de la clase Persona
juan = Persona()
manuel = Persona()


# programa principal
print(f"Juan tiene {juan.piernas} piernas")
print(f"Juan tiene {juan.brazos} brazos")

print(f"Manuel tiene {manuel.piernas} piernas")
print(f"Manuel tiene {manuel.brazos} brazos")

# atributos de instancia

juan.pelo = "rubio"

print(f"Juan tiene el pelo {juan.pelo}")


# ejecutar un metodo de la clase

manuel.caminar()
