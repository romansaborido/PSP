from multiprocessing import Pool
from time import time

def sum(num):
    suma = 0
    for i in range(1, num + 1):
        suma += i
    return suma

numeros = [1, 2, 3, 4, 5]

if __name__ == "__main__":

    inicio_p1 = time()

    with Pool(processes=3) as pool:
        res1 = pool.map(sum, numeros)

    fin_p1 = time()

    print(f"El pool 1 tardo {fin_p1 - inicio_p1:.4f} segundos en ejecutarse y su resultado es -> {res1}")

    inicio_p2 = time()

    with Pool(processes=5) as pool:
        res2 = pool.map(sum, numeros)

    fin_p2 = time()

    print(f"El pool 2 tardo {fin_p2 - inicio_p2:.4f} segundos en ejecutarse y su resultado es -> {res2}")