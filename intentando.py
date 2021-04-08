import arcpy
import os
import pandas as pd
from arcpy.management import CopyRaster
from arcpy.sa import ExtractByMask
from arcpy.sa import *
import shutil


arcpy.env.overwriteOutput = True
debug = True

# Comprobamos si existe la carpeta workspace
existe = os.path.isdir(r"C:\script\workspace")
if existe == True:
    a = (r"C:\script\workspace")
    shutil.rmtree(a)
    os.makedirs(r"C:\script\workspace\tablas")
else:
    os.makedirs(r"C:\script\workspace\tablas")

print("empieza el script")

# Creamos gdb de uso:
pruebaGDB = arcpy.CreateFileGDB_management(
    r"C:\script\workspace", "datosInput.gdb")


# Inputs:
# Falta input cultivo
################################################################################
# CONFIG
################################################################################

# Absolute Workspace
# Where you store all the stuff for this project
root_path = r"C:\script\"
# Config de Destino
destino_dir = r"C:\script\workspace"
destino_dbname = "datos_finales.gdb"
destino_workspace = r"C:\script\workspace\datos_finales.gdb"
destino_tablas_ruta = r"C:\script\workspace\tablas"

# Rutas:
catastro = r"C:\script\catastro\catastrogdb.gdb"
catastro_capa = r"C:\script\catastro\catastrogdb.gdb\Catastro_murcia"
precipitaciones = r"C:\script\climatologia\precipitaciones.gdb"
temperaturasMax = r"C:\script\climatologia\temperaturasMax.gdb"
temperaturasMin = r"C:\script\climatologia\temperaturasMin.gdb"
geologia = r"C:\script\datosConstantes\Geologia.gdb"
geologia_capa = r"C:\script\datosConstantes\Geologia.gdb\litologia"
hidrologia = r"C:\script\datosConstantes\Hidrologia.gdb"
hidrologia_capa = r"C:\script\datosConstantes\Hidrologia.gdb\aguaRaster"
pendiente = r"C:\script\datosConstantes\pendiente.gdb"
pendiente_capa = r"C:\script\datosConstantes\pendiente.gdb\pendiente"

# Espacio de trabajo precipitaciones
espacioTrabajo = arcpy.env.workspace = r"C:\script\climatologia\precipitaciones.gdb"

################################################################################
# Realizacion de meses procedentes de input:
# Datos Raster:
# Creamos una lista para iterar las precipitaciones:
listaPrecipitaciones = arcpy.ListDatasets("*", "Raster")
print(listaPrecipitaciones)

listameses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
              'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


def pedirentrada():
    mesEntrada = input("introduce un mes de inicio de poliza \t")
    #mesEntrada = arcpy.GetParameterAsText(0)
    mesSalida = input('introduce un mes de fin de poliza \t')
    #mesSalida = arcpy.GetParameterAsText(1)
    return (mesEntrada, mesSalida)


def getperiod(inicio, final):
    """dado inicio y final saca los meses de entre medias"""
    a = listameses.index(inicio)
    b = listameses.index(final)
    return listameses[a:b+1]


assert len(getperiod("enero", "febrero")) == 2


def recorrer(mesEntrada, mesSalida):
    """recorre el periodo y devuelve y copio los datos en la ruta"""
    periodo = getperiod(mesEntrada, mesSalida)
   # print(f"te vamos a copiar estos datos: {periodo}")
    for mes in periodo:
        #print(f"estoy copiando precipitaciones {mes} ")
        arcpy.management.CopyRaster(
            mes, os.path.join(geodb_periodo_path, mes + "Pre"))

       # print(f"estoy copiando temperaturas maximas {mes} ")
        arcpy.env.workspace = r"C:\script\climatologia\temperaturasMax.gdb"
        arcpy.management.CopyRaster(
            mes, os.path.join(geodb_periodo_path, mes + "TMax"))

      #  print(f"estoy copiando temperaturas minimas {mes} ")
        arcpy.env.workspace = r"C:\script\climatologia\temperaturasMin.gdb"
        arcpy.management.CopyRaster(
            mes, os.path.join(geodb_periodo_path, mes + "TMin"))


################################################################################
#
#
#
################################################################################


inicio, final = pedirentrada()  # pide entrada al usuario
recorrer(inicio, final)

# ask users INPUT CATASTRO + SELECT:
# TODO: extract inputs and add validation. eg: "560014A40027"
input_catastro = input("introduce el numero de parcela catastral \t")

"""
The input is to be replaced by arcpy parameters:

    input_catastro = arcpy.GetParameterAsText(2)


"""


geodb_periodo_path = r"C:\script\workspace\datosInput.gdb"

# extrae de las tablas de att los atributos de capa de el catastro selecionado
entidadRecorte = arcpy.Select_analysis(
    catastro_capa, geodb_periodo_path, "OBJECTID" + "=" + str(input_catastro))
#entidadRecorte = arcpy.Select_analysis(catastro_capa,geodb_periodo_path,campo + "= '" + str(numero) + "'")


# REALIZAMOS EL CLIP DE CATASTRO CON LOS DATOS CLIMATICOS:
arcpy.env.workspace = geodb_periodo_path
lista_capas_gdb = arcpy.ListDatasets("*", "Raster")
# print(lista_capas_gdb)


def recortar(lista_capas_gdb, save_path):
    """ Recorta capas en funcion de la entidad de recorte.
    lista_capas_gdb: lista de capas a cortar
    save_path: donde guardar la vaina
    """
    inRaster = capa
    inMaskData = entidadRecorte
    outExtractByMask = ExtractByMask(inRaster, inMaskData)
    outExtractByMask.save(os.path.join(geodb_periodo_path, save_path))
    if debug:
        print(f"estoy recortando {capa}")
        print(f"estoy guardando en  {save_path}")


def recortar_clima(lista_capas_gdb):
    for capa in lista_capas_gdb:
        recortar(capa, capa + "_recorte")


recortar_clima(lista_capas_gdb)
# RECORTE DATOS CONSTANTES:

# RECORTAMOS LA CAPA DE GEOLOGIA
recortar(geologia_capa, r"geologia_recorte")

# RECORTAMOS CAPA DE PENDIENTE:
recortar(pendiente_capa, r"pendiente_recorte")

# RECORTAMOS CAPA DE HIDROLOGÍA:
recortar(hidrologia_capa, r"hidrologia_recorte")

# CREAMOS UNA NUEVA GDB SOLO CON LAS CAPAS DE RECORTE
lista_recorte = arcpy.ListDatasets("*", "Raster")

if debug:
    print(lista_recorte)


def guardar_periodo(destino_dir,
                    destino_dbname, destino_workspace,
                    lista_recorte, geodb_periodo_path):
    """ Guarda el resultado del periodo selecionado
    """
    # Creamos una GDB nueva para el resultado
    arcpy.CreateFileGDB_management(destino_dir, destino_dbname)
    arcpy.env.workspace = destino_workspace

    for capa in lista_recorte:
        if "_recorte" in capa:
            arcpy.env.workspace = geodb_periodo_path
            if debug:
                print(f"{capa}+esta capa es resultado")
            arcpy.management.CopyRaster(capa, os.path.join(
                destino_workspace, capa + "_def"))


guardar_periodo(destino_dir, destino_dbname, destino_workspace,
                lista_recorte, geodb_periodo_path)

# TRANSFORMAMOS LOS DATOS A CSV:


def transformar_csv(destino_workspace, destino_tablas_ruta):
    """
    Transforma a csv y guarda cada tabla en el workspace
    """
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = destino_workspace
    lista = arcpy.ListRasters("*", "ALL")

    for elemento in lista:
        if arcpy.Exists(os.path.join(destino_tablas_ruta, elemento+".csv")):
            arcpy.Delete_management(os.path.join(
                destino_tablas_ruta, elemento+".csv"))
        arcpy.conversion.TableToTable(
            elemento, destino_tablas_ruta, elemento+".csv")
        if debug:
            print(elemento)


transformar_csv(destino_workspace, destino_tablas_ruta)

# PANDAS
# 1. LISTO LAS TABLAS:
arcpy.env.workspace = destino_tablas_ruta
tablas_peligrosidad = arcpy.ListFiles("*.csv")
if debug:
    print("tablas_peligrosidad")
    print(tablas_peligrosidad)


# Calculo la media de las columnas Value de los CSVs:

def obtener_medias_peligro(destino_tablas_ruta, tablas_peligrosidad):
    """Se obtiene la media de los distintos mapas de peligrosidad
    """
    lista_media = []

    for me in tablas_peligrosidad:
        leercsv = pd.read_csv(os.path.join(destino_tablas_ruta, me), sep=";", header=0)
        media = leercsv['Value'].mean()
        lista_media.append(media)
    if debug:
        print("A continuacion viene la lista de la media de la columna value de los CSVs")
        print(lista_media)
    return lista_media


# MULTIPLICO LOS NÚMERO DE LAS LISTAS [a*b*c]

def obtener_total(medias_peligrosidad):
    """
    Se obtiene el valor (unico) de la peligrosidad por parcela.
    """
    total = 1
    for i in medias_peligrosidad:
        total = total+i
        (total)
    dividendo = print("dividendo " + str(total))
    divisor = print("divisor " + str(longitudlista))
    return total


# Numero final de multiplicación entre numero de capas:
medias_peligrosidad = obtener_medias_peligro(destino_tablas_ruta, tablas_peligrosidad)
longitudlista = len(medias_peligrosidad)
total_peligro = obtener_total(medias_peligrosidad)
indice_peligro_parcela = total_peligro/longitudlista
if debug:
    print(f"el indice de peligro de la puta parcela es {indice_peligro_parcela}")


# Precios seguros:

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

obtener_precio_seguro(indice_peligro_parcela)