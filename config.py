
################################################################################
# CONFIG
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