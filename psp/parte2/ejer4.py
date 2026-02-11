from multiprocessing import Process, Pipe
import time

def leer_y_filtrar_peliculas(ruta_fichero, año, conn):
    """Proceso 1: Lee el fichero y filtra películas por año"""
    print(f"\n[Proceso 1] Leyendo fichero: {ruta_fichero}")
    print(f"[Proceso 1] Filtrando películas del año {año}...\n")
    
    try:
        with open(ruta_fichero, 'r', encoding='utf-8') as fichero:
            contador = 0
            for linea in fichero:
                linea = linea.strip()
                if ';' in linea:
                    partes = linea.split(';')
                    if len(partes) == 2:
                        nombre_pelicula = partes[0].strip()
                        año_estreno = partes[1].strip()
                        
                        # Filtrar por año
                        if año_estreno == str(año):
                            print(f"[Proceso 1] Enviando: {nombre_pelicula} ({año_estreno})")
                            conn.send((nombre_pelicula, año_estreno))
                            contador += 1
        
        print(f"\n[Proceso 1] Total películas enviadas: {contador}")
        conn.send(None)
        conn.close()
        print("[Proceso 1] Finalizado\n")
    
    except FileNotFoundError:
        print(f"[Proceso 1] Error: No se encontró el fichero {ruta_fichero}")
        conn.send(None)
        conn.close()

def guardar_peliculas(conn):
    """Proceso 2: Recibe películas y las guarda en un fichero"""
    print("[Proceso 2] Esperando películas...\n")
    
    peliculas = []
    año_fichero = None
    
    dato = conn.recv()
    
    while dato is not None:
        nombre_pelicula, año_estreno = dato
        peliculas.append(nombre_pelicula)
        
        if año_fichero is None:
            año_fichero = año_estreno
        
        print(f"[Proceso 2] Recibida: {nombre_pelicula}")
        dato = conn.recv()
    
    conn.close()
    
    # Guardar en fichero
    if peliculas and año_fichero:
        nombre_fichero = f"peliculas{año_fichero}.txt"
        
        with open(nombre_fichero, 'w', encoding='utf-8') as fichero:
            for pelicula in peliculas:
                fichero.write(f"{pelicula}\n")
        
        print(f"\n[Proceso 2] {len(peliculas)} películas guardadas en {nombre_fichero}")
    else:
        print("\n[Proceso 2] No se recibieron películas")
    
    print("[Proceso 2] Finalizado")

if __name__ == '__main__':
    print("=== SISTEMA DE FILTRADO DE PELÍCULAS ===\n")
    
    # Solicitar datos al usuario
    while True:
        try:
            año = int(input("Introduce un año (menor al actual, 2026): "))
            if año < 2026:
                break
            else:
                print("Error: El año debe ser menor a 2026")
        except ValueError:
            print("Error: Introduce un número válido")
    
    ruta_fichero = input("Introduce la ruta al fichero de películas: ").strip()
    
    if not ruta_fichero:
        ruta_fichero = "peliculas.txt"
        print(f"Usando fichero por defecto: {ruta_fichero}")
    
    inicio = time.perf_counter()
    
    # Crear pipe para comunicación entre procesos
    left, right = Pipe()
    
    # Crear los dos procesos
    p1 = Process(target=leer_y_filtrar_peliculas, args=(ruta_fichero, año, right))
    p2 = Process(target=guardar_peliculas, args=(left,))
    
    # Lanzar procesos
    print("\n" + "="*50)
    p1.start()
    p2.start()
    
    # Esperar a que terminen
    p1.join()
    p2.join()
    
    final = time.perf_counter()
    
    print("\n" + "="*50)
    print(f"Tiempo de ejecución: {final - inicio:.4f} segundos")
    print("Todos los procesos han terminado")