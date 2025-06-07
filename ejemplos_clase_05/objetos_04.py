# definir la clase

class Persona:

    estoy_moviendo = False

    def caminar(self):
        print("Iniciando el proceso de caminar...")
        self.estoy_moviendo = True

    def detener(self):
        print("Deteniendo el proceso de caminar...")
        self.estoy_moviendo = False



juan = Persona()

print(juan.estoy_moviendo)

juan.caminar()

print(juan.estoy_moviendo)

juan.detener()

print(juan.estoy_moviendo)