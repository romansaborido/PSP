from multiprocessing import Process, Queue
import time

def leer_fichero(nombre_fichero, cola, num_procesos):
    with open(nombre_fichero, "r") as f:
        for linea in f:
            a, b = map(int, linea.split())
            cola.put((a, b))

    # Enviar valores para indicar fin
    for _ in range(num_procesos):
        cola.put(None)

def sumar_rango(cola):
    for datos in iter(cola.get, None):
        a, b = datos
        inicio = min(a, b)
        fin = max(a, b)
        resultado = sum(range(inicio, fin + 1))

        print(f"Suma de {inicio} a {fin}: {resultado}")


if __name__ == "__main__":
    fichero = "numeros.txt"
    num_procesos = 3

    cola = Queue()
    procesos = []

    # Proceso lector
    p_lector = Process(target=leer_fichero, args=(fichero, cola, num_procesos))
    p_lector.start()

    # Procesos sumadores
    for _ in range(num_procesos):
        p = Process(target=sumar_rango, args=(cola,))
        procesos.append(p)
        p.start()

    # Esperar a que todos terminen
    p_lector.join()
    for p in procesos:
        p.join()

    print("Todos los procesos han terminado")
