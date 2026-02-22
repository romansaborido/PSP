import threading
import random


class AdivinaNumero(threading.Thread):
    """Hilo que intenta adivinar el número oculto generando valores aleatorios."""

    # Número a adivinar, compartido entre todos los hilos
    numero_oculto: int = random.randint(0, 100)

    # Indica si algún hilo ya ha acertado el número
    acertado: bool = False

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def _intentar_adivinar(self) -> bool:
        """Genera un número aleatorio y comprueba si coincide con el oculto.
        
        Returns:
            True si el hilo debe terminar su ejecución, False si debe continuar.
        """
        intento: int = random.randint(0, 100)

        # Verificar acierto
        if intento == AdivinaNumero.numero_oculto:
            AdivinaNumero.acertado = True
            print(f"{self.name} ha acertado el número: {intento}")
            return True

        # Verificar si otro hilo ya acertó
        if AdivinaNumero.acertado:
            print(f"{self.name} se detiene porque otro hilo ya acertó")
            return True

        return False

    def run(self) -> None:
        """Busca el número oculto hasta acertar o hasta que otro hilo lo encuentre."""
        terminado: bool = self._intentar_adivinar()

        while not terminado:
            terminado = self._intentar_adivinar()


if __name__ == "__main__":
    print(f"Número oculto a adivinar: {AdivinaNumero.numero_oculto}")

    hilos: list[AdivinaNumero] = [
        AdivinaNumero(f"Hilo-{i}") for i in range(10)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("Todos los hilos han finalizado.")
