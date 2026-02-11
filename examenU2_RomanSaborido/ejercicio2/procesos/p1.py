# Proceso 1
def proceso1_filtrar_departamento(conn_envio, departamento):

    print(f"Proceso 1: Filtrando empleados del departamento '{departamento}'...")
    
    # Leer el fichero salarios.txt
    with open('salarios.txt', 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    # Filtrar y enviar líneas del departamento indicado
    empleados_enviados = 0
    for linea in lineas:
        # Separar los campos
        campos = linea.strip().split(';')
        
        if len(campos) == 4:
            nombre, apellido, salario, depto = campos
            
            # Si el departamento coincide, enviar la línea sin el departamento
            if depto == departamento:
                linea_sin_depto = f"{nombre};{apellido};{salario}"
                conn_envio.send(linea_sin_depto)
                empleados_enviados += 1
    
    # Enviar señal de finalización
    conn_envio.send(None)
    conn_envio.close()
    
    print(f"Proceso 1: Se enviaron {empleados_enviados} empleados del departamento '{departamento}'")