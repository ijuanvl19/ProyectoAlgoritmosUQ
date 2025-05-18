from collections import Counter
import os
import re
import textwrap
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator
import seaborn as sb
from wordcloud import WordCloud
import data_model.categoreis_lists as cl


# this funtion will take a bibtex file and generate a graph whit  databases

def graficate_authors(data):
    """ esta funcion tomara un hasmap de datos bibtex y generara una grafica con los autores"""
    authors = {}

    for entry in data:
        if 'author' in entry and entry['author'].strip():
            # Obtener solo el primer autor y formatear
            first_author = entry['author'].split(' and ')[0].strip()
            # Formatear a 'inicial del nombre. apellido'
            parts = first_author.split()
            if parts and parts[0]:
                formatted_author = f"{parts[0][0].lower()}. {' '.join(parts[1:])}".lower(
                ) if len(parts) > 1 else parts[0].lower()
            else:
                formatted_author = "unknown"  # Valor predeterminado si no hay autor válido

            # Contar las citaciones del primer autor
            authors[formatted_author] = authors.get(formatted_author, 0) + 1

    # Ordenar los autores por el número de citaciones en orden descendente y tomar los 15 primeros
    top_authors = sorted(
        authors.items(), key=lambda x: x[1], reverse=True)[:15]

    # Verificar que top_authors no esté vacío
    if not top_authors:
        print("No hay autores con suficientes datos para graficar.")
        return

    # Desempaquetar los datos de los 15 autores más citados
    authors, count_authors = zip(*top_authors)

    # Obtener una paleta de colores distinta para cada barra
    cmap = cm.get_cmap('tab20', len(authors))
    colors = [cmap(i) for i in range(len(authors))]

    # Crear la figura y los ejes
    _, ax = plt.subplots(figsize=(12, 7))
    plt.title('Top 15 Authors by Citations')
    plt.xlabel('Count')
    plt.ylabel('Authors')

    # Crear el gráfico de barras horizontal con colores individuales
    bars = ax.barh(authors, count_authors, color=colors)

    # Añadir los valores al final de cada barra
    for bar, count in zip(bars, count_authors):
        ax.text(
            bar.get_width(),  # posición x, ligeramente a la derecha del final de la barra
            bar.get_y() + bar.get_height() / 2,  # posición y, al centro de la barra
            f'{count}',  # el texto a mostrar (conteo)
            va='center',  # alineación vertical centrada
            ha='left'  # alineación horizontal a la izquierda
        )

    # Asegurarse de que el eje x tenga solo enteros
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # Invertir el eje y para que el autor con más citaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado para que la leyenda y los textos no se corten
    plt.tight_layout()

    # Guardar la figura
    plt.savefig('assets/graficates/authors.png', bbox_inches='tight')
    plt.show()


def graficate_year(data):
    ''' esta funcion tomara un hasmap de datos bibtex y generara una grafica de linea con los años'''
    years_count = {}

    for entry in data:
        if 'year' in entry:
            # Extraer solo los caracteres numéricos del año
            year = re.sub(r'\D', '', entry['year'])
            if year:  # Verifica que no esté vacío después de eliminar letras
                year = int(year)
                # Contar cada año de forma individual sin agrupación
                years_count[year] = years_count.get(year, 0) + 1

    # Ordenar los años y sus conteos
    years, count_years = zip(*sorted(years_count.items()))

    plt.figure(figsize=(18, 6))
    plt.plot(years, count_years, marker='o', linestyle='-', color='blue')
    # Sombrear el área debajo de la línea
    plt.fill_between(years, count_years, color='lightblue', alpha=0.5)
    plt.title('Publications Over Time')
    plt.xlabel('Years')
    plt.ylabel('Number of Publications')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    # Ajuste del eje x para mostrar cada año
    plt.xticks(years, rotation=45)

    # Guardar la figura
    plt.tight_layout()
    plt.savefig('assets/graficates/years_timeline.png')

    plt.show()


def graficar_por_anio_y_tipo(data):
    """
    Genera un gráfico de líneas agrupadas mostrando el número de productos por año y tipo.
    """

    # Recolectar los datos que necesitamos
    registros = []
    for entry in data:
        year = entry.get('year')
        # Asegúrate que sea la clave correcta en tu estructura
        tipo = entry.get('type')
        if year and tipo:
            registros.append({'year': int(year), 'type': tipo})

    # Crear DataFrame
    df = pd.DataFrame(registros)

    # Agrupar por año y tipo, y contar
    conteo = df.groupby(['year', 'type']).size().unstack(fill_value=0)

    # Ordenar por año
    conteo = conteo.sort_index()

    # Crear gráfico de líneas
    plt.figure(figsize=(12, 6))
    for tipo in conteo.columns:
        plt.plot(conteo.index, conteo[tipo], marker='o', label=tipo)

    plt.title('Cantidad de productos por año y tipo')
    plt.xlabel('Año de publicación')
    plt.ylabel('Cantidad de productos')
    plt.legend(title='Tipo de producto')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('assets/graficates/productos_por_anio_y_tipo.png')
    plt.show()


def graficate_entertype(data):
    enter_types = {}
    for entry in data:
        if 'type' in entry:
            # Convertir a minúsculas para unificar duplicados como "article" y "Article"
            entry_type = entry['type'].strip().lower()
            enter_types[entry_type] = enter_types.get(entry_type, 0) + 1

    # Ordenar los tipos de entrada por conteo en orden descendente
    sorted_enter_types = sorted(
        enter_types.items(), key=lambda x: x[1], reverse=True)

    # Desempaquetar los datos
    enter_types, count_enter_types = zip(*sorted_enter_types)

    # Envolver los textos largos con textwrap
    enter_types_wrapped = [textwrap.fill(
        etype, width=20) for etype in enter_types]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.title('Entry Types')
    plt.xlabel('Count')
    plt.ylabel('Entry Types')

    # Obtener una paleta de colores distinta para cada barra
    cmap = cm.get_cmap('tab20', len(enter_types))
    colors = [cmap(i) for i in range(len(enter_types))]

    # Crear el gráfico de barras horizontal con colores diferentes
    bars = ax.barh(enter_types_wrapped, count_enter_types, color=colors)

    # Añadir el valor al final de cada barra
    for bar, count in zip(bars, count_enter_types):
        ax.text(
            bar.get_width() + 0.1,  # Posición en el eje x
            bar.get_y() + bar.get_height() / 2,  # Posición en el eje y
            str(count),
            va='center',
            ha='left',
            fontsize=10
        )

    # Añadir la leyenda con los colores respectivos
    ax.legend(bars, enter_types, title='Entry Types', bbox_to_anchor=(
        1.05, 1), loc='upper left', fontsize=10, ncol=1)

    # Invertir el eje y para que el tipo con más publicaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que la leyenda no se corte

    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Ajuste inicial
    plt.subplots_adjust(left=0.2, right=0.85, top=0.9,
                        bottom=0.1)  # Ajuste adicional

    # Guardar la figura
    plt.savefig('assets/graficates/entry_types.png', bbox_inches='tight')

    # Mostrar la figura
    plt.show()


def graficate_journals(data):
    journals = {}

    # Contar la cantidad de veces que aparece cada journal
    for entry in data:
        if 'journal' in entry:
            journals[entry['journal']] = journals.get(entry['journal'], 0) + 1

    # Ordenar los journals por el número de apariciones en orden descendente y tomar los 25 primeros
    top_journals = sorted(
        journals.items(), key=lambda x: x[1], reverse=True)[:25]

    # Verificar que top_journals no esté vacío
    if not top_journals:
        print("No hay journals con suficientes datos para graficar.")
        return

    # Desempaquetar los datos de los 25 journals más citados
    journals, count_journals = zip(*top_journals)

    # Ajustar los nombres de los journals largos con saltos de línea
    journals_wrapped = [textwrap.fill(journal, width=30)
                        for journal in journals]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(24, 20))
    plt.title('Top 25 Journals by Citations')
    plt.xlabel('Count')
    plt.ylabel('Journals')

    # Generar una paleta de colores única para cada barra
    cmap = cm.get_cmap('tab20', len(journals))
    colors = [cmap(i) for i in range(len(journals))]

    # Crear el gráfico de barras horizontal con colores individuales
    bars = ax.barh(journals_wrapped, count_journals, color=colors)

    # Agregar el total al final de cada barra
    for bar, count in zip(bars, count_journals):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2, str(count),
                va='center', ha='left', fontsize=10)

    # Invertir el eje y para que el journal con más citaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que no se corte
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # Guardar la figura
    plt.savefig('assets/graficates/top_journals.png')
    plt.show()


def graficate_publisher(data):
    publisher = {}

    for entry in data:
        if 'publisher' in entry:
            publisher[entry['publisher']] = publisher.get(
                entry['publisher'], 0) + 1

    # Ordenar los publishers por el número de apariciones en orden descendente
    sorted_publisher = sorted(
        publisher.items(), key=lambda x: x[1], reverse=True)

    # Desempaquetar los datos
    publishers, count_publishers = zip(*sorted_publisher)

    # Ajustar los nombres de los publishers largos con saltos de línea
    publishers_wrapped = [textwrap.fill(pub, width=30) for pub in publishers]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(24, 20))
    plt.title('Top Publishers')
    plt.xlabel('Count')
    plt.ylabel('Publishers')

    # Crear una paleta de colores distinta para cada barra
    cmap = cm.get_cmap('tab20', len(publishers))
    colors = [cmap(i) for i in range(len(publishers))]

    # Crear el gráfico de barras horizontal con colores individuales
    bars = ax.barh(publishers_wrapped, count_publishers, color=colors)

    # Añadir el valor al final de cada barra
    for bar, count in zip(bars, count_publishers):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, str(count),
                va='center', ha='left', fontsize=10)

    # Invertir el eje y para que el publisher con más citaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que no se corte
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # Guardar la figura
    plt.savefig('assets/graficates/top_publishers.png')
    plt.show()


def graficate_databases(data):
    """
    This function will take a bibtex file and generate a pie chart with databases
    """
    databases = []
    count_dbs = []

    for entry in data:
        if 'database' in entry:
            if entry['database'] not in databases:
                databases.append(entry['database'])
                count_dbs.append(1)
            else:
                index = databases.index(entry['database'])
                count_dbs[index] += 1

    colors = [plt.cm.tab10(i / len(databases)) for i in range(len(databases))]

    plt.figure(figsize=(8, 8))
    plt.title('Databases', fontsize=14)

    # Pie chart
    plt.pie(
        count_dbs,
        labels=databases,
        autopct='%1.1f%%',  # mostrar porcentaje
        startangle=90,      # comenzar desde la parte superior
        colors=colors
    )

    plt.legend()
    plt.axis('equal')  # Para que el círculo no quede ovalado

    # Guardar y mostrar
    plt.tight_layout()
    plt.savefig('assets/graficates/databases.png')
    plt.show()


def graficate_type_database(data):
    # Contador para las combinaciones de tipo y base de datos
    type_database_count = {}

    # Crear sets para las bases de datos y tipos únicos
    bases_datos = set()
    tipos = set()

    for entry in data:
        if 'type' in entry and 'database' in entry:
            # Convertir a minúsculas para evitar duplicados por capitalización
            tipo = entry['type'].strip().lower()
            database = entry['database'].strip().lower()

            # Añadir a los sets
            bases_datos.add(database)
            tipos.add(tipo)

            # Contar la cantidad de publicaciones por tipo y base de datos
            type_database_count[(tipo, database)] = type_database_count.get(
                (tipo, database), 0) + 1

    # Convertir los sets a listas ordenadas para un orden consistente
    bases_datos = sorted(list(bases_datos))
    tipos = sorted(list(tipos))[:16]  # Limitar a los 16 tipos únicos

    # Crear una matriz de datos para contar las publicaciones
    count_matrix = np.zeros((len(tipos), len(bases_datos)))

    # Rellenar la matriz con los conteos
    for (tipo, database), count in type_database_count.items():
        if tipo in tipos and database in bases_datos:
            type_idx = tipos.index(tipo)
            database_idx = bases_datos.index(database)
            count_matrix[type_idx, database_idx] = count

    # Precalcular las posiciones de "left" para las barras apiladas
    left_positions = np.cumsum(count_matrix, axis=1) - count_matrix

    # Ajustar los nombres de los tipos largos con saltos de línea
    tipos_wrapped = [textwrap.fill(tipo, width=30) for tipo in tipos]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(20, 12))  # Aumentar el tamaño de la figura

    # Obtener una paleta de colores distinta para cada base de datos
    cmap = cm.get_cmap('tab20', len(bases_datos))
    colors = [cmap(i) for i in range(len(bases_datos))]

    # Graficar cada base de datos como una barra apilada en cada tipo
    width = 0.6  # Ancho de las barras
    for i, database in enumerate(bases_datos):
        ax.barh(tipos_wrapped, count_matrix[:, i], left=left_positions[:,
                i], label=database, height=width, color=colors[i])

    plt.title('Publications by Type and Database', fontsize=18)
    plt.xlabel('Count', fontsize=14)
    plt.ylabel('Types', fontsize=14)
    # Ajustar el tamaño de la fuente de las etiquetas de los tipos
    ax.tick_params(axis='y', labelsize=12)

    # Mostrar la leyenda en la parte superior del gráfico dividida en columnas si es necesario
    ax.legend(title='Database', bbox_to_anchor=(1.05, 1),
              loc='upper left', fontsize=10, ncol=2)

    # Invertir el eje y para que el tipo con más publicaciones esté arriba
    ax.invert_yaxis()

    # Ajustar el espaciado de la figura para que todo se vea bien
    plt.subplots_adjust(left=0.25, right=0.85, top=0.9, bottom=0.1)

    # Guardar la figura
    plt.savefig('assets/graficates/types_databases.png')
    plt.show()


def heatmap_tipo_vs_anio(data):
    """
    Genera un heatmap cruzando tipo de producto vs año de publicación.
    """

    registros = []
    for entry in data:
        year = entry.get('year')
        tipo = entry.get('type')
        if year and tipo:
            registros.append({'year': int(year), 'type': tipo.strip().lower()})

    df = pd.DataFrame(registros)

    # Crear tabla de conteo
    tabla = df.groupby(['type', 'year']).size().unstack(fill_value=0)

    # Ordenar columnas (años)
    tabla = tabla.reindex(sorted(tabla.columns), axis=1)

    # Graficar
    plt.figure(figsize=(14, 6))
    sb.heatmap(tabla, annot=True, fmt='d', cmap='YlGnBu')
    plt.title('Mapa de calor: Tipo de producto por Año de publicación')
    plt.xlabel('Año')
    plt.ylabel('Tipo de producto')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('assets/graficates/heatmap_tipo_anio.png')
    plt.show()


def normalizar_variables(lista):
    mapeo = {}
    for item in lista:
        partes = [p.strip().lower() for p in item.split('-')]
        base = partes[-1] if len(partes) > 1 else partes[0]
        for p in partes:
            mapeo[p] = base
    return mapeo

def contar_frecuencias_global(abstracts, categorias):
    """
    Retorna un Counter global con todas las palabras clave normalizadas de todas las categorías.
    """
    global_map = {}
    for palabras in categorias.values():
        global_map.update(normalizar_variables(palabras))

    conteo = Counter()
    for abstract in abstracts:
        for palabra, base in global_map.items():
            if palabra in abstract:
                conteo[base] += 1
    return conteo

def graficar_wordcloud(freq, nombre):
    if not freq:
        return
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq)
    os.makedirs('assets/graficates/wordclouds', exist_ok=True)
    wc.to_file(f'assets/graficates/wordclouds/{nombre}_cloud.png')

def graficar_tabla(freq, nombre):
    if not freq:
        return
    df = pd.DataFrame(freq.items(), columns=['Keyword', 'Count']).sort_values(by='Count', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    tabla = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)
    os.makedirs('assets/graficates/tablas', exist_ok=True)
    plt.savefig(f'assets/graficates/tablas/{nombre}_table.png', bbox_inches='tight')
    plt.close()

# ---------- Función principal reorganizada ----------

def generate_table_words(data):
    

    categories = {
        'Habilities': cl.CategoriesLists. habilities,
        'Computational Concepts': cl.CategoriesLists.computal_concepts,
        'Attitudes': cl.CategoriesLists.actitudes,
        'Psychometric Properties': cl.CategoriesLists.psychometric_properties,
        'Evaluation Tools': cl.CategoriesLists.evaluation_tools,
        'Investigation Design': cl.CategoriesLists.investigation_design,
        'Schooling Level': cl.CategoriesLists.schooling_level,
        'Medium': cl.CategoriesLists.medio,
        'Strategy': cl.CategoriesLists.strategy,
        'Tools': cl.CategoriesLists.tools
    }

    abstracts = [entry['abstract'].lower() for entry in data if 'abstract' in entry]
    resumen_categorias = []
    
    # Paso 1: Frecuencia global
    freq_global = contar_frecuencias_global(abstracts, categories)
    graficar_wordcloud(freq_global, "Global")
    graficar_tabla(freq_global, "Global")

    # Paso 2: Procesar por cada categoría
    for nombre_cat, palabras in categories.items():
        word_map = normalizar_variables(palabras)
        freq = Counter()
        for abstract in abstracts:
            for palabra, base in word_map.items():
                if palabra in abstract:
                    freq[base] += 1

        total_cat = sum(freq.values())
        resumen_categorias.append((nombre_cat, total_cat))

        graficar_wordcloud(freq, nombre_cat)
        graficar_tabla(freq, nombre_cat)

        # Si es habilidades, crear tabla adicional
        if nombre_cat == "Habilities":
            graficar_tabla(freq, "Habilities_only")

    # Tabla resumen final de categorías
    df_resumen = pd.DataFrame(resumen_categorias, columns=["Category", "Total"])
    df_resumen = df_resumen.sort_values(by="Total", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    tabla = ax.table(cellText=df_resumen.values, colLabels=df_resumen.columns, loc='center', cellLoc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)
    os.makedirs('assets/graficates', exist_ok=True)
    plt.savefig('assets/graficates/words_by_category_table.png', bbox_inches='tight')
    plt.close()
