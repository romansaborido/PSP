import threading
import random
import time


class ClienteTienda(threading.Thread):
    """Hilo que representa un cliente que visita tanto la carnicería como la charcutería.

    Cada sección tiene su propio semáforo. El cliente puede ser atendido en
    cualquier orden, y solo está completamente servido cuando ha pasado por ambas.
    """

    # Semáforo de carnicería: 4 empleados
    sem_carniceria: threading.Semaphore = threading.Semaphore(4)

    # Semáforo de charcutería: 2 empleados
    sem_charcuteria: threading.Semaphore = threading.Semaphore(2)

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def _visitar_carniceria(self) -> None:
        """Espera turno en carnicería y simula la atención."""
        print(f"El cliente {self.name} espera en Carnicería")
        ClienteTienda.sem_carniceria.acquire()

        print(f"El cliente {self.name} está siendo atendido en Carnicería")
        time.sleep(random.randint(1, 10))
        print(f"El cliente {self.name} ha terminado en Carnicería")

        ClienteTienda.sem_carniceria.release()

    def _visitar_charcuteria(self) -> None:
        """Espera turno en charcutería y simula la atención."""
        print(f"El cliente {self.name} espera en Charcutería")
        ClienteTienda.sem_charcuteria.acquire()

        print(f"El cliente {self.name} está siendo atendido en Charcutería")
        time.sleep(random.randint(1, 10))
        print(f"El cliente {self.name} ha terminado en Charcutería")

        ClienteTienda.sem_charcuteria.release()

    def run(self) -> None:
        """El cliente visita ambas secciones; el orden es aleatorio para mayor realismo.

        Al lanzar las dos visitas sin esperar entre ellas, el hilo puede ser
        atendido en la sección que antes tenga hueco, reflejando el comportamiento
        descrito en el enunciado.
        """
        # Hilo interno para visitar una sección mientras se espera en la otra
        hilo_carniceria: threading.Thread = threading.Thread(
            target=self._visitar_carniceria
        )
        hilo_charcuteria: threading.Thread = threading.Thread(
            target=self._visitar_charcuteria
        )

        # Lanzar ambas visitas en paralelo: el cliente hace cola en ambos sitios
        # y es atendido en el que primero tenga un empleado libre
        hilo_carniceria.start()
        hilo_charcuteria.start()

        # Esperar a que el cliente haya sido atendido en ambas secciones
        hilo_carniceria.join()
        hilo_charcuteria.join()

        print(f"El cliente {self.name} ha terminado todas sus compras")


if __name__ == "__main__":
    num_clientes: int = 10
    hilos: list[ClienteTienda] = [
        ClienteTienda(f"Cliente-{i}") for i in range(num_clientes)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\nTodos los clientes han completado sus compras.")
