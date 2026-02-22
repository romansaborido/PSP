import threading


class ContadorCompartido(threading.Thread):
    """Hilo que incrementa un contador compartido hasta alcanzar el límite."""

    # Variables de clase compartidas entre todos los hilos
    contador: int = 0
    LIMITE: int = 1000

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def run(self) -> None:
        """Incrementa el contador mientras no se alcance el límite."""
        while ContadorCompartido.contador < ContadorCompartido.LIMITE:
            ContadorCompartido.contador += 1

        print(f"Hilo {self.name} terminó. Contador actual: {ContadorCompartido.contador}")


if __name__ == "__main__":
    num_hilos: int = 10
    hilos: list[ContadorCompartido] = [
        ContadorCompartido(f"Hilo-{i}") for i in range(num_hilos)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print(f"\nValor final del contador: {ContadorCompartido.contador}")
    print("(Nota: sin sincronización, el valor puede superar 1000 por condiciones de carrera)")
