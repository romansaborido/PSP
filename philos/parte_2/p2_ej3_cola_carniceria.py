import threading
import random
import time


class ClienteCarniceria(threading.Thread):
    """Hilo que representa un cliente en la carnicería.

    La carnicería tiene 4 empleados, por lo que pueden atender 4 clientes
    simultáneamente. El resto debe esperar usando un Semáforo.
    """

    # Semáforo que representa los 4 empleados disponibles
    empleados: threading.Semaphore = threading.Semaphore(4)

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def _ser_atendido(self) -> None:
        """Espera a que haya un empleado libre y simula la atención en carnicería."""
        print(f"El cliente {self.name} está esperando en la carnicería")

        # Espera a que haya un empleado disponible (decrementa el semáforo)
        ClienteCarniceria.empleados.acquire()

        print(f"El cliente {self.name} está siendo atendido")
        tiempo_preparacion: int = random.randint(1, 10)
        time.sleep(tiempo_preparacion)
        print(f"El cliente {self.name} ha terminado en la carnicería")

        # Libera al empleado para que atienda al siguiente cliente
        ClienteCarniceria.empleados.release()

    def run(self) -> None:
        """Gestiona el ciclo completo del cliente en la carnicería."""
        self._ser_atendido()


if __name__ == "__main__":
    num_clientes: int = 10
    hilos: list[ClienteCarniceria] = [
        ClienteCarniceria(f"Cliente-{i}") for i in range(num_clientes)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\nTodos los clientes han sido atendidos en la carnicería.")
