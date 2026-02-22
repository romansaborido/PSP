import threading
import random
import time


class Persona(threading.Thread):
    """Hilo que representa a una persona encerrada en el Escape Room.

    Cada persona intenta adivinar el código de 4 cifras de forma independiente.
    Cuando alguien lo descubre, lo notifica mediante un Event. Luego, todas las
    personas se reúnen en una Barrier antes de salir juntas.
    """

    # Código secreto de 4 cifras a adivinar
    CODIGO_SECRETO: str = str(random.randint(1000, 9999))

    # Event que se activa cuando alguien adivina el código
    codigo_encontrado: threading.Event = threading.Event()

    # Barrera que asegura que todos esperan antes de salir juntos
    barrera_salida: threading.Barrier = threading.Barrier(5)

    # Nombre de quien encontró el código
    quien_encontro: str = ""
    lock_descubridor: threading.Lock = threading.Lock()

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def _generar_intento(self) -> str:
        """Genera un código aleatorio de 4 cifras.

        Returns:
            Cadena de 4 dígitos como intento de código.
        """
        return str(random.randint(1000, 9999))

    def _buscar_codigo(self) -> None:
        """Genera intentos hasta acertar el código o hasta que otro lo encuentre."""
        intento: str = self._generar_intento()

        while not Persona.codigo_encontrado.is_set() and intento != Persona.CODIGO_SECRETO:
            time.sleep(random.uniform(0.1, 0.3))
            intento = self._generar_intento()

        # Comprobar si este hilo fue el que acertó (y no lo encontró otro antes)
        if intento == Persona.CODIGO_SECRETO and not Persona.codigo_encontrado.is_set():
            with Persona.lock_descubridor:
                # Segunda comprobación dentro del lock para evitar doble escritura
                if not Persona.codigo_encontrado.is_set():
                    Persona.quien_encontro = self.name
                    Persona.codigo_encontrado.set()
                    print(f"¡{self.name} ha encontrado el código: {intento}!")

    def run(self) -> None:
        """Ciclo completo: busca el código, espera a los demás y sale junto al grupo."""
        print(f"{self.name} está buscando el código...")
        self._buscar_codigo()

        print(f"{self.name} espera a los demás para salir juntos")

        # Todos esperan en la barrera hasta que el último llegue
        Persona.barrera_salida.wait()

        print(f"{self.name} ¡sale del Escape Room!")


if __name__ == "__main__":
    print("=== ESCAPE ROOM ===")
    print(f"(Código secreto para verificar al final: {Persona.CODIGO_SECRETO})\n")

    nombres: list[str] = ["Ana", "Bruno", "Carmen", "Daniel", "Elena"]

    hilos: list[Persona] = [Persona(nombre) for nombre in nombres]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print(f"\n¡Todos han salido! Fue {Persona.quien_encontro} quien encontró el código.")
