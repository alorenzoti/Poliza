# coding=utf-8


"""
Intentando.py

Probando a hacer cosas con arcpy

"""

"""

Notas de desarrollo:

Tareas
- Revisa que no queden to-dos por ahi repartidos
- Falta input cultivo
- HECHO Validar que los archivos existon con os.path.exists

PYTHON 2vs3
- comprobar que las rutas y cadenas funcionan en python 2 y 3
- look raw_input por input

REFACTORING 
- Revisar los nombres de variables y rutas para ser mas evidentes
- Cambiar las rutas para ser mas consistentes
- Como simplificar las rutas: convention over configuration
- reajustar los nombres de las configs en lo que son gdb y lo que son capas
- separar todo lo que sea arcpy a core.

FEATURE REQUESTS
- pensar en sacar lo que sea "interactivo" aparte para facilitar la integracion con arcgis
- utilizar espacios de trabajo temporales https://pro.arcgis.com/es/pro-app/latest/arcpy/geoprocessing_and_python/using-environment-settings.htm

"""

####################################################gst############################
# CORE
from poliza_utils import limpiar_workspace, comprobar_rutas
from core import pedir_mes, entrada_periodo_usuario
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
    recoge_meteo_periodo(ruta_gdb_temporal, inicio, final)

    # extrae de las tablas de att los atributos de capa de el catastro selecionado
    entidadRecorte = obtener_catastro(obtener_parcela_usuario(), ruta_catastro_capa, ruta_gdb_temporal)

    # REALIZAMOS EL CLIP DE CATASTRO CON LOS DATOS CLIMATICOS:
    lista_capas_gdb = lista_capas(ruta_gdb_temporal)
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
    lista_recorte = lista_capas(ruta_gdb_temporal)
    # Y guardamos las capas selecionadas para el periodo dado en ella
    guardar_periodo(destino_dir, destino_dbname, destino_workspace,
                    lista_recorte, ruta_gdb_temporal)

    calcular_indice_peligro_parcela(destino_tablas_ruta)
    obtener_precio_seguro(indice_peligro_parcela)
