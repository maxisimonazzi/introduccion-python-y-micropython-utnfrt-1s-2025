lista = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print(f"Lista original: {lista}")
# Pop un elemento de la lista
elemento = lista.pop()
print(f"Elemento eliminado: {elemento}")
print(f"Lista después de eliminar el último elemento: {lista}")
# Pop un elemento de la lista en una posición específica
elemento2 = lista.pop(5)
print(f"Elemento eliminado en la posición 5: {elemento2}")
print(f"Lista después de eliminar el elemento en la posición 5: {lista}")