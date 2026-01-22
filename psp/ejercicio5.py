from multiprocessing import Process

def sumar_rango(a, b):
    # Aseguramos que el rango sea correcto aunque a > b
    inicio = min(a, b)
    fin = max(a, b)
    
    resultado = sum(range(inicio, fin + 1))
    print(f"Suma de {inicio} a {fin}: {resultado}")

if __name__ == "__main__":
    procesos = []

    # Lista de pares de valores para probar
    valores = [(1, 10), (20, 5), (3, 4), (7, 15)]

    # Crear y lanzar los procesos
    for a, b in valores:
        p = Process(target=sumar_rango, args=(a, b))
        procesos.append(p)
        p.start()

    # Esperar a que todos los procesos terminen
    for p in procesos:
        p.join()

    print("Todos los procesos han terminado")







