lista1 = [1,2,3,4]

lista2 = ["a", "b", "c", "d"]

# Concatenar listas
# lista_nueva = [1, 2, 3, 4, "a", "b", "c", "d"]

lista_nueva = lista1 + lista2
print(lista_nueva)

print("--"*20)

lista1.extend(lista2)
print(lista1)