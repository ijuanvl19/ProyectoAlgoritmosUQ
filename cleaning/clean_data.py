import mmap
import os
import bibtexparser
import re


def leer_bibtex(filepath):
    print(f"Leyendo el archivo: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as bibtex_file:
        return bibtexparser.load(bibtex_file)

# Función para combinar múltiples archivos .bib en uno solo


def leer_bibtex_con_mmap_regex(filepath):
    entradas = []
    buffer = []
    # Ajuste para capturar el tipo y el ID de la entrada, incluyendo números u otros caracteres en el ID
    entry_pattern = re.compile(r'@(\w+)\s*\{\s*([^,]+)\s*,', re.DOTALL)
    # Para capturar campos clave-valor
    field_pattern = re.compile(r'(\w+)\s*=\s*\{(.*?)\},?', re.DOTALL)
    i = 0

    with open(filepath, 'r', encoding='utf-8') as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
            for line in iter(mm.readline, b""):
                line = line.decode('utf-8')
                buffer.append(line)

                # Detectar el final de una entrada
                if line.strip() == "}":
                    entrada_completa = ''.join(buffer)
                    entry = {}

                    # Obtener el tipo de entrada y el identificador con el patrón ajustado
                    entry_match = entry_pattern.search(entrada_completa)
                    if entry_match:
                        entry['type'] = entry_match.group(1)
                        entry['id'] = entry_match.group(2).strip()

                    # Obtener campos clave-valor de la entrada
                    for field in field_pattern.findall(entrada_completa):
                        entry[field[0]] = field[1].strip()

                    # Agregar la entrada a la lista
                    entradas.append(entry)

                    # Reiniciar el buffer para la siguiente entrada
                    buffer = []

                i += 1
                print(f"Línea {i}")  # Seguimiento de progreso

    return entradas




def combinar_bibtex_sin_repetidos_por_titulo(archivos_bib, output_filepath):
    
    entradas_unicas = {}
    entradas_repetidas = {}
    entradas_totales = []

    for archivo in archivos_bib:
        print(f"Leyendo el archivo: {archivo}")

        database = archivo.split('/')[1]

        # Leer cada archivo .bib y obtener sus entradas
        print(f"Leyendo el archivo: {archivo}")
       
        if archivo.split('/')[1] == 'IEEE':
            bib_database = leer_bibtex(archivo)
            for entry in bib_database.entries:
                title = entry.get('title', '').strip().lower()

                # Asegurar 'ENTRYTYPE' y 'ID' en cada entrada
                # Asignar 'misc' si no hay tipo
                entry['ENTRYTYPE'] = entry.get('ENTRYTYPE', 'misc')
                # Asignar 'undefined' si no hay ID
                entry['ID'] = entry.get('ID', 'undefined')
                if database != 'temps':
                    entry['database'] = database
                
                entradas_totales.append(entry) 

                if title and title not in entradas_unicas:
                    entradas_unicas[title] = entry
                elif(title and title not in entradas_repetidas) : 
                    entradas_repetidas[title] = entry
        else:
            bib_database = leer_bibtex_con_mmap_regex(archivo)
            for entry in bib_database:
                title = entry.get('title', '').strip().lower()

                entry['ENTRYTYPE'] = entry.get('type', 'misc')
                entry['ID'] = entry.get('id', 'undefined')

                if database != 'temps':
                    entry['database'] = database

                entradas_totales.append(entry) 
                if title and title not in entradas_unicas:
                    entradas_unicas[title] = entry

                elif(title and title not in entradas_repetidas) : 
                    entradas_repetidas[title] = entry

    # Crear una base de datos combinada con las entradas únicas
    bib_database_combinado = bibtexparser.bibdatabase.BibDatabase()
    bib_database_repetidos = bibtexparser.bibdatabase.BibDatabase()
    bib_database_totales = bibtexparser.bibdatabase.BibDatabase()

    bib_database_combinado.entries = list(entradas_unicas.values())
    bib_database_repetidos.entries = list(entradas_repetidas.values())
    bib_database_totales.entries = entradas_totales
    
    # Guardar el archivo combinado
    with open(output_filepath, 'w', encoding='utf-8') as bibtex_file:
        bibtexparser.dump(bib_database_combinado, bibtex_file)

    with open('assets/temps/repetidos.bib', 'w', encoding='utf-8') as bibtex_file:
        bibtexparser.dump(bib_database_repetidos, bibtex_file)

    with open('assets/temps/totales.bib', 'w', encoding='utf-8') as bibtex_file:
        bibtexparser.dump(bib_database_totales, bibtex_file)
    

    print(f"Archivo combinado sin repetidos guardado en: {output_filepath}")


# # Función para obtener todos los archivos .bib de una carpeta
def obtener_archivos_bib(carpeta):
    archivos_bib = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".bib"):  # Verificar que sea un archivo .bib
            archivos_bib.append(os.path.join(carpeta, archivo))
    return archivos_bib


# Función para escribir los datos filtrados en un nuevo archivo .bib
def escribir_bibtex(output_filepath, normaldata_entries):
    with open(output_filepath, 'w', encoding='utf-8') as bibtex_file:
        for entry in normaldata_entries:
            print(f"Escribiendo entrada: {entry}")
            data = entry.get_data()

            # Escribir la entrada en formato .bib
            bibtex_file.write("@data{\n")
            for key, value in data.items():
                bibtex_file.write(f"  {key} = {{{value}}},\n")
            bibtex_file.write("}\n\n")
