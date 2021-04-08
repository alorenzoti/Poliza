#!env/bin/python
# coding=utf-8
import arcpy
import os
import pandas as pd
from arcpy.management import CopyRaster
from arcpy.sa import ExtractByMask
from arcpy.sa import *
import shutil

from core import pedir_mes, entrada_periodo_usuario, entrada_arcpy, getperiod
from config import *

# Configuraciones internas
arcpy.env.overwriteOutput = True
debug = True


# Inputs:
# TODO: Falta input cultivo
# Imagino que en las rutas???


################################################################################
#
#
#
################################################################################

if __name__ == "__main__":

    print("empieza el script")
    limpiar_workspace()
    inicio, final = pedirentrada()  # pide entrada al usuario
    recoge_meteo(ruta_geodb_trabajo, inicio, final)

    # extrae de las tablas de att los atributos de capa de el catastro selecionado
    entidadRecorte = arcpy.Select_analysis(
        ruta_catastro_capa, ruta_geodb_trabajo, "OBJECTID" + "=" + obtener_parcela_usuario)

    # REALIZAMOS EL CLIP DE CATASTRO CON LOS DATOS CLIMATICOS:
    arcpy.env.workspace = ruta_geodb_trabajo
    lista_capas_gdb = arcpy.ListDatasets("*", "Raster")

    recortar_clima(entidadRecorte, lista_capas_gdb)
    # RECORTE DATOS CONSTANTES:

    # RECORTAMOS LA CAPA DE GEOLOGIA
    recortar(entidadRecorte, ruta_geologia_capa, r"geologia_recorte")
    # RECORTAMOS CAPA DE PENDIENTE:
    recortar(entidadRecorte, pendiente_capa, r"pendiente_recorte")
    # RECORTAMOS CAPA DE HIDROLOGÍA:
    recortar(entidadRecorte, hidrologia_capa, r"hidrologia_recorte")

    # CREAMOS UNA NUEVA GDB SOLO para LAS CAPAS DE RECORTE
    lista_recorte = arcpy.ListDatasets("*", "Raster")
    # Y guardamos las capas selecionadas para el periodo dado en ella
    guardar_periodo(destino_dir, destino_dbname, destino_workspace,
                    lista_recorte, ruta_geodb_trabajo)

    calcular_indice_peligro_parcela(destino_tablas_ruta)
    obtener_precio_seguro(indice_peligro_parcela)