from multiprocessing import Process, Pipe

def leer_numeros(ruta_fichero, conn):
    with open(ruta_fichero, "r", encoding="utf-8") as file:
        for linea in file:
            linea = linea.strip()
            if linea:
                conn.send(int(linea))
    conn.send(None)
    conn.close()

def sumar_numeros(conn):
    suma: int = 0
    numero = conn.recv()
    while numero is not None:
        suma += numero
        numero = conn.recv()
    print(f"Suma total = {suma}")
    conn.close()


if __name__ == '__main__':

    conn1, conn2 = Pipe()

    proceso_lector = Process(target=leer_numeros, args=('./numeros.txt', conn1))
    proceso_sumar = Process(target=sumar_numeros, args=(conn2,))

    proceso_lector.start()
    proceso_sumar.start()

    proceso_lector.join()
    proceso_sumar.join()

