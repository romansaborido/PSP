import threading
import random
import time


class Estudiante(threading.Thread):
    """Hilo que representa un estudiante que comparte libros con otros.

    Cada estudiante necesita exactamente 2 libros simultáneamente. Si alguno
    no está libre, espera. Los libros se devuelven siempre a la vez.
    Se usa Condition para coordinar el acceso al estado compartido de los libros.
    """

    # Estado de cada libro: True = ocupado, False = libre
    libros: list[bool] = [False] * 9

    # Condition para coordinar la espera y notificación entre estudiantes
    cond: threading.Condition = threading.Condition()

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def _seleccionar_libros(self) -> tuple[int, int]:
        """Selecciona aleatoriamente dos índices de libro distintos.

        Returns:
            Tupla con los dos índices de libro seleccionados.
        """
        indices: list[int] = random.sample(range(len(Estudiante.libros)), 2)
        return indices[0], indices[1]

    def _libros_disponibles(self, libro1: int, libro2: int) -> bool:
        """Comprueba si los dos libros seleccionados están libres.

        Args:
            libro1: Índice del primer libro.
            libro2: Índice del segundo libro.

        Returns:
            True si ambos libros están disponibles.
        """
        return not Estudiante.libros[libro1] and not Estudiante.libros[libro2]

    def _reservar_libros(self, libro1: int, libro2: int) -> None:
        """Espera hasta que ambos libros estén disponibles y los reserva.

        Args:
            libro1: Índice del primer libro a reservar.
            libro2: Índice del segundo libro a reservar.
        """
        with Estudiante.cond:
            # Esperar mientras alguno de los libros esté ocupado
            while not self._libros_disponibles(libro1, libro2):
                print(
                    f"{self.name} espera: libros {libro1+1} o {libro2+1} ocupados"
                )
                Estudiante.cond.wait()

            # Ambos libros libres: los marcamos como ocupados
            Estudiante.libros[libro1] = True
            Estudiante.libros[libro2] = True
            print(f"{self.name} ha cogido los libros {libro1+1} y {libro2+1}")

    def _devolver_libros(self, libro1: int, libro2: int) -> None:
        """Devuelve los dos libros y notifica a los estudiantes que esperan.

        Args:
            libro1: Índice del primer libro a devolver.
            libro2: Índice del segundo libro a devolver.
        """
        with Estudiante.cond:
            Estudiante.libros[libro1] = False
            Estudiante.libros[libro2] = False
            print(f"{self.name} ha devuelto los libros {libro1+1} y {libro2+1}")
            # Notificar a todos los estudiantes que están esperando
            Estudiante.cond.notify_all()

    def run(self) -> None:
        """Selecciona dos libros, los usa un tiempo aleatorio y los devuelve."""
        libro1, libro2 = self._seleccionar_libros()

        self._reservar_libros(libro1, libro2)

        # Usa los libros durante un tiempo aleatorio entre 3 y 5 segundos
        tiempo_uso: int = random.randint(3, 5)
        time.sleep(tiempo_uso)

        self._devolver_libros(libro1, libro2)


if __name__ == "__main__":
    nombres_estudiantes: list[str] = ["Alejandro", "Beatriz", "Carlos", "Diana"]

    hilos: list[Estudiante] = [Estudiante(nombre) for nombre in nombres_estudiantes]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\nTodos los estudiantes han terminado de usar sus libros.")
