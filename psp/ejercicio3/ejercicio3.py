from multiprocessing import Process, Queue

def leer_numeros(ruta_fichero, cola):
    with open(ruta_fichero, "r", encoding="utf-8") as file:
        for linea in file:
            linea = linea.strip()      # quitar espacios y saltos de línea
            if linea:                  # evitar líneas vacías
                cola.put(int(linea))  # o int(linea) si son enteros
    cola.put(None)

def sumar_numeros(cola):
    suma: int = 0
    numero = cola.get()
    while numero is not None:
        suma += numero
        numero = cola.get()
    print(f"Suma total = {suma}")    


if __name__ == '__main__':
    cola = Queue()

    proceso_leer = Process(target=leer_numeros, args=("./numeros.txt", cola))
    proceso_sumar = Process(target=sumar_numeros, args=(cola,))

    proceso_leer.start()
    proceso_sumar.start()

    proceso_leer.join()
    proceso_sumar.join()


