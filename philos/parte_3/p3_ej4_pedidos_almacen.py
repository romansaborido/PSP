import threading
import random
import time


class Trabajador(threading.Thread):
    """Hilo que representa a un trabajador en el almacén.

    Todos los trabajadores esperan en una barrera inicial para comenzar
    al mismo tiempo. A continuación, esperan a que un Event indique que
    hay un pedido disponible, lo procesan, y vuelven a esperar el siguiente.
    El ciclo se repite un número fijo de veces.
    """

    # Barrera que sincroniza el inicio simultáneo de todos los trabajadores
    barrera_inicio: threading.Barrier = threading.Barrier(5)

    # Event que indica si hay un pedido disponible para preparar
    pedido_disponible: threading.Event = threading.Event()

    # Número de pedidos que procesará cada trabajador
    NUM_PEDIDOS: int = 3

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def _esperar_pedido(self) -> None:
        """Bloquea al trabajador hasta que se genere un pedido."""
        print(f"{self.name} está esperando un pedido...")
        Trabajador.pedido_disponible.wait()

    def _preparar_pedido(self) -> None:
        """Simula la preparación de un pedido y marca el evento como no seteado."""
        # Marcar inmediatamente el evento como no seteado para que el siguiente
        # pedido no sea tomado por los demás hasta que se genere uno nuevo
        Trabajador.pedido_disponible.clear()

        tiempo_preparacion: float = round(random.uniform(1.0, 3.0), 1)
        print(f"{self.name} está preparando un pedido (tardará {tiempo_preparacion}s)")
        time.sleep(tiempo_preparacion)
        print(f"{self.name} ha terminado de preparar su pedido")

    def run(self) -> None:
        """Ciclo completo: espera inicio, luego procesa NUM_PEDIDOS pedidos."""
        print(f"{self.name} está listo para empezar")

        # Todos esperan a que el último trabajador esté listo
        Trabajador.barrera_inicio.wait()
        print(f"{self.name} ¡comienza a trabajar!")

        pedidos_procesados: int = 0

        while pedidos_procesados < Trabajador.NUM_PEDIDOS:
            self._esperar_pedido()
            self._preparar_pedido()
            pedidos_procesados += 1

        print(f"{self.name} ha completado todos sus pedidos y descansa")


class GeneradorPedidos:
    """Genera pedidos periódicamente usando un Timer que se autorreprograma."""

    def __init__(self, intervalo: float, num_pedidos: int) -> None:
        self._intervalo: float = intervalo
        self._pedidos_restantes: int = num_pedidos

    def _generar_pedido(self) -> None:
        """Setea el Event de pedido y programa el siguiente si quedan más."""
        if self._pedidos_restantes > 0:
            self._pedidos_restantes -= 1
            print(f"\n📦 NUEVO PEDIDO GENERADO ({self._pedidos_restantes} restantes)\n")
            Trabajador.pedido_disponible.set()

            # Programar el siguiente pedido solo si quedan más
            if self._pedidos_restantes > 0:
                timer: threading.Timer = threading.Timer(
                    self._intervalo, self._generar_pedido
                )
                timer.start()

    def iniciar(self) -> None:
        """Arranca el primer temporizador de generación de pedidos."""
        timer: threading.Timer = threading.Timer(
            self._intervalo, self._generar_pedido
        )
        timer.start()


if __name__ == "__main__":
    print("=== PEDIDOS DE ALMACÉN ===\n")

    # El generador producirá un pedido cada 4 segundos, en total 15
    # (5 trabajadores x 3 pedidos = 15, aunque compiten entre sí)
    NUM_PEDIDOS_TOTAL: int = 15
    generador: GeneradorPedidos = GeneradorPedidos(
        intervalo=4.0, num_pedidos=NUM_PEDIDOS_TOTAL
    )

    nombres: list[str] = ["Trabajador-A", "Trabajador-B", "Trabajador-C",
                          "Trabajador-D", "Trabajador-E"]

    hilos: list[Trabajador] = [Trabajador(nombre) for nombre in nombres]

    for hilo in hilos:
        hilo.start()

    # Arrancar el generador de pedidos tras un pequeño margen
    # para que todos los hilos estén ya en la barrera
    time.sleep(0.5)
    generador.iniciar()

    for hilo in hilos:
        hilo.join()

    print("\nTodos los trabajadores han completado sus pedidos.")
