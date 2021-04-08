# coding=utf-8
import arcpy
import os
import pandas as pd
from arcpy.management import CopyRaster
from arcpy.sa import ExtractByMask
from arcpy.sa import *
import shutil

# Configuraciones internas
arcpy.env.overwriteOutput = True
debug = True

"""
Intentando.py

Probando a hacer cosas con arcpy

"""

"""

Notas de desarrollo:
- Falta input cultivo
- Cambiar las rutas para ser mas consistentes
- Revisar los nombres de variables y rutas

"""

################################################################################
#
# CONFIG
#
################################################################################

# Absolute Workspace
# Where you store all the stuff for this project
root_path = r"C:\script\\"
# Config de Destino
destino_dir = r"C:\script\workspace"
destino_dbname = "datos_finales.gdb"
destino_workspace = r"C:\script\workspace\datos_finales.gdb"
destino_tablas_ruta = r"C:\script\workspace\tablas"

# Rutas:
ruta_catastro = r"C:\script\catastro\catastrogdb.gdb"
ruta_catastro_capa = r"C:\script\catastro\catastrogdb.gdb\Catastro_murcia"
ruta_precipitaciones = r"C:\script\climatologia\precipitaciones.gdb"
ruta_temperaturasMax = r"C:\script\climatologia\temperaturasMax.gdb"
ruta_temperaturasMin = r"C:\script\climatologia\temperaturasMin.gdb"
ruta_geologia = r"C:\script\datosConstantes\Geologia.gdb"
ruta_geologia_capa = r"C:\script\datosConstantes\Geologia.gdb\litologia"
ruta_hidrologia = r"C:\script\datosConstantes\Hidrologia.gdb"
ruta_hidrologia_capa = r"C:\script\datosConstantes\Hidrologia.gdb\aguaRaster"
ruta_pendiente = r"C:\script\datosConstantes\pendiente.gdb"
ruta_pendiente_capa = r"C:\script\datosConstantes\pendiente.gdb\pendiente"

#  Ruta de gdb de trabajo (Temporal)
ruta_geodb_trabajo = r"C:\script\workspace\datosInput.gdb"

################################################################################
#
# CORE
#
################################################################################





def limpiar_workspace(workspace):
    if os.path.isdir(workspace):
        shutil.rmtree(workspace)
    os.makedirs(os.path.join(workspace, r"tablas"))



listameses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
              'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

def pedir_mes(msg):
    valid = False
    while not valid:
        mes = raw_input(msg)
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


def recoge_meteo(ruta_geodb_trabajo, mesEntrada, mesSalida):
    """
    recoge precipitaciones y temperaturas en un periodo dado y las copia a nuestra gdb para cada mes.
    """
    periodo = getperiod(mesEntrada, mesSalida)
    # TODO: workspace
    if debug:
        print("te vamos a copiar estos datos: {0}".format(periodo))
    for mes in periodo:
        arcpy.env.workspace = ruta_precipitaciones
        if debug:
            print("estoy copiando precipitaciones {mes} ".format(mes=mes))
            print("en el wkspc {0}".format(arcpy.env.workspace)
        arcpy.management.CopyRaster( mes, os.path.join( mes + "Pre"))

        if debug:
            print("estoy copiando temperaturas maximas {mes} ".format(mes=mes))
        arcpy.env.workspace = ruta_temperaturasMax
        arcpy.management.CopyRaster(
            mes, os.path.join(ruta_geodb_trabajo, mes + "TMax"))

        if debug:
            print("estoy copiando temperaturas minimas {mes} ".format(mes=mes))
        arcpy.env.workspace = ruta_temperaturasMin
        arcpy.management.CopyRaster(
            mes, os.path.join(ruta_geodb_trabajo, mes + "TMin"))



# ask users INPUT CATASTRO + SELECT:
# TODO: extract inputs and add validation. eg: "560014A40027"
def obtener_parcela_usuario():
    input_catastro = raw_input("introduce el numero de parcela catastral \t")
    return str(input_catastro)


def obtener_parcela_arcpy():
    return arcpy.GetParameterAsText(2)



def recortar(entidadRecorte, lista_capas_gdb, save_path):
    """ Recorta capas en funcion de la entidad de recorte.
    lista_capas_gdb: lista de capas a cortar
    save_path: donde guardar la vaina
    """
    inRaster = capa
    inMaskData = entidadRecorte
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(os.path.join(ruta_geodb_trabajo, save_path))
    if debug:
        print("estoy recortando {0}".format(capa))
        print("estoy guardando en {0}".format(save_path))


def recortar_clima(entidadRecorte, lista_capas_gdb):
    for capa in lista_capas_gdb:
        recortar(entidadRecorte, capa, capa + "_recorte")


def guardar_periodo(destino_dir,
                    destino_dbname, destino_workspace,
                    lista_recorte, ruta_geodb_trabajo):
    """
    Guarda el resultado del periodo selecionado
    """
    # Creamos una GDB nueva para el resultado
    arcpy.CreateFileGDB_management(destino_dir, destino_dbname)
    arcpy.env.workspace = destino_workspace

    for capa in lista_recorte:
        if "_recorte" in capa:
            arcpy.env.workspace = ruta_geodb_trabajo
            if debug:
                print("{capa}+esta capa es resultado".format(capa=capa))
            arcpy.management.CopyRaster(capa, os.path.join(
                destino_workspace, capa + '_def'))




def guardar_periodo(destino_dir,
                    destino_dbname, destino_workspace,
                    lista_recorte, ruta_geodb_trabajo):
    """ Guarda el resultado del periodo selecionado
    """
    # Creamos una GDB nueva para el resultado
    arcpy.CreateFileGDB_management(destino_dir, destino_dbname)
    arcpy.env.workspace = destino_workspace

    for capa in lista_recorte:
        if "_recorte" in capa:
            arcpy.env.workspace = ruta_geodb_trabajo
            if debug:
                print("{capa}+esta capa es resultado".format(capa=capa))
            arcpy.management.CopyRaster(capa, os.path.join(
                destino_workspace, capa + '_def'))


def guardar_periodo(destino_dir,
                    destino_dbname, destino_workspace,
                    lista_recorte, ruta_geodb_trabajo):
    """ Guarda el resultado del periodo selecionado
    """
    # Creamos una GDB nueva para el resultado
    arcpy.CreateFileGDB_management(destino_dir, destino_dbname)
    arcpy.env.workspace = destino_workspace

    for capa in lista_recorte:
        if "_recorte" in capa:
            arcpy.env.workspace = ruta_geodb_trabajo
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



################################################################################
#
# MAIN
#
################################################################################
if __name__ == "__main__":

    print("empieza el script")
    limpiar_workspace(destino_dir)
    inicio, final = entrada_periodo_usuario()  # pide entrada al usuario
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