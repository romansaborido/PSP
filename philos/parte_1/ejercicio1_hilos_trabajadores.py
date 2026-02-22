import threading
import random
import time


class HiloTrabajador(threading.Thread):
    """Hilo que simula a un trabajador realizando tareas en bucle."""

    # Número de iteraciones por hilo (evita bucle infinito real)
    MAX_ITERACIONES: int = 3

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def run(self) -> None:
        """Ejecuta las tareas del trabajador durante MAX_ITERACIONES ciclos."""
        iteracion: int = 0

        while iteracion < HiloTrabajador.MAX_ITERACIONES:
            print(f"Soy {self.name} y estoy trabajando")

            # Pausa aleatoria entre 1 y 10 segundos
            tiempo_espera: int = random.randint(1, 10)
            time.sleep(tiempo_espera)

            print(f"Soy {self.name} y he terminado de trabajar")
            iteracion += 1


if __name__ == "__main__":
    nombres: list[str] = ["Carlos", "María", "Pedro", "Lucía", "Andrés"]

    hilos: list[HiloTrabajador] = [HiloTrabajador(nombre) for nombre in nombres]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("Todos los hilos han finalizado.")
