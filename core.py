

import os
import pandas as pd
from arcpy.sa import ExtractByMask
from arcpy.sa import * #TODO: quitar esta puta mierda de import

from config import *
from utils import comprobar_rutas, 

# Configuraciones internas
arcpy.env.overwriteOutput = True
debug = True




listameses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
              'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

def pedir_mes(msg):
    valid = False
    while not valid:
        mes = input(msg)
        valid = mes in listameses
    return mes


def entrada_periodo_usuario():
    mesEntrada = pedir_mes("introduce un mes de inicio de poliza \t")
    mesSalida = pedir_mes('introduce un mes de fin de poliza \t')
    return (mesEntrada, mesSalida)


def entrada_arcpy():
    mesEntrada = arcpy.GetParameterAsText(0)
    mesSalida = arcpy.GetParameterAsText(1)
    return (mesEntrada, mesSalida)


def getperiod(inicio, final):
    """dado inicio y final saca los meses de entre medias"""
    a = listameses.index(inicio)
    b = listameses.index(final)
    return listameses[a:b+1]


# probando que funciona ok
assert len(getperiod("enero", "febrero")) == 2


def lista_capas(ruta_workspace):
    """
    lista todas las capas en un arcpy workspace
    """
    arcpy.env.workspace = ruta_workspace
    capas = arcpy.ListDatasets("*", "Raster")
    return capas


def recoge_meteo_periodo(ruta_gdb_temporal, mesEntrada, mesSalida, ruta_temperaturasMax=ruta_temperaturasMax,  ):
    """
    recoge precipitaciones y temperaturas en un periodo dado y las copia a nuestra gdb para cada mes.
    """
    periodo = getperiod(mesEntrada, mesSalida)
    if debug:
        print("te vamos a copiar estos datos: {0}".format(periodo))
    for mes in periodo:
        if debug:
            print("estoy copiando precipitaciones {mes} ".format(mes=mes))
        arcpy.management.CopyRaster(
            mes, os.path.join( mes + "Pre"))
        if debug:
            print("estoy copiando temperaturas maximas {mes} ".format(mes=mes))
        arcpy.env.workspace = ruta_temperaturasMax
        arcpy.management.CopyRaster(
            mes, os.path.join(ruta_gdb_temporal, mes + "TMax"))

        if debug:
            print("estoy copiando temperaturas minimas {mes} ".format(mes=mes))
        arcpy.env.workspace = ruta_temperaturasMin
        arcpy.management.CopyRaster(
            mes, os.path.join(ruta_gdb_temporal, mes + "TMin"))



# ask users INPUT CATASTRO + SELECT:
# TODO: extract inputs and add validation. eg: "560014A40027"
def obtener_parcela_usuario():
    input_catastro = input("introduce el numero de parcela catastral \t")
    return str(input_catastro)


def obtener_parcela_arcpy():
    return arcpy.GetParameterAsText(2)


def obtener_catastro(parcela, ruta_catastro_capa, ruta_gdb_temporal):
    """ Obtener la parcela de la db del catastro. imagino.
    """
    #arcpy.env.workspace=workspace # NOTE: En el original no se usa workspace para esta operacion 
    entidadRecorte = arcpy.Select_analysis(
        ruta_catastro_capa, ruta_gdb_temporal, "OBJECTID" + "=" + parcela)
    return entidadRecorte


def recortar(entidadRecorte, lista_capas_gdb, save_path):
    """ Recorta capas en funcion de la entidad de recorte.
    lista_capas_gdb: lista de capas a cortar
    save_path: donde guardar la vaina
    """
    inRaster = capa
    inMaskData = entidadRecorte
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(os.path.join(ruta_gdb_temporal, save_path))
    if debug:
        print("estoy recortando {0}".format(capa))
        print("estoy guardando en {0}".format(save_path))


def recortar_clima(entidadRecorte, lista_capas_gdb):
    for capa in lista_capas_gdb:
        recortar(entidadRecorte, capa, capa + "_recorte")



def guardar_periodo(destino_dir,
                    destino_dbname, destino_workspace,
                    lista_recorte, ruta_gdb_temporal):
    """ Guarda el resultado del periodo selecionado
    """
    # Creamos una GDB nueva para el resultado
    arcpy.CreateFileGDB_management(destino_dir, destino_dbname)
    arcpy.env.workspace = destino_workspace

    for capa in lista_recorte:
        if "_recorte" in capa:
            arcpy.env.workspace = ruta_gdb_temporal
            if debug:
                print("{capa}+esta capa es resultado".format(capa=capa))
            arcpy.management.CopyRaster(capa, os.path.join(
                destino_workspace, capa + '_def'))



def obtener_total(medias_peligrosidad):
    """
    Se obtiene el valor (unico) de la peligrosidad por parcela.
    """
    total = 1
    for i in medias_peligrosidad:
        total = total+i
    return total



def obtener_precio_seguro(indice_peligro_parcela):
    if (indice_peligro_parcela>0 and indice_peligro_parcela<50421):
        #print("la vulnerabilidad es máxima")
        maxima = arcpy.SetParameterAsText(3, "la vulnerabilidad es máxima")
        print("el seguro a todo riesgo es 3000€")
        print("el seguro a medio riesgo es 2500€")
        print("el seguro a tercero es 2000€")
    elif (indice_peligro_parcela>50421 and indice_peligro_parcela<84035):
        #print("la vulnerabilidad es media")
        media = arcpy.SetParameterAsText(4, "la vulnerabilidad es media")
        print("el seguro a todo riesgo es 2000€")
        print("el seguro a medio riesgo es 1500€")
        print("el seguro a tercero es 1000€")
    elif (indice_peligro_parcela>84035 and indice_peligro_parcela< 117649):
        #print("la vulnerabilidad es baja")
        baja = arcpy.SetParameterAsText(5, "la vulnerabilidad es baja")
        print("el seguro a todo riesgo es 1000€")
        print("el seguro a medio riesgo es 500€")
        print("el seguro a tercero es 250€")
    else:
        #print("Perdone las molestias, algo ha fallado. Volveremos a calcularlo")
        fallo = arcpy.SetParameterAsText(6, "Perdone las molestias, algo ha fallado. Volveremos a calcularlo")


def calcular_indice_peligro_parcela(destino_tablas_ruta):
    """ Calcula el ipp """
    # Transformamos los datos a csv para procesarlos con pandas
    transformar_csv(destino_workspace, destino_tablas_ruta)
    # lista las tablas de peligrosidad
    arcpy.env.workspace = destino_tablas_ruta
    tablas_peligrosidad = arcpy.ListFiles("*.csv")
    if debug:
        print("tablas_peligrosidad")
        print(tablas_peligrosidad)

    # Calculo la medias de peligrosidad
    medias_peligrosidad = obtener_medias_peligro(destino_tablas_ruta, tablas_peligrosidad)
    longitudlista = len(medias_peligrosidad)
    total_peligro = obtener_total(medias_peligrosidad)
    indice_peligro_parcela = total_peligro/longitudlista
    if debug:
        print("el indice de peligro de la puta parcela es {0}".format(indice_peligro_parcela))
    return indice_peligro_parcela
