import threading
import random
import time


class ClientePanaderia(threading.Thread):
    """Hilo que representa un cliente en la cola de la panadería.

    Solo hay un dependiente, por lo que los clientes son atendidos de uno en uno.
    Se usa un Lock como mecanismo de exclusión mutua.
    """

    # Lock que representa al único dependiente disponible
    dependiente: threading.Lock = threading.Lock()

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def _ser_atendido(self) -> None:
        """Espera a que el dependiente esté libre y simula la atención al cliente."""
        print(f"El cliente {self.name} está esperando ser atendido")

        # El cliente espera hasta que el dependiente quede libre
        ClientePanaderia.dependiente.acquire()

        print(f"El cliente {self.name} está siendo atendido")
        tiempo_atencion: int = random.randint(1, 5)
        time.sleep(tiempo_atencion)
        print(f"El cliente {self.name} ha sido atendido y se va de la panadería")

        ClientePanaderia.dependiente.release()

    def run(self) -> None:
        """Gestiona el ciclo completo del cliente en la panadería."""
        self._ser_atendido()


if __name__ == "__main__":
    num_clientes: int = 8
    hilos: list[ClientePanaderia] = [
        ClientePanaderia(f"Cliente-{i}") for i in range(num_clientes)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\nTodos los clientes han sido atendidos.")
