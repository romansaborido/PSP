import threading
import random
import time


class Corredor(threading.Thread):
    """Hilo que representa a un corredor en una carrera.

    Todos los corredores esperan en la barrera de salida hasta que
    se completa la cuenta atrás. Al arrancar, cada uno corre durante
    un tiempo aleatorio y registra su tiempo final.
    """

    # Barrera que sincroniza la salida de todos los corredores
    barrera_salida: threading.Barrier = threading.Barrier(10)

    # Registro de tiempos: nombre -> segundos
    tiempos: dict[str, float] = {}

    # Lock para escribir en el diccionario de tiempos de forma segura
    lock_tiempos: threading.Lock = threading.Lock()

    def __init__(self, nombre: str) -> None:
        threading.Thread.__init__(self, name=nombre)

    def _cuenta_atras(self) -> None:
        """Realiza la cuenta atrás antes de la salida.

        Solo la ejecuta el primer corredor que llega a la barrera
        (el que recibe n_waiting == 0 al llamar a wait()).
        En este diseño se llama antes del wait() para que todos la vean.
        """
        for cuenta in range(3, 0, -1):
            print(f"  {cuenta}...")
            time.sleep(1)
        print("  ¡PISTOLATAZO! ¡Salid todos!\n")

    def _correr(self) -> float:
        """Simula el tiempo que tarda el corredor en completar la carrera.

        Returns:
            Tiempo en segundos que ha tardado en terminar.
        """
        tiempo_carrera: float = round(random.uniform(5.0, 15.0), 2)
        time.sleep(tiempo_carrera)
        return tiempo_carrera

    def _registrar_tiempo(self, tiempo: float) -> None:
        """Guarda el tiempo del corredor en el registro compartido de forma segura.

        Args:
            tiempo: Segundos que ha tardado el corredor.
        """
        with Corredor.lock_tiempos:
            Corredor.tiempos[self.name] = tiempo

    def run(self) -> None:
        """Ciclo completo del corredor: llega, espera la salida y corre."""
        print(f"{self.name} está en la línea de salida")

        # El primer hilo en llegar hace la cuenta atrás; los demás esperan
        posicion: int = Corredor.barrera_salida.wait()
        if posicion == 0:
            self._cuenta_atras()

        # Segunda barrera: todos arrancan a la vez tras la cuenta atrás
        Corredor.barrera_salida.wait()

        tiempo: float = self._correr()
        self._registrar_tiempo(tiempo)
        print(f"{self.name} ha terminado la carrera en {tiempo:.2f} segundos")


if __name__ == "__main__":
    print("=== CARRERA ===\n")
    print("Los corredores se están colocando en la salida...\n")

    nombres: list[str] = [
        "Usain", "Mo", "Eliud", "Wayde", "David",
        "Christian", "Yohan", "Noah", "André", "Marcell"
    ]

    hilos: list[Corredor] = [Corredor(nombre) for nombre in nombres]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    # Mostrar clasificación final ordenada por tiempo
    print("\n=== CLASIFICACIÓN FINAL ===")
    clasificacion: list[tuple[str, float]] = sorted(
        Corredor.tiempos.items(), key=lambda par: par[1]
    )
    for puesto, (nombre, tiempo) in enumerate(clasificacion, start=1):
        print(f"  {puesto}. {nombre}: {tiempo:.2f} segundos")
