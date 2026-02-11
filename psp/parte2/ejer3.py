from multiprocessing import Process, Pool
import random
import time
import os

def generar_notas(ruta_fichero):
    """Proceso 1: Genera 6 notas aleatorias entre 1 y 10 con decimales"""
    notas = [round(random.uniform(1.0, 10.0), 2) for _ in range(6)]
    
    with open(ruta_fichero, 'w') as fichero:
        for nota in notas:
            fichero.write(f"{nota}\n")
    
    print(f"[Proceso 1] Notas generadas en {ruta_fichero}: {notas}")
    return ruta_fichero

def calcular_media(args):
    """Proceso 2: Lee notas de un fichero y calcula la media"""
    ruta_fichero, nombre_alumno = args
    
    try:
        with open(ruta_fichero, 'r') as fichero:
            notas = [float(linea.strip()) for linea in fichero]
        
        media = sum(notas) / len(notas)
        
        with open('medias.txt', 'a') as fichero:
            fichero.write(f"{media:.2f} {nombre_alumno}\n")
        
        print(f"[Proceso 2] Media de {nombre_alumno}: {media:.2f}")
        return (nombre_alumno, media)
    
    except FileNotFoundError:
        print(f"Error: No se encontró el fichero {ruta_fichero}")
        return (nombre_alumno, 0.0)

def obtener_nota_maxima():
    """Proceso 3: Lee medias.txt y obtiene la nota máxima"""
    try:
        with open('medias.txt', 'r') as fichero:
            lineas = fichero.readlines()
        
        if not lineas:
            print("[Proceso 3] No hay notas para procesar")
            return
        
        notas_alumnos = []
        for linea in lineas:
            partes = linea.strip().split(' ', 1)
            if len(partes) == 2:
                nota = float(partes[0])
                nombre = partes[1]
                notas_alumnos.append((nota, nombre))
        
        nota_maxima, alumno_mejor = max(notas_alumnos, key=lambda x: x[0])
        
        print("\n" + "="*50)
        print(f"[Proceso 3] NOTA MÁXIMA: {nota_maxima:.2f}")
        print(f"[Proceso 3] ALUMNO: {alumno_mejor}")
        print("="*50)
    
    except FileNotFoundError:
        print("[Proceso 3] Error: No se encontró el fichero medias.txt")

if __name__ == '__main__':
    print("=== SISTEMA DE GESTIÓN DE NOTAS ===\n")
    
    inicio = time.perf_counter()
    
    if os.path.exists('medias.txt'):
        os.remove('medias.txt')
    
    num_alumnos = 10
    
    print("--- Usando Pool ---\n")
    
    print("[PASO 1] Generando notas de 10 alumnos...")
    rutas_ficheros = [f"Alumno{i+1}.txt" for i in range(num_alumnos)]
    
    with Pool(processes=num_alumnos) as pool:
        pool.map(generar_notas, rutas_ficheros)
    
    print(f"\n[PASO 1] Completado - {num_alumnos} ficheros generados\n")
    
    print("[PASO 2] Calculando medias...")
    args_medias = [(f"Alumno{i+1}.txt", f"Alumno{i+1}") for i in range(num_alumnos)]
    
    with Pool(processes=num_alumnos) as pool:
        resultados = pool.map(calcular_media, args_medias)
    
    print(f"\n[PASO 2] Completado - {num_alumnos} medias calculadas\n")
    
    print("[PASO 3] Obteniendo nota máxima...")
    obtener_nota_maxima()
    
    final = time.perf_counter()
    
    print(f"\nTiempo de ejecución (Pool): {final - inicio:.4f} segundos")
    
    if os.path.exists('medias.txt'):
        os.remove('medias.txt')
    for i in range(num_alumnos):
        if os.path.exists(f"Alumno{i+1}.txt"):
            os.remove(f"Alumno{i+1}.txt")
    
    print("\n" + "="*50)
    print("\n--- Usando bucles for con Process ---\n")
    
    inicio2 = time.perf_counter()
    
    
    print("[PASO 1] Generando notas de 10 alumnos...")
    procesos_generacion = []
    
    for i in range(num_alumnos):
        p = Process(target=generar_notas, args=(f"Alumno{i+1}.txt",))
        procesos_generacion.append(p)
        p.start()
    
    for p in procesos_generacion:
        p.join()
    
    print(f"\n[PASO 1] Completado - {num_alumnos} ficheros generados\n")
    
    print("[PASO 2] Calculando medias...")
    procesos_medias = []
    
    for i in range(num_alumnos):
        p = Process(target=calcular_media, args=((f"Alumno{i+1}.txt", f"Alumno{i+1}"),))
        procesos_medias.append(p)
        p.start()
    
    for p in procesos_medias:
        p.join()
    
    print(f"\n[PASO 2] Completado - {num_alumnos} medias calculadas\n")
    
    print("[PASO 3] Obteniendo nota máxima...")
    p3 = Process(target=obtener_nota_maxima)
    p3.start()
    p3.join()
    
    final2 = time.perf_counter()
    
    print(f"\nTiempo de ejecución (bucles for): {final2 - inicio2:.4f} segundos")
    print("\nTodos los procesos han terminado")