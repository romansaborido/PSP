# Proceso 2
def proceso2_temperatura_maxima(dia):

    # Leer temperaturas del fichero correspondiente al día
    nombre_fichero = f"{dia:02d}-12.txt"
    
    with open(nombre_fichero, 'r') as f:
        temperaturas = [float(linea.strip()) for linea in f]
    
    # Encontrar la temperatura máxima
    temp_maxima = max(temperaturas)
    
    # Escribir en maximas.txt (añadiendo al final del fichero)
    with open('maximas.txt', 'a') as f:
        f.write(f"{dia:02d}-12:{temp_maxima}\n")
    
    print(f"Temperatura máxima del día {dia:02d}-12: {temp_maxima}°C")