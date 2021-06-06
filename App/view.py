"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """



import config as cf
import sys
import controller
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from App import controller
import time
import tracemalloc
assert cf



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Identificar los clústeres de comunicación (req. 1)")
    print("3- Identificar los puntos de conexión críticos de la red (req. 2)")
    print("4- Ruta de menor distancia (req. 3)")
    print("5- Identificar la infraestructura crítica de la red (req. 4)")
    print("6- Análisis de fallas (req. 5)")
    print("7- Mejores canales para transmitir (req. 6)")
    print("8- Mejor ruta para comunicarme (req. 7)")
    print("9- Graficando los grafos (req. 8)")
    print("0- Salir")
    print("*******************************************")


catalog = None


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.init() 
        rtas = controller.loadData(catalog)
        primerVertice = rtas[0]
        ultimoPais = rtas[1]
        numCountries = controller.totalLandingPoints(catalog)
        numLanding = controller.numeroPoints(catalog)
        numConexiones = controller.totalConexiones(catalog)
        controller.cargarClusteres(catalog)


        print('Total de landing points: ' + str(numLanding))
        print('Total de conexiones: '+ str(numConexiones))
        print('Total de Paises: ' + str(numCountries))
        print('Primer landing points cargados: ' + primerVertice['landing_point_id']
        +' || '+ primerVertice['name']+ ' || ' + primerVertice['latitude'] + ' || ' + 
        primerVertice['longitude'] )
        print('Ultimo pais cargado: ' + ultimoPais['CountryName'] + ' || ' +
        ultimoPais['Population'] + ' || ' + ultimoPais['Internet users'])
   

    elif int(inputs[0]) == 2:
        
        lp1 = input("Nombre del landing point 1: ")
        lp2 = input("Nombre del landing point 2: ")
        
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        

        respuesta = controller.getCantidadClusteres(catalog) 
        print('La cantidad de clusteres es: ' + str(respuesta))
        
        rta2 = controller.pertenecenCluster(catalog,lp1,lp2)
        print("*******************************************")
        print()
        if rta2:
            print('Los dos Landing Points pertencen al mismo cluster.')
        else:
            print('Los dos Landing Points NO pertencen al mismo cluster.')
    

        
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nTiempo [ms]: " + str(delta_time) + "  ||  " + 
              "Memoria [kB]: " + str(delta_memory) + "\n")

       
        
        

    elif int(inputs[0]) == 3:
       
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        

        respuesta = controller.conexionesLps(catalog)
       
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nTiempo [ms]: " + str(delta_time) + "  ||  " + 
              "Memoria [kB]: " + str(delta_memory) + "\n")
        
       

    elif int(inputs[0]) == 4:
        paisA = input("País origen: ")
        paisB = input("País destino: ")
        
   
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
      

        rta = controller.getRutaMenorDist(catalog, paisA, paisB)
        lis = rta[0]
        lista = lis['elements']
        distanciaTotal = rta[1]

        print("La ruta con distancias es: ")
        for n in lista: 
            peso = n['peso']
            vertice1 = n['vertice1']
            vertice2 = n['vertice2']
            print("Desde "+ vertice1 + " hasta " + vertice2 + " con "+ str(peso) + " Km.")
            print()
        print()
        print("******************************************")
        print("La disancia total es: " + str(distanciaTotal) + " Km.")

        
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nTiempo [ms]: " + str(delta_time) + "  ||  " + 
              "Memoria [kB]: " + str(delta_memory) + "\n")

       

    elif int(inputs[0]) == 5:
      
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
      

        rta = controller.redExpansion(catalog)

        pesoTotal = rta[0]
        numVertices = rta[1]
        distanciaMayor = rta[2]
        ramaMayor =  rta[3]

        print("El número de nodos conectados a la red de expansión mínima es: "+ str(numVertices))
        print("El costo total de la red de expansión mínima es: " + str(pesoTotal) + " Km.")
        print("La rama mas larga es: " + ramaMayor + " con " + str(distanciaMayor)+ " Km.")
     
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nTiempo [ms]: " + str(delta_time) + "  ||  " + 
              "Memoria [kB]: " + str(delta_memory) + "\n")
      
       
        

    elif int(inputs[0]) == 6:
        lp = input("Nombre del landing point: ")
        """
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        """
        
        rta = controller.getFallas(catalog, lp)
        numeroPaises = rta[0] 
        paises = rta[1]

        lista = paises['elements']
        print("El numero de paises afectados es: " + str(numeroPaises))
        for n in lista:
            print(n)

        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nTiempo [ms]: " + str(delta_time) + "  ||  " + 
              "Memoria [kB]: " + str(delta_memory) + "\n")

        print("\n++++++ Req. No. 5 results ... ++++++")
     

    elif int(inputs[0]) == 7:
        pais = input("Nombre del país: ")
        cable = input("Nombre del cable: ")

        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        respuesta = controller.getMejoresCanales(cont, pais, cable)

        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nTiempo [ms]: " + str(delta_time) + "  ||  " + 
              "Memoria [kB]: " + str(delta_memory) + "\n")

        print("\n++++++ Req. No. 6 results ... ++++++")        

    elif int(inputs[0]) == 8:
        ip1 = input("Dirección IP1: ")
        ip2 = input("Dirección IP2: ")

        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        respuesta = controller.getMejorRuta(cont, ip1, ip2)

        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nTiempo [ms]: " + str(delta_time) + "  ||  " + 
              "Memoria [kB]: " + str(delta_memory) + "\n")

        print("\n++++++ Req. No. 7 results ... ++++++")

    elif int(inputs[0]) == 9:
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()

        print("\n++++++ Req. No. 8 results ... ++++++")

        
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nTiempo [ms]: " + str(delta_time) + "  ||  " + 
              "Memoria [kB]: " + str(delta_memory) + "\n")

    else:
        sys.exit(0)
sys.exit(0)
