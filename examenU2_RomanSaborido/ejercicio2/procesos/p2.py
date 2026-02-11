# Proceso 2
def proceso2_filtrar_salario(conn_recepcion, conn_envio, salario_minimo):
    
    print(f"Proceso 2: Filtrando empleados con salario >= {salario_minimo}...")
    
    empleados_enviados = 0

    # Obtenemos la primera linea
    linea = conn_recepcion.recv()

    # Recibir líneas del proceso 1 hasta recibir None
    while linea is not None:        
        
        # Separar campos: Nombre;Apellido;Salario
        campos = linea.split(';')
        
        if len(campos) == 3:
            nombre, apellido, salario = campos
            salario_num = float(salario)
            
            # Si el salario cumple el mínimo, enviar al proceso 3
            if salario_num >= salario_minimo:
                conn_envio.send(linea)
                empleados_enviados += 1

        # Obtenemos la siguiente linea        
        linea = conn_recepcion.recv()        
    
    # Enviar señal de finalización (None)
    conn_envio.send(None)
    conn_recepcion.close()
    conn_envio.close()
    
    print(f"Proceso 2: Se enviaron {empleados_enviados} empleados con salario >= {salario_minimo}")