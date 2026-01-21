from multiprocessing import Process

def sum(num):
    suma = 0
    for i in range (1, num + 1):
        suma += i
    print(suma)

if __name__ == "__main__":
    p1 = Process(target=sum, args=(5,))
    p2 = Process(target=sum, args=(10,))
    p1.start()
    p1.join()
    p2.start()
    p2.join()
    print("Todos los procesos han terminado")
