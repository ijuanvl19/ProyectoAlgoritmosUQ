from scrapping import ieee
from cleaning import clean_data as cd
import os

ieee.donwloadData()

##Especifica la carpeta que contiene los archivos .bib
#carpeta_bib = 'assets/IEEE/'
#
##Obtener todos los archivos .bib de la carpeta
#archivos_bib = cd.obtener_archivos_bib(carpeta_bib)
#
##Especificar la carpeta donde se guardará el archivo combinado
#carpeta_salida = 'assets/temps/'
#
##Especificar el nombre del archivo de salida
#nombre_archivo_salida = 'IEEEConsolidated.bib'
#
##Crear la ruta completa para el archivo de salida
#ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
#
##Combinar los archivos .bib y guardar en la ruta especificada
#cd.combinar_bibtex_sin_repetidos_por_titulo(archivos_bib, ruta_completa_salida)