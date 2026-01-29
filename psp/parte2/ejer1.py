from multiprocessing import Pool
import time

def contar_vocal(vocal):
    """Cuenta cuántas veces aparece una vocal en el fichero"""
    try:
        with open(r'C:\Users\portatil\Desktop\roman\dam\PSP\psp\parte2\texto.txt', 'r', encoding='utf-8') as fichero:
            contenido = fichero.read().lower()
            contador = contenido.count(vocal.lower())
            return (vocal, contador)
    except FileNotFoundError:
        print(f"Error: No se encontró el fichero texto.txt")
        return (vocal, 0)

if __name__ == '__main__':
    vocales = ['a', 'e', 'i', 'o', 'u']
    
    inicio = time.perf_counter()
    
    with Pool(processes=5) as pool:
        resultados = pool.map(contar_vocal, vocales)
    
    final = time.perf_counter()
    
    print("\n=== CONTEO DE VOCALES ===")
    for vocal, cantidad in resultados:
        print(f"Vocal '{vocal}': {cantidad} veces")
    
    print(f"\nTiempo de ejecución: {final - inicio:.4f} segundos")
    print("Todos los procesos han terminado")