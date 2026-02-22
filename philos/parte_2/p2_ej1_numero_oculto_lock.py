import threading
import random


class AdivinaNumeroSync(threading.Thread):
    """Hilo que intenta adivinar el número oculto usando Lock para sincronización."""

    # Número a adivinar, compartido entre todos los hilos
    numero_oculto: int = random.randint(0, 100)

    # Indica si algún hilo ya ha acertado
    acertado: bool = False

    # Lock para proteger la comprobación y escritura de 'acertado'
    lock: threading.Lock = threading.Lock()

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def _comprobar_intento(self, intento: int) -> bool:
        """Comprueba el intento dentro de una sección crítica protegida por Lock.

        Args:
            intento: Número generado aleatoriamente por el hilo.

        Returns:
            True si el hilo debe terminar su ejecución, False si debe continuar.
        """
        # Adquirimos el lock para que solo un hilo a la vez compruebe y modifique 'acertado'
        AdivinaNumeroSync.lock.acquire()

        # Si ya acertó otro hilo mientras esperábamos, terminamos
        if AdivinaNumeroSync.acertado:
            AdivinaNumeroSync.lock.release()
            print(f"{self.name} se detiene: otro hilo ya acertó")
            return True

        # Comprobar si este hilo ha acertado
        if intento == AdivinaNumeroSync.numero_oculto:
            AdivinaNumeroSync.acertado = True
            AdivinaNumeroSync.lock.release()
            print(f"{self.name} ha acertado el número: {intento}")
            return True

        AdivinaNumeroSync.lock.release()
        return False

    def run(self) -> None:
        """Busca el número oculto hasta acertar o hasta que otro hilo lo encuentre."""
        intento: int = random.randint(0, 100)
        terminado: bool = self._comprobar_intento(intento)

        while not terminado:
            intento = random.randint(0, 100)
            terminado = self._comprobar_intento(intento)


if __name__ == "__main__":
    print(f"Número oculto a adivinar: {AdivinaNumeroSync.numero_oculto}\n")

    hilos: list[AdivinaNumeroSync] = [
        AdivinaNumeroSync(f"Hilo-{i}") for i in range(10)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\nTodos los hilos han finalizado.")
