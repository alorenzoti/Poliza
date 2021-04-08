
import arcpy
import os

ruta_precipitaciones = r"C:\script\climatologia\precipitaciones.gdb"
arcpy.env.workspace = ruta_precipitaciones
mes = "febrero"
debug = True

if debug:
    print("estoy copiando precipitaciones {mes} ".format(mes=mes))
    print("en el wkspc {0}".format(arcpy.env.workspace))
arcpy.management.CopyRaster( mes, os.path.join( mes + "Pre"))