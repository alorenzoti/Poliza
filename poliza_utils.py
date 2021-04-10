
"""
Libreria con historias que no necesitas arcpy.
Asi puedo testear estas cositas mas
"""

import os
import shutil
import config

debug = True


def ruta_existe(ruta):
    """
    Comprueba una sola ruta, pasandole el nombre de variable.
    Devuelve True si la ruta existe.
    la "ruta" de entrada es el nombre de variable de la 
    verdadera ruta. Asi que tenemos que "renderizar" la verdadera
    usando exec o algun truco similar.
    """
    rr = getattr(config, ruta)
    return os.path.exists(rr)


def obtener_rutas():
    """
    Devuelve los nombres de variable de todas las rutas
    definidas en el config.py
    """
    return list(filter(lambda x: not x.startswith("__"), dir(config)))
    


def comprobar_rutas():
    """
    Comprueba que las rutas son correctas
    """
    # para cada ruta, comprueba que existe.
    # y quedate solo con las que no existen
    # Utiliza una tupla para pasar la ruta y el bool
    for ruta in obtener_rutas():
        rutas_invalidas = []
        if not ruta_existe(ruta):
            rutas_invalidas.append()
    if len(rutas_invalidas) > 0:
        print(rutas_invalidas)
        print("Algunas rutas parecen incorrectas. por favor comprueba tu instalacion")
        raise ValueError("Path doesn't exists: {0}".format(rutas_invalidas))
    return True


def limpiar_workspace(workspace):
    if os.path.isdir(workspace):
        a = (r"C:\script\workspace")
        shutil.rmtree(a)
        os.makedirs(r"C:\script\workspace\tablas")
    else:
        os.makedirs(r"C:\script\workspace\tablas")