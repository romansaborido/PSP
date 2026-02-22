import threading
import queue
import random
import time


class Productor(threading.Thread):
    """Hilo productor que genera datos y los introduce en la cola compartida.

    Si la cola está llena (capacidad 1), espera hasta que el consumidor retire
    el dato actual antes de introducir uno nuevo.
    """

    def __init__(self, nombre: str, cola: queue.Queue, num_items: int) -> None:
        threading.Thread.__init__(self, name=nombre)
        self._cola: queue.Queue = cola
        self._num_items: int = num_items

    def _producir_item(self, indice: int) -> int:
        """Genera un dato simulado.

        Args:
            indice: Número de secuencia del item producido.

        Returns:
            Valor entero generado aleatoriamente.
        """
        time.sleep(random.uniform(0.5, 1.5))
        return random.randint(1, 100)

    def run(self) -> None:
        """Produce num_items datos y los introduce en la cola."""
        items_producidos: int = 0

        while items_producidos < self._num_items:
            dato: int = self._producir_item(items_producidos)

            # put() bloquea automáticamente si la cola está llena (block=True por defecto)
            self._cola.put(dato)
            print(f"{self.name} ha producido: {dato} | Cola: {self._cola.qsize()} elemento(s)")

            items_producidos += 1

        print(f"{self.name} ha terminado de producir")


class Consumidor(threading.Thread):
    """Hilo consumidor que extrae datos de la cola compartida y los procesa.

    Si la cola está vacía, espera hasta que el productor introduzca un dato.
    """

    def __init__(self, nombre: str, cola: queue.Queue, num_items: int) -> None:
        threading.Thread.__init__(self, name=nombre)
        self._cola: queue.Queue = cola
        self._num_items: int = num_items

    def _procesar_item(self, dato: int) -> None:
        """Simula el procesamiento del dato recibido.

        Args:
            dato: Valor extraído de la cola a procesar.
        """
        time.sleep(random.uniform(0.5, 2.0))
        print(f"{self.name} ha consumido: {dato}")

    def run(self) -> None:
        """Consume num_items datos de la cola."""
        items_consumidos: int = 0

        while items_consumidos < self._num_items:
            # get() bloquea automáticamente si la cola está vacía (block=True por defecto)
            dato: int = self._cola.get()
            self._procesar_item(dato)

            # Marcar la tarea como completada para que queue.join() pueda finalizar
            self._cola.task_done()
            items_consumidos += 1

        print(f"{self.name} ha terminado de consumir")


if __name__ == "__main__":
    NUM_ITEMS: int = 6

    print("=" * 55)
    print("  PRODUCTOR-CONSUMIDOR — Cola de capacidad 1")
    print("=" * 55)
    print(
        "Con capacidad 1, el productor SIEMPRE debe esperar a que\n"
        "el consumidor retire el dato antes de introducir el siguiente.\n"
        "Esto crea un ritmo estrictamente alternado: produce → consume → produce…\n"
    )

    # Cola con capacidad máxima 1
    cola_1: queue.Queue = queue.Queue(maxsize=1)

    productor_1: Productor = Productor("Productor", cola_1, NUM_ITEMS)
    consumidor_1: Consumidor = Consumidor("Consumidor", cola_1, NUM_ITEMS)

    productor_1.start()
    consumidor_1.start()

    productor_1.join()
    consumidor_1.join()

    print("\n" + "=" * 55)
    print("  PRODUCTOR-CONSUMIDOR — Cola de capacidad 5")
    print("=" * 55)
    print(
        "Con capacidad 5, el productor puede adelantarse hasta 5 items\n"
        "sin esperar al consumidor, siempre que la cola no se llene.\n"
        "Ambos hilos trabajan de forma más independiente y el productor\n"
        "solo se bloquea cuando la cola está completamente llena.\n"
    )

    # Cola con capacidad máxima 5
    cola_5: queue.Queue = queue.Queue(maxsize=5)

    productor_5: Productor = Productor("Productor", cola_5, NUM_ITEMS)
    consumidor_5: Consumidor = Consumidor("Consumidor", cola_5, NUM_ITEMS)

    productor_5.start()
    consumidor_5.start()

    productor_5.join()
    consumidor_5.join()

    print("""
=== Análisis comparativo ===

Cola de capacidad 1:
  - El productor y el consumidor se sincronizan de forma estricta.
  - El productor se bloquea inmediatamente tras cada producción
    hasta que el consumidor retire el dato.
  - El flujo es secuencial: produce → consume → produce → consume…
  - Útil cuando el consumidor debe procesar cada dato antes de que
    se genere el siguiente (p. ej. procesamiento en tiempo real).

Cola de capacidad 5:
  - El productor puede generar hasta 5 datos antes de bloquearse.
  - El consumidor puede procesar ráfagas de datos sin que el
    productor tenga que esperar en cada iteración.
  - Ambos hilos trabajan de forma más independiente, lo que mejora
    el rendimiento si hay diferencias de velocidad entre ellos.
  - La lógica de sincronización NO cambia: queue.Queue gestiona
    internamente los bloqueos con put() y get(). Solo cambia
    el parámetro maxsize en el constructor.

Conclusión:
  El cambio de capacidad 1 a 5 es mínimo en el código (un solo parámetro),
  pero tiene un impacto significativo en el comportamiento en tiempo de ejecución.
""")
