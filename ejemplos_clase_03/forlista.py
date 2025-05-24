lista = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
#         0    1    2    3    4    5    6    7    8    9   SUBINDICES
print(lista)

print("--"*20)
for i in range(0,10):
    print(lista[i])


print("--"*20)

lista_numeros_al_azar = [8, 6, 5, 4, 9, 12, 3, 2, 1, 2]
suma = 0
for i in range(0,len(lista_numeros_al_azar)):
    suma = suma + lista_numeros_al_azar[i]

print("La suma de los elementos de la lista es: ", suma)

print("--"*20)

lista_facil = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for i in lista_facil:
    print(i)