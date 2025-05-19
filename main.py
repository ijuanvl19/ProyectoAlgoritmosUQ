import scrapping.scrapping as sc
from cleaning import clean_data as cd
import os
import threading as th
import graficates.graficate as gr
import data_model.categoreis_lists as cl


# Crear hilos para descargar los datos de diferentes fuentes a la vez
# thread_1 = th.Thread(target=sc.donwloadDataIEE)
# thread_2 = th.Thread(target=sc.download_sage_articles)
# thread_3 = th.Thread(target=sc.download_sciense_articles)

# thread_1.start()
# thread_2.start()
# thread_3.start()

# thread_1.join()
# thread_2.join()
# thread_3.join()

# # Esperar a que todos los hilos terminen
# thread_1.join()
# thread_2.join()
# thread_3.join()


# Especifica la carpeta que contiene los archivos .bib
folders = ['IEEE', 'sage', 'sciense']

output_folder = 'assets/temps/'

for folder in folders:
    # Obtener la ruta de la carpeta actual
    routs = [os.path.normpath(r).replace('\\', '/') for r in cd.obtener_archivos_bib('assets/' + folder)]
    # Crear la ruta completa para el archivo de salida
    output_filepath = os.path.join(output_folder, f'{folder}Consolidated.bib')
    # Combinar los archivos .bib y guardar en la ruta especificada
    cd.combinar_bibtex_sin_repetidos_por_titulo(routs, output_filepath)
    print(f"Archivo combinado sin repetidos guardado en: {output_filepath}")

print("Archivos combinados y guardados correctamente.")

# generar un archivo bibtex consolidado sin repetidos por título general de los archivos .bib temporales
input_folder = 'assets/temps/'
output_filepath = os.path.join(input_folder, 'Consolidated.bib')

# Combinar los archivos .bib y guardar en la ruta especificada
cd.combinar_bibtex_sin_repetidos_por_titulo(cd.obtener_archivos_bib(input_folder), output_filepath)
print(f"Archivo combinado sin repetidos guardado en: {output_filepath}")
# -------------------------------------------------------------------------------------------------------
# hasta aqui el codigo de la parte de scrapping y limpieza de los archivos bibtex
# -------------------------------------------------------------------------------------------------------


# Graficar los datos de las bases de datos
# input_file = 'assets/temps/Consolidated.bib'

# data = cd.leer_bibtex_con_mmap_regex(input_file)

# graficas consideradas core en el documento de requerimiento
# top 15 autores
''' esta funcion grafica los 15 autores con mayor cantidad de documentos mostrando el nombre y la cantidad de documentos en los que han participado'''
# gr.graficate_authors(data)

# Graficar los datos de los años
''' esta funcion grafica la cantidad de documentos por año en una linea de tiempo'''
# gr.graficate_year(data)

# graficar los diferetnes tipos de documentos por año
''' esta funcion grafica la cantidad de documentos por año y por tipo de documento(articulo, libro, etc)'''
# gr.graficar_por_anio_y_tipo(data)

# Graficar los datos de los tipos de documentos
''' esta funcion grafica la cantidad de documentos por tipo de documento(articulo, libro, etc)'''
# gr.graficate_entertype(data)

# graficar los 15 journals con mayor cantidad de documentos
''' esta funcion grafica los 15 journals con mayor cantidad de documentos mostrando el nombre y la cantidad de documentos en los que han participado'''
# gr.graficate_journals(data)

# graficar las 15 revistas con mayor cantidad de documentos
''' esta funcion grafica los 15 revistas con mayor cantidad de documentos mostrando el nombre y la cantidad de documentos en los que han participado'''
# gr.graficate_publisher(data)
# --------------------------------------------------------------------------------------------------------
# hasta aqui las graficas core
# --------------------------------------------------------------------------------------------------------
# graficas adicionales que consideramos relevantes
# Llamar a la función para graficar las bases de datos
''' esta funcion grafica la cantidad de documentos por base de datos'''
# gr.graficate_databases(data)

# graficar los diferentes tipos de documentos por base de datos
''' esta funcion grafica la cantidad de documentos por base de datos y por tipo de documento(articulo, libro, etc)'''
# gr.graficate_type_database(data)

# graficar los diferentes tipos de documentos por año
''' esta funcion grafica la cantidad de documentos por año y por tipo de documento(articulo, libro, etc) mostrando un mapa de calor'''
# gr.heatmap_tipo_vs_anio(data)
# ----------------------------------------------------------------------------------------------------------
# hasta aqui las graficas adicionales
# ----------------------------------------------------------------------------------------------------------

# crear tabla de contenido de las categorias
# gr.generate_table_words(data)

# graficar nubes de palabras y tablas de frecuencia para cada categoria
''' esta funcion grafica una nube de palabras y una tabla de frecuencia para cada categoria asi como una tabla de contenido general'''
# gr.generate_table_words(data)

