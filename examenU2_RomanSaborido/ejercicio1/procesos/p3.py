# Proceso 3
def proceso3_temperatura_minima(dia):

    # Leer temperaturas del fichero correspondiente al día
    nombre_fichero = f"{dia:02d}-12.txt"
    
    with open(nombre_fichero, 'r') as f:
        temperaturas = [float(linea.strip()) for linea in f]
    
    # Encontrar la temperatura mínima
    temp_minima = min(temperaturas)
    
    # Escribir en minimas.txt (añadiendo al final del fichero)
    with open('minimas.txt', 'a') as f:
        f.write(f"{dia:02d}-12:{temp_minima}\n")
    
    print(f"Temperatura mínima del día {dia:02d}-12: {temp_minima}°C")