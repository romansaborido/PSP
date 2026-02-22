import threading
import time
import random


class Peaton(threading.Thread):
    """Hilo que representa a un peatón esperando cruzar el paso de cebra.

    Los peatones llegan en momentos distintos y esperan en una barrera.
    Un temporizador (semáforo de tráfico) libera la barrera periódicamente,
    permitiendo que todos los que están esperando crucen a la vez.
    """

    # Event que representa el semáforo en verde (cruce permitido)
    semaforo_verde: threading.Event = threading.Event()

    # Lock para imprimir mensajes de cruce de forma ordenada
    lock_print: threading.Lock = threading.Lock()

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def _esperar_verde(self) -> None:
        """El peatón espera hasta que el semáforo se ponga en verde."""
        with Peaton.lock_print:
            print(f"{self.name} llega al paso y espera (semáforo en ROJO)")
        Peaton.semaforo_verde.wait()

    def _cruzar(self) -> None:
        """Simula el tiempo que tarda el peatón en cruzar."""
        tiempo_cruce: float = round(random.uniform(2.0, 5.0), 1)
        with Peaton.lock_print:
            print(f"{self.name} está cruzando (tardará {tiempo_cruce}s)")
        time.sleep(tiempo_cruce)
        with Peaton.lock_print:
            print(f"{self.name} ha cruzado")

    def run(self) -> None:
        """El peatón espera el verde y cruza."""
        self._esperar_verde()
        self._cruzar()


class SemaforoTrafico:
    """Controla el ciclo del semáforo usando un Timer.

    Alterna entre rojo (Event no seteado) y verde (Event seteado)
    con temporizadores, liberando a los peatones que estén esperando.
    """

    def __init__(self, segundos_rojo: int, segundos_verde: int) -> None:
        self._segundos_rojo: int = segundos_rojo
        self._segundos_verde: int = segundos_verde
        self._ciclos_completados: int = 0
        self._max_ciclos: int = 3

    def _poner_verde(self) -> None:
        """Pone el semáforo en verde y programa el siguiente cambio a rojo."""
        print("\n🟢 SEMÁFORO EN VERDE — ¡Los peatones pueden cruzar!\n")
        Peaton.semaforo_verde.set()

        timer_rojo: threading.Timer = threading.Timer(
            self._segundos_verde, self._poner_rojo
        )
        timer_rojo.start()

    def _poner_rojo(self) -> None:
        """Pone el semáforo en rojo y programa el siguiente cambio a verde."""
        Peaton.semaforo_verde.clear()
        self._ciclos_completados += 1
        print(f"\n🔴 SEMÁFORO EN ROJO (ciclo {self._ciclos_completados}/{self._max_ciclos})\n")

        if self._ciclos_completados < self._max_ciclos:
            timer_verde: threading.Timer = threading.Timer(
                self._segundos_rojo, self._poner_verde
            )
            timer_verde.start()

    def iniciar(self) -> None:
        """Arranca el ciclo del semáforo comenzando en rojo."""
        print("🔴 SEMÁFORO EN ROJO — Esperando peatones...\n")
        timer_verde: threading.Timer = threading.Timer(
            self._segundos_rojo, self._poner_verde
        )
        timer_verde.start()


if __name__ == "__main__":
    print("=== PASO DE PEATONES ===\n")

    semaforo: SemaforoTrafico = SemaforoTrafico(segundos_rojo=4, segundos_verde=5)
    semaforo.iniciar()

    # Los peatones llegan en momentos distintos
    nombres: list[str] = [
        "Peatón-1", "Peatón-2", "Peatón-3", "Peatón-4",
        "Peatón-5", "Peatón-6", "Peatón-7"
    ]

    hilos: list[Peaton] = []
    for nombre in nombres:
        hilo: Peaton = Peaton(nombre)
        hilos.append(hilo)
        hilo.start()
        # Cada peatón llega con un pequeño retraso
        time.sleep(random.uniform(0.5, 2.5))

    for hilo in hilos:
        hilo.join()

    print("\nTodos los peatones han cruzado.")
