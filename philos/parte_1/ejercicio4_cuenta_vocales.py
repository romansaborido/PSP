import threading


class ContadorVocal(threading.Thread):
    """Hilo que cuenta las ocurrencias de una vocal específica en un texto."""

    # Resultado compartido: diccionario vocal -> cantidad
    resultados: dict[str, int] = {}

    def __init__(self, vocal: str, texto: str) -> None:
        threading.Thread.__init__(self, name=f"Hilo-{vocal}")
        self._vocal: str = vocal
        self._texto: str = texto

    def _contar_vocal(self) -> int:
        """Cuenta cuántas veces aparece la vocal en el texto (mayúsculas y minúsculas).
        
        Returns:
            Número de apariciones de la vocal.
        """
        texto_minusculas: str = self._texto.lower()
        return texto_minusculas.count(self._vocal)

    def run(self) -> None:
        """Cuenta la vocal asignada y almacena el resultado en el diccionario compartido."""
        cantidad: int = self._contar_vocal()
        ContadorVocal.resultados[self._vocal] = cantidad
        print(f"{self.name}: la vocal '{self._vocal}' aparece {cantidad} veces")


if __name__ == "__main__":
    texto_ejemplo: str = (
        "El murciélago alado sobrevolaba oscuros árboles en una tarde de invierno. "
        "Aullaba el viento entre las hojas mientras el río fluía silencioso hacia el oeste."
    )

    print(f"Texto analizado:\n{texto_ejemplo}\n")

    vocales: list[str] = ["a", "e", "i", "o", "u"]

    hilos: list[ContadorVocal] = [
        ContadorVocal(vocal, texto_ejemplo) for vocal in vocales
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    # Mostrar resumen final
    total: int = sum(ContadorVocal.resultados.values())
    print(f"\nResumen: {ContadorVocal.resultados}")
    print(f"Total de vocales contadas: {total}")
