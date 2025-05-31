# ejemplo sobre como generar una casilla de email
# Reglas de generacion
# 1, colocar las primeras tres letra del nombre
# 2, seguido del apellido
# 3, agregar el año
# 4, seguido de @gmail.com

# Maximiliano Simonazzi 1983 -> maxsimonazzi1983@gmail.com

def generarMail(nombre, apellido, anio):
    print()
    print(f"Email generado: {nombre[0:3].lower()}{apellido.lower()}{anio}@hotmail.com")



# programa principal

a = input("Ingrese su nombre: ")
b = input("Ingrese su apellido: ")
c = int(input("Ingrese su año de nacimiento: "))

generarMail(a, b, c) # generarMail("Maximiliano", "Simonazzi", 1983)


generarMail("Paula", "Gomez", 1990) # generarMail("Paula", "Gomez", 1990)