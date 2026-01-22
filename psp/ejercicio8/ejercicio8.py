from multiprocessing import Process, Pipe

def leer_fichero(nombre_fichero, conn):
    with open(nombre_fichero, "r") as f:
        for linea in f:
            a, b = map(int, linea.split())
            conn.send((a, b))

    # Enviar señal de fin
    conn.send(None)
    conn.close()

def sumar_rango(conn):
    for datos in iter(conn.recv, None):
        a, b = datos
        inicio = min(a, b)
        fin = max(a, b)
        resultado = sum(range(inicio, fin + 1))

        print(f"Suma de {inicio} a {fin}: {resultado}")

    conn.close()


if __name__ == "__main__":
    fichero = "numeros.txt"

    # Crear la tubería
    conn_padre, conn_hijo = Pipe()

    # Proceso lector (envía datos)
    p_lector = Process(target=leer_fichero, args=(fichero, conn_hijo))

    # Proceso sumador (recibe datos)
    p_sumador = Process(target=sumar_rango, args=(conn_padre,))

    p_lector.start()
    p_sumador.start()

    p_lector.join()
    p_sumador.join()

    print("Todos los procesos han terminado.")
