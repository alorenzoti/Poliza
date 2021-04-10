# coding=utf-8

import arcpy #TODO: quitar la ultima llamada a esto desde este script.

"""
Intentando.py

Probando a hacer cosas con arcpy

"""

"""

Notas de desarrollo:
- Falta input cultivo
- Revisar los nombres de variables y rutas
- Validar que los archivos existon con os.path.exists
- comprobar que las rutas y cadenas funcionan en python 2 y 3
- look raw_input por input
- Cambiar las rutas para ser mas consistentes
- Como simplificar las rutas: convention over configuration

"""

################################################################################
# CORE
from core import limpiar_workspace, pedir_mes, entrada_periodo_usuario
from core import entrada_arcpy, getperiod, recoge_meteo, obtener_parcela_usuario
from core import obtener_parcela_arcpy, recortar, recortar_clima, guardar_periodo
from core import guardar_periodo, guardar_periodo, obtener_total
from core import obtener_precio_seguro, calcular_indice_peligro_parcela
################################################################################
# CONFIG
from config import *

################################################################################
#
# MAIN
#
################################################################################
if __name__ == "__main__":

    print("empieza el script")
    assert comprobar_rutas()
    limpiar_workspace(destino_dir)
    inicio, final = entrada_periodo_usuario()  # pide entrada al usuario
    recoge_meteo_periodo(ruta_geodb_trabajo, inicio, final)

    # extrae de las tablas de att los atributos de capa de el catastro selecionado
    # TODO: Aqui parece que falta el workspace!!
    entidadRecorte = obtener_catastro(ruta_db_catastro, obtener_parcela_usuario(), ruta_catastro_capa, ruta_geodb_trabajo)

    # REALIZAMOS EL CLIP DE CATASTRO CON LOS DATOS CLIMATICOS:
    lista_capas_gdb = lista_capas(ruta_geodb_trabajo)
    recortar_clima(entidadRecorte, lista_capas_gdb)
    ## RECORTE DATOS CONSTANTES:
    ## -------------------------
    # CAPA DE GEOLOGIA
    recortar(entidadRecorte, ruta_geologia_capa, r"geologia_recorte")
    # CAPA DE PENDIENTE:
    recortar(entidadRecorte, pendiente_capa, r"pendiente_recorte")
    # CAPA DE HIDROLOGÍA:
    recortar(entidadRecorte, hidrologia_capa, r"hidrologia_recorte")

    # CREAMOS UNA NUEVA GDB SOLO para LAS CAPAS DE RECORTE
    #TODO Refartoring.
    #TODO: falta el workspace. creo que va a ser el de trabajo.
    # lista_recorte = lista_capas(ruta_geodb_trabajo) # Alternativa moderna.
    lista_recorte = arcpy.ListDatasets("*", "Raster")
    # Y guardamos las capas selecionadas para el periodo dado en ella
    guardar_periodo(destino_dir, destino_dbname, destino_workspace,
                    lista_recorte, ruta_geodb_trabajo)

    calcular_indice_peligro_parcela(destino_tablas_ruta)
    obtener_precio_seguro(indice_peligro_parcela)
