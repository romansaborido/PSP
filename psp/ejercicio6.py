from multiprocessing import Pool

def sumar_rango(a, b):
    # Aseguramos el orden correcto aunque a > b
    inicio = min(a, b)
    fin = max(a, b)

    resultado = sum(range(inicio, fin + 1))
    print(f"Suma de {inicio} a {fin}: {resultado}")

if __name__ == "__main__":
    # Pares de valores a procesar
    valores = [(1, 10), (20, 5), (3, 4), (7, 15)]

    # Crear el Pool de procesos
    with Pool() as pool:
        # Ejecutar la función de forma concurrente
        pool.starmap(sumar_rango, valores)

    # Este mensaje se imprime cuando todos los procesos han terminado
    print("Todos los procesos han terminado")
