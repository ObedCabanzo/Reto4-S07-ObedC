"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """



from math import inf
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as omp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as dj
from DISClib.Algorithms.Graphs import prim
from DISClib.ADT.graph import gr
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

   landing_points: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar los puntos de conexion 
   components: Almacena la informacion de los componentes conectados
   countrys:  Tabla de hash que almacena los paises cargados y su informacion  
    """
    try:
        analyzer = {
                    'connections': None,  
                    'countrys':None,
                    'landing_points':None,
                    'componentes': None
                   }

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=10,
                                              comparefunction=compareIds) 
        analyzer['countrys'] = mp.newMap(numelements=100,
                                     maptype='PROBING', loadfactor=0.5,
                                     comparefunction=compareIds)
        analyzer['landing_points'] = mp.newMap(numelements=100,
                                     maptype='PROBING', loadfactor=0.5,
                                     comparefunction=compareIds)
        analyzer['landing_points_name'] = mp.newMap(numelements=100,
                                     maptype='PROBING', loadfactor=0.5,
                                     comparefunction=compareIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')
         

# Funciones para agregar informacion al catalogo


def newConnection(analyzer, connection):
    """
    Crea conexiones entre landing points (arcos)
    """
    grafo = analyzer['connections']
    dist = connection['cable_length']
    dist1 = dist.split(" ")
    dist2 = dist1[0].replace(",","")
    if dist2 == 'n.a.':
        dist2 = inf
    distancia = float(dist2)

    origen = connection['\ufefforigin']
    destino = connection['destination']
    cable = connection['cable_name']
    
    forigen = formatVertex(origen,cable)
    fdestino = formatVertex(destino,cable)
    
    existOrigen = gr.containsVertex(grafo, forigen)
    existDestino = gr.containsVertex(grafo, fdestino)
    

    try:

        if not existOrigen and not existDestino:
            addVertice(analyzer,forigen)
            addVertice(analyzer,fdestino)
            addConnection(analyzer,forigen,fdestino,distancia)
            addMapLP(analyzer,origen,forigen,connection)
            addMapLP(analyzer,destino,fdestino,connection)

        else: 
            if not existOrigen:
                addVertice(analyzer,forigen)
                addMapLP(analyzer,origen,forigen,connection)
            if not existDestino:
                addVertice(analyzer,fdestino)
                addMapLP(analyzer,destino,fdestino,connection)

            estanUnidos = estanConectados(grafo,forigen,fdestino)

            if not estanUnidos:
                addConnection(analyzer,forigen,fdestino,distancia)
        
            


    except Exception as exp:
        error.reraise(exp, 'model:addConnection')
    None

def addConnection(analyzer, origen, destino,distancia):
    """
    Crea conexiones entre landing points (arcos)
    """
    grafo = analyzer['connections']
    try:
        gr.addEdge(grafo,origen,destino,distancia)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addConnection')
        
# Funciones para creacion de datos

def addMapLP(analyzer, origen,forigen,connection):

    """
    Añade elementos al mapa de landingPoints e inicializa una lista
    para cada uno de ellos, donde se guardan los diferentes cables que llegan 
    a cada LP.
    """

    mapLp = analyzer['landing_points']
 
    if mp.contains(mapLp,origen):
        entry = mp.get(mapLp,origen)
        valor = me.getValue(entry)
        banda  = connection['capacityTBPS']
        dist = connection['cable_length']
        dist1 = dist.split(" ")
        dist2 = dist1[0].replace(",","")
        if dist2 == 'n.a.':
            dist2 = inf
        distancia = float(dist2)

        cable = connection['cable_name']

        lista = valor['lista']

        tamaño = lt.size(lista)
        if tamaño == 0:
            lt.addLast(lista, forigen)
            valor['menorAncho'] = banda
            valor['cable'] = cable
            valor['distancia'] = distancia
            
        else: 
            ultimo = lt.lastElement(lista)
            addConnection(analyzer,ultimo,forigen, 0.1 )
            lt.addLast(lista, forigen)

            if banda < valor['menorAncho']:
                valor['menorAncho'] = banda
                valor['cable'] = cable
                valor['distancia'] = distancia


def crearLandingCapital(analyzer):

    """
    Para cada pais en el mapa countrys, conecta la capital del pais con los 
    landing points dentro del pais.
    """

    paises = analyzer['countrys']
    landingPoints = analyzer['landing_points']

    lista = mp.keySet(paises)
    
    iterador = lt.iterator(lista)

    tam = lt.size(lista)
    con  = 0

    try:
        while con < tam:
           a = next(iterador)
           entry = mp.get(paises,a)
           valor = me.getValue(entry)
 
           capital = valor['capital']
           lpsPais = valor['lista'] 

           lpCapital = newLandingPoint(capital,None,a)
           mp.put(landingPoints,capital,lpCapital)

           tamLista = lt.size(lpsPais)
           con2 = 0

           while con2 < tamLista:
            
               n = lt.getElement(lpsPais,con2)

               entry2 = mp.get(landingPoints,n)
               valor2 = me.getValue(entry2)

               menorDistancia = valor2['distancia']
               listaLps = valor2['lista']
               tam3 = lt.size(listaLps)
               con3 = 0

               while con3 < tam3:
                    i = lt.getElement(listaLps,con3) 
                    addConnection(analyzer,capital,i, menorDistancia)
                    con3 += 1
               con2 += 1
        con += 1
 
    except StopIteration:
        print("Finalizó.")
        

def crearLandingPoints(analyzer, landing_point):
    """
    Crea el landing point dado por parametro, y lo añade a la lista de 
    Landing Points
    """
    
    mapa = analyzer['landing_points']
    mapaNames = analyzer['landing_points_name']

    id = landing_point['landing_point_id']
    name  = landing_point['name']

    corte = name.split(",")
    tamaño = len(corte)

    paisLp = corte[tamaño-1].strip()

    modif = corte[0].lower()
    modif1 = modif.strip()
    
    pais = corte[len(corte)-1]
    paisM = pais.strip()

    elemento  = newLandingPoint(id,landing_point,paisLp)
    elementoName  = newLandingPointName(modif1,id,paisM)

    mp.put(mapaNames,modif1,elementoName)
    mp.put(mapa,id,elemento)
    añadirLpPais(analyzer,landing_point,id)
    

def añadirLpPais(analyzer,landing_point,id):

    """
    Añade cada landingPoint al pais al que pertenece, dentro del mapa de countrys
    """
    
    paises = analyzer['countrys']
    pais = landing_point['name']
    corte = pais.split(",")
    tamaño = len(corte)

    paisLp = corte[tamaño-1].strip()
    
    entry = mp.get(paises, paisLp)
    valor = me.getValue(entry)
    lista = valor['lista']
    lt.addLast(lista, id)
    
    

def addVertice(analyzer, vertice):
    
    grafo = analyzer['connections']
    try:

        gr.insertVertex(grafo, vertice)
    except Exception as exp:
        error.reraise(exp, 'model:addVertice')


def addCountry(analyzer, country):
    
    paises = analyzer['countrys']
    key = country['CountryName']
    capital = country['CapitalName']
    
    pais = newCountry(key, country,capital)
    mp.put(paises,key,pais)

    addVertice(analyzer,capital)

def newCountry(name,elemento,capital):
    """
    Define la estructura de un pais 
    """
    country = { 'name' : name,'elemento': elemento,'capital':capital, 'lista': None}
    country['lista'] = lt.newList('ARRAY_LIST')
    return country

def newLandingPoint(id,lp,pais):

    """
    Define la estructura de un landing point con id como key
    """

    lp = {'landing_point': id,'landing_pt': lp, 'pais': pais,'menorAncho': None, 'cable': None,
    'distancia': None, 'lista': None}
    lp['lista'] = lt.newList('ARRAY_LIST')
    return lp 

def newLandingPointName(name,id,pais):
    """
    Define la estructura de un landing point con name como key
    """
    lp = {'landing_point': name,'id': id, 'pais':pais}
    return lp 

    
# Funciones de consulta

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju 
    """
    analyzer['componentes'] = scc.KosarajuSCC(analyzer['connections'])

def numConnectedComponents(analyzer):
    """
    Retorna el numero de componentes conectados
    """
    return scc.connectedComponents(analyzer['componentes'])

def pertenecenCluster(analyzer,lp1,lp2):
    """
    REQ. 1
    Retorna True si los 2 vertices en parametro estan fuertemente conectados. 
    """
    lpsName = analyzer['landing_points_name']
    lps = analyzer['landing_points']
    kossc = analyzer['componentes']

    par1 = lp1.lower()
    par11 = par1.strip()

    par2 = lp2.lower()
    par22 = par2.strip()

    lpo1 = mp.get(lpsName,par11)
    lpo2 = mp.get(lpsName,par22)

    if lpo1 == None or lpo2 == None:
        print('Uno de los landing points no existe en el mapa landing_points_name.')
    else:
        val1 = me.getValue(lpo1)
        val2 = me.getValue(lpo2)
        id1 = val1['id']
        id2 = val2['id']

        landP1 = mp.get(lps,id1)
        valP1 = me.getValue(landP1)
        listaLandP1 = valP1['lista']

        landP2 = mp.get(lps,id2)
        valP2 = me.getValue(landP2)
        listaLandP2 = valP2['lista']

        tam = lt.size(listaLandP1)
        con = 0

        terminado = False
        
        while con < tam and not terminado:
            vert1 = lt.getElement(listaLandP1,con)
          
            tam1 = lt.size(listaLandP2)
            con1 = 0

            while con1 < tam1 and not terminado:
                    
                vert2 = lt.getElement(listaLandP2,con1)
          
                if scc.stronglyConnected(kossc,vert1,vert2):
                    terminado = True
                   
                con1 += 1

            con += 1

    return terminado

def conexionesLps(analyzer):
    """
    REQ 2. 
    Retorna una lista con todos los landing points que tengan 2 o mas conexiones. 
    """
    lpsName = analyzer['landing_points_name']
    lps = analyzer['landing_points']
    lista = mp.keySet(lpsName)
    iterador = lt.iterator(lista)

    tam = lt.size(lista)
    con  = 0
    try: 
        while con< tam:
            a = next(iterador)
            lp = mp.get(lpsName,a)
            val = me.getValue(lp)
            pais = val['pais']
            id = val['id']
            name = val['landing_point']

            lp1 = mp.get(lps,id)
            val1 = me.getValue(lp1)
            lista = val1['lista']
            num = lt.size(lista)

            if(num >= 2):
                print("Landing point: " + name + " - " + pais + " - " + id + 
                "\nTotal de Conexiones: " + str(num) )
                print()

            con += 1

    except StopIteration:
        print("Finalizó.")


def getRutaMenorDist(analyzer, paisA, paisB):
    """
    REQ. 3

    Retorna la ruta (incluir la distancia de conexión [km]
    entre cada par consecutivo de landing points) y la
    distancia total de la ruta.
    """
    paises = analyzer['countrys']
    grafo = analyzer['connections']

    pais1 = mp.get(paises,paisA)
    pais2 = mp.get(paises,paisB)
    lista = lt.newList('ARRAY_LIST')
    distanciaTotal = 0
    if (pais1 == None or pais2 == None):
        print("Uno de los paises no existe.")
    else:
        val1 = me.getValue(pais1)
        val2 = me.getValue(pais2)
        capital1 = val1['capital']
        capital2 = val2['capital']
        estruc = dj.Dijkstra(grafo,capital1)
        distanciaTotal = dj.distTo(estruc,capital2)

        camino = dj.pathTo(estruc,capital2)
        tam = lt.size(camino)
        con  = 0
        iterador = lt.iterator(camino)

        try:
            while con < tam:
                a = next(iterador)
                peso =  a['weight']
                vertice1 = a['vertexA'] 
                vertice2 = a['vertexB']

                union = {'peso': peso,'vertice1': vertice1, 'vertice2': vertice2}
                lt.addLast(lista,union)
                con += 1
        except StopIteration:
            print("Finalizó.")
        
    return lista, distanciaTotal
       
def redExpansion(analyzer):
    """
    REQ. 4
    Retorna el numero de nodos conectados a la red de expansion minima,
    el total del costo de la red y la rama mas larga de la red.
    """
    grafo = analyzer['connections']
    estruc = prim.PrimMST(grafo)
    pesoTotal = prim.weightMST(grafo,estruc)
    vertices = estruc['marked']
    numVertices = mp.size(vertices)
    distancias = estruc['distTo']
    keys = mp.keySet(distancias)
    iterador = lt.iterator(keys)

    con = 0
    tam = lt.size(keys)

    distanciaMayor = 0
    ramaMayor = None
    try:
        while con < tam:
            a = next(iterador)
            elemento = mp.get(distancias,a)
            valor = me.getValue(elemento)
            if(valor > distanciaMayor):
                distanciaMayor = valor
                ramaMayor = a
    except StopIteration:
        print("Finalizó.")

    return pesoTotal,numVertices,distanciaMayor,ramaMayor

def getFallas(analyzer,lapo):
    """
    REQ 5.
    Retorna el numero de paises afectados, y una lista de paises afectados
    ordenada descendentemente con la distancia al lp dado en parametro.
    """

    sf = lapo.lower()
    lp = sf.strip()

    lps = analyzer['landing_points']
    lpsName = analyzer['landing_points_name']
    grafo = analyzer['connections']
    elemento = mp.get(lpsName,lp)

    paises = lt.newList('ARRAY_LIST')
    

    if elemento == None:
        print("El landing point no existe.")
    else:
        valor = me.getValue(elemento)
        id = valor['id']

        entry = mp.get(lps,id)
        val = me.getValue(entry)
        lis = val['lista']
        lista = lis['elements']
        for n in lista:
            adya = gr.adjacents(grafo,n)
            
            iterador  = lt.iterator(adya)
            con = 0
            tam = lt.size(adya)
            try: 
                while con < tam: 
                    a = next(iterador)
                    lp = extraerLp(a)
                    entry = mp.get(lps,lp)
                    valor = me.getValue(entry)
                    pais = valor['pais']

                    if(not lt.isPresent(paises,pais)):
                        lt.addLast(paises, pais)
                    con += 1

            except StopIteration:
                print("Finalizó.")
    numPaises = lt.size(paises)

    return numPaises, paises





def medirDistanciaMinima(grafo, vertice1, vertice2):
    """
    Mide el costo que existe entre el vertice 1 y el vertice 2.
    """
    estruc = dj.Dijkstra(grafo,vertice1)
    distanciaTotal = dj.distTo(estruc,vertice2)
    return distanciaTotal
    
def getCantidadClusteres(analyzer):
    """
    Retorna la cantidad de componentes conectados.
    """
    scco = analyzer['componentes']
    rta = scc.connectedComponents(scco)
    return rta

def estanConectados(grafo,forigen,fdestino):

    """
    Revisa si existe conexion entre dos Landing Points

    Returns: True si estan conectados, false de lo contrario.
    """

    esta = gr.getEdge(grafo,forigen,fdestino)
    if esta is None:
        rta = False
    else:
        rta = True
    return rta

def darCapital(pais):

    """
    Retorna la capital de un pais.
    """
    lista = pais.split(',')
    capital = lista[0].strip().lower()
    return capital


def formatVertex(lpoint,cable):
    """
    Formatea la estructura del vertice = landing point + cable
    """
    
    name = lpoint + '-' + cable
    return name 

def extraerLp(vertice):
    """
    Extrae el landing point del vertice dado por parametro.
    """
    corte = vertice.split("-")
    lp = corte[0]
    return lp

def numeroPaises(analyzer):

    """
    Retorna el numero de paises unicos
    """
    cont = mp.size(analyzer['countrys'])
    return cont


def numeroPoints(analyzer):
    """
    Retorna el numero de landing points
    """

    cont = mp.size(analyzer['landing_points'])
    return cont

def totalConexiones(analyzer):
    """
    Retorna el numero de arcos entre landing points
    """
    cont = gr.numEdges(analyzer['connections'])
    return cont 


# Funciones utilizadas para comparar elementos dentro de una lista

def compareIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


