from multiprocessing import Pool
from procesos.p1 import proceso1_generar_temperaturas
from procesos.p2 import proceso2_temperatura_maxima
from procesos.p3 import proceso3_temperatura_minima


if __name__ == '__main__':
    print("=== EJERCICIO 1: Registro de temperaturas de diciembre ===\n")
    
    # Limpiar archivos de ejecuciones previas
    open('maximas.txt', 'w').close()
    open('minimas.txt', 'w').close()
    
    # Generar temperaturas para los 31 días de diciembre
    print("FASE 1: Generando temperaturas para 31 días...")
    
    # Usamos Pool para ejecutar 31 veces el proceso1 de forma simultánea
    with Pool(processes=31) as pool:

        # map ejecuta proceso1_generar_temperaturas para cada día (1 a 31)
        pool.map(proceso1_generar_temperaturas, range(1, 32))
    
    print("\nTemperaturas generadas para todos los días\n")
    
    # FASE 2: Calcular temperaturas máximas y mínimas de forma simultánea
    print("FASE 2: Calculando temperaturas máximas y mínimas...")
    
    # Usamos Pool para ejecutar simultáneamente los procesos 2 y 3. Cada pool ejecuta su función para los 31 días
    with Pool(processes=31) as pool:

        # Lanzar proceso2 para calcular máximas de todos los días
        pool.map(proceso2_temperatura_maxima, range(1, 32))
    
    with Pool(processes=31) as pool:

        # Lanzar proceso3 para calcular mínimas de todos los días
        pool.map(proceso3_temperatura_minima, range(1, 32))
    
    print("\nTemperaturas máximas y mínimas calculadas")
    print("\nRESULTADO\n=========")
    print("Se han generado los siguientes archivos:")
    print("31 archivos de temperaturas: 01-12.txt hasta 31-12.txt")
    print("maximas.txt: contiene las temperaturas máximas de cada día")
    print("minimas.txt: contiene las temperaturas mínimas de cada día")
