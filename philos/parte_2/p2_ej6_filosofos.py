import threading
import random
import time


class Filosofo(threading.Thread):
    """Hilo que representa a un filósofo en el problema de los filósofos de Dijkstra.

    Cada filósofo necesita dos palillos (el suyo y el del vecino) para comer.
    La estrategia para evitar interbloqueo es que el filósofo con índice mayor
    tome siempre primero el palillo de mayor índice. Esto rompe la simetría
    y evita que todos los filósofos cojan a la vez su palillo izquierdo,
    lo que causaría un deadlock circular.
    """

    # Un Lock por palillo, compartido entre los filósofos adyacentes
    palillos: list[threading.Lock] = [threading.Lock() for _ in range(5)]

    def __init__(self, indice: int) -> None:
        threading.Thread.__init__(self, name=f"Filósofo-{indice}")
        self._indice: int = indice
        self._palillo_izq: int = indice
        self._palillo_der: int = (indice + 1) % 5

    def _orden_adquisicion(self) -> tuple[int, int]:
        """Determina el orden en que se deben tomar los palillos para evitar deadlock.

        El filósofo siempre toma primero el palillo de menor índice.
        Esto impide el ciclo circular de esperas que causa interbloqueo.

        Returns:
            Tupla (primero, segundo) con los índices en orden de adquisición.
        """
        primero: int = min(self._palillo_izq, self._palillo_der)
        segundo: int = max(self._palillo_izq, self._palillo_der)
        return primero, segundo

    def _pensar(self) -> None:
        """Simula el tiempo de reflexión del filósofo."""
        print(f"{self.name} está pensando")
        time.sleep(random.randint(1, 3))

    def _comer(self) -> None:
        """Toma los palillos en orden seguro, come y los suelta."""
        primero, segundo = self._orden_adquisicion()

        # Tomar palillos en el orden que evita deadlock
        Filosofo.palillos[primero].acquire()
        Filosofo.palillos[segundo].acquire()

        print(f"{self.name} está comiendo con palillos {self._palillo_izq} y {self._palillo_der}")
        time.sleep(random.randint(1, 3))
        print(f"{self.name} ha terminado de comer y suelta los palillos")

        # Siempre soltar en orden inverso al de adquisición
        Filosofo.palillos[segundo].release()
        Filosofo.palillos[primero].release()

    def run(self) -> None:
        """Ciclo de vida del filósofo: piensa y come repetidamente."""
        ciclos: int = 3
        iteracion: int = 0

        while iteracion < ciclos:
            self._pensar()
            self._comer()
            iteracion += 1

        print(f"{self.name} ha terminado su sesión")


if __name__ == "__main__":
    print("=== Problema de los filósofos de Dijkstra ===")
    print("Estrategia anti-deadlock: tomar siempre primero el palillo de menor índice\n")

    hilos: list[Filosofo] = [Filosofo(i) for i in range(5)]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\nTodos los filósofos han terminado.")

    print("""
=== Análisis de la solución ===

¿Se produce interbloqueo?
  No. Al obligar a todos los filósofos a tomar primero el palillo de MENOR índice,
  se rompe el ciclo de espera circular. El filósofo 4 tomaría primero el palillo 0
  (menor entre 0 y 4) en lugar del 4, lo que impide que se forme el anillo de bloqueo.

¿Podría un filósofo no comer nunca (inanición)?
  Sí, es teóricamente posible aunque improbable. Si los filósofos 0, 1, 2 y 3
  consiguen siempre los palillos antes de que el filósofo 4 los pueda tomar,
  y este patrón se repite indefinidamente, el filósofo 4 nunca comería.
  En la práctica, con tiempos aleatorios esto es extremadamente improbable,
  pero la solución no garantiza formalmente equidad (fairness).
  Para garantizarla habría que usar una cola de espera ordenada (p. ej. con Condition).
""")
