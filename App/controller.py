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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos

def loadData(analyzer):

    """
    Carga los datos de los archivos csv al catalogo
    """
    pais = loadCountrys(analyzer)
    vertices = loadlps(analyzer)
    loadConnections(analyzer)
#    loadConnections(analyzer)

    return vertices, pais 
    
    


def loadConnections(analyzer):
    """
    Se crea un arco entre cada par de vertices que
    pertenecen al mismo landing_point y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes cables
    servidas en un mismo landing_point.
    """

    servicesfile = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for i in input_file:
        model.newConnection(analyzer, i)
    model.crearLandingCapital(analyzer)

   ## model.crearLandingCapital(analyzer)
    


def loadlps(analyzer):
    """
    Carga los vertices del archivo.
    """

    etiquetasfile = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(etiquetasfile, encoding='utf-8'))
    cont = 0
    primerlp = None
    for lp in input_file:
        cont +=1
        model.crearLandingPoints(analyzer, lp)
        if cont == 1:
            primerlp = lp
    
    return primerlp

        

def loadCountrys(analyzer):
    
    """
    Carga los paises del archivo.
    """

    etiquetasfile = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(etiquetasfile, encoding='utf-8'))
    ultimo = None
    for country in input_file:
        model.addCountry(analyzer, country)
        ultimo = country 
    return ultimo


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def totalLandingPoints(analyzer):
    """
    Retorna el numero de paises unicos
    """
    cont = model.numeroPaises(analyzer)
    return cont

def numeroPoints(analyzer):
    """
    Retorna el numero de landing points
    """
    cont = model.numeroPoints(analyzer)
    return cont

def totalConexiones(analyzer):
    """
    Retorna el numero de arcos entre landing points
    """
    cont = model.totalConexiones(analyzer)
    return cont 

def cargarClusteres(analyzer):
    """
    Carga el el analyzer los componentes conectados.
    """
    model.connectedComponents(analyzer)

def getCantidadClusteres(catalog):
    """
    Retorna la cantidad de componentes conectados.
    """
    rta = model.getCantidadClusteres(catalog)
    return rta


def redExpansion(catalog):
    """
    Retorna el numero de nodos conectados a la red de expansion minima,
    el total del costo de la red y la rama mas larga de la red.
    """
    red = model.redExpansion(catalog)
    return red

def pertenecenCluster(catalog,lp1,lp2):
    """
    Retorna True si los 2 vertices en parametro estan fuertemente conectados. 
    """
    rta = model.pertenecenCluster(catalog,lp1,lp2)
    return rta

def conexionesLps(catalog):
    """
    Retorna una lista con todos los landing points que tengan 2 o mas conexiones. 
    """
    rta = model.conexionesLps(catalog)
    return rta

def getRutaMenorDist(analyzer, paisA, paisB):
    """
    Retorna un contenedor con la distancia de cada para de vertices, 
    y la distancia total minima. 
    """
    ruta = model.getRutaMenorDist(analyzer, paisA, paisB)
    return ruta

def getFallas(analyzer,lp):
    """
    Retorna el numero de paises afectados, y una lista de paises afectados
    ordenada descendentemente con la distancia al lp dado en parametro.
    """
    rta = model.getFallas(analyzer,lp)
    return rta
  
