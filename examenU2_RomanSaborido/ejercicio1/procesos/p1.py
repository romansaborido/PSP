import random

# Proceso 1
def proceso1_generar_temperaturas(dia):

    # Generar 24 temperaturas aleatorias entre 0 y 20 con 2 decimales
    temperaturas = [round(random.uniform(0, 20), 2) for _ in range(24)]
    
    # Crear nombre del fichero con formato DD-12.txt (DD con 2 dígitos)
    nombre_fichero = f"{dia:02d}-12.txt"
    
    # Escribir las temperaturas en el fichero (una por línea)
    with open(nombre_fichero, 'w') as f:
        for temp in temperaturas:
            f.write(f"{temp}\n")
    
    print(f"Generadas temperaturas para el día {dia:02d}-12")