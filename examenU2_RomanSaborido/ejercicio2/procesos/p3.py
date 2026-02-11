# Proceso 3
def proceso3_escribir_fichero(conn_recepcion):
    
    print("Proceso 3: Escribiendo resultados en empleados.txt...")
    
    empleados_escritos = 0
    
    # Abrir el fichero de salida
    with open('empleados.txt', 'w', encoding='utf-8') as f:

        # Obtenemos la primera linea
        linea = conn_recepcion.recv()

        # Recibir líneas del proceso 2 hasta recibir None
        while linea is not None:
            
            # Separar campos
            campos = linea.split(';')
            
            if len(campos) == 3:
                nombre, apellido, salario = campos
                
                # Escribir en el formato: Apellido Nombre, Salario
                f.write(f"{apellido} {nombre}, {salario}\n")
                empleados_escritos += 1
            
            # Obtenemos la siguiente linea
            linea = conn_recepcion.recv()    
    
    conn_recepcion.close()
    
    print(f"Proceso 3: Se escribieron {empleados_escritos} empleados en empleados.txt")