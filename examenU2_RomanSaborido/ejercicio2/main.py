from multiprocessing import Process, Pipe
from ejercicio2.procesos.p1 import proceso1_filtrar_departamento
from ejercicio2.procesos.p2 import proceso2_filtrar_salario
from ejercicio2.procesos.p3 import proceso3_escribir_fichero


if __name__ == '__main__':
    print("\nEJERCICIO 2: Filtrado de empleados\n==================================")
    
    # Solicitar datos al usuario
    departamento = input("\nIntroduce el nombre del departamento: ")
    salario_minimo = float(input("Introduce el salario mínimo: "))
    
    print(f"\nBuscando empleados de '{departamento}' con salario >= {salario_minimo}\n")
    
    # Cada Pipe() devuelve dos extremos: uno para recibir y otro para enviar
    p1_envio, p2_recepcion = Pipe()
    p2_envio, p3_recepcion = Pipe()
    
   
    # Proceso 1: recibe el extremo de envío del primer pipe y el departamento
    proceso1 = Process(target=proceso1_filtrar_departamento, args=(p1_envio, departamento))
    
    # Proceso 2: recibe ambos extremos y el salario mínimo
    proceso2 = Process(target=proceso2_filtrar_salario, args=(p2_recepcion, p2_envio, salario_minimo))
    
    # Proceso 3: recibe el extremo de recepción del segundo pipe
    proceso3 = Process(target=proceso3_escribir_fichero, args=(p3_recepcion,))
    
    # Iniciamos los procesos
    proceso1.start()
    proceso2.start()
    proceso3.start()
    
    # Esperamos a que todos los procesos terminen
    proceso1.join()
    proceso2.join()
    proceso3.join()
    
    print("\nRESULTADO\n=========")
    print("El archivo 'empleados.txt' contiene los resultados del filtrado")
