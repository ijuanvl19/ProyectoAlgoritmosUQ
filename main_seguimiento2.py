# main_seguimiento2.py - REESTRUCTURADO PARA WINDOWS 11 (CORREGIDO IMPORTS)

import os
import sys
import time
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
from tabulate import tabulate
import bibtexparser

# ----------------------- Configuración de rutas ------------------------

# Ruta base del proyecto
BASE_DIR = r"C:\Users\Juan Pablo Vélez L\Desktop\Universidad\2. AnálisisDeAlgoritmos\ProyectoAlgoritmos"
SORTING_DIR = os.path.join(BASE_DIR, "sorting")
BIBTEX_FILE = os.path.join(BASE_DIR, "assets", "temps", "IEEEConsolidated.bib")

# Agregar carpeta base al sys.path para reconocer paquetes
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# ----------------------- Importación de algoritmos ------------------------

from sorting.timSort import timsort
from sorting.CombSort import comb_sort
from sorting.SelectionSort import selection_sort
from sorting.TreeSort import tree_sort
from sorting.BubbleSort import bubble_sort
from sorting.GnomeSort import gnome_sort
from sorting.BinaryInsertionSort import binary_insertion_sort
from sorting.PigeonholeSort import pigeonhole_sort
from sorting.BucketSort import bucket_sort
from sorting.QuickSort import quicksort
from sorting.HeapSort import heap_sort
from sorting.BitonicSort import bitonic_sort
from sorting.RadixSort import radix_sort
from sorting.Cocktail import cocktail_sort
from sorting.ShellSort import shell_sort

# ----------------------- Lista de términos clave ------------------------

terminos_clave = [
    "Abstraction", "Motivation", "Algorithm", "Persistence", "Coding", "Block", "Creativity",
    "Mobile application", "Logic", "Programming", "Conditionals", "Robotic", "Loops", "Scratch"
]

# ----------------------- Leer archivo BibTeX ------------------------

with open(BIBTEX_FILE, encoding="utf-8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

abstracts = [entry.get("abstract", "") for entry in bib_database.entries if "abstract" in entry]
texto_completo = " ".join(abstracts).lower()

# ----------------------- Contar ocurrencias ----------------------------

frecuencias = {}
for termino in terminos_clave:
    expresion = re.escape(termino.lower())
    frecuencias[termino] = len(re.findall(expresion, texto_completo))

datos = list(frecuencias.items())

# Mostrar tabla una sola vez
print("\nFrecuencia de términos antes de ordenar:\n")
print(tabulate(datos, headers=["Término", "Frecuencia"], tablefmt="fancy_grid"))

# ----------------------- Algoritmos de ordenamiento --------------------

algoritmos = {
    "TimSort": timsort,
    "Comb Sort": comb_sort,
    "Selection Sort": selection_sort,
    "Tree Sort": tree_sort,
    "Bubble Sort": bubble_sort,
    "Gnome Sort": gnome_sort,
    "Binary Insertion Sort": binary_insertion_sort,
    "Pigeonhole Sort": pigeonhole_sort,
    "Bucket Sort": bucket_sort,
    "Quick Sort": quicksort,
    "Heap Sort": heap_sort,
    "Bitonic Sort": bitonic_sort,
    "Radix Sort": radix_sort,
    "Cocktail Sort": cocktail_sort,
    "Shell Sort": shell_sort
}

# ----------------------- Ejecución y visualización dinámica ----------------------

tiempos_ejecucion = {}
resultados_ordenados = {}

for nombre, algoritmo in algoritmos.items():
    entrada = datos.copy()
    inicio = time.time()
    ordenado = algoritmo(entrada)
    tiempo = time.time() - inicio
    tiempos_ejecucion[nombre] = tiempo
    resultados_ordenados[nombre] = ordenado
    print(f"[{nombre}] Tiempo: {tiempo:.6f} segundos")

# Gráfico dinámico
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3)

opciones = list(algoritmos.keys()) + ["Comparativo"]

def actualizar(label):
    ax.clear()
    if label == "Comparativo":
        colores = plt.cm.plasma(np.linspace(0, 1, len(tiempos_ejecucion)))
        ax.bar(tiempos_ejecucion.keys(), tiempos_ejecucion.values(), color=colores)
        ax.set_title("Comparación de Tiempos de Ejecución")
        ax.set_ylabel("Tiempo (segundos)")
        ax.set_xlabel("Algoritmo")
        ax.set_xticks(range(len(tiempos_ejecucion)))
        ax.set_xticklabels(tiempos_ejecucion.keys(), rotation=45, ha="right")
    else:
        datos = resultados_ordenados[label]
        etiquetas = [x[0] for x in datos]
        valores = [x[1] for x in datos]
        colores = plt.cm.viridis(np.linspace(0, 1, len(etiquetas)))
        ax.bar(etiquetas, valores, color=colores)
        ax.set_title(f"{label} - Frecuencia de Términos\nTiempo: {tiempos_ejecucion[label]:.6f}s")
        ax.set_ylabel("Frecuencia")
        ax.set_xticks(range(len(etiquetas)))
        ax.set_xticklabels(etiquetas, rotation=45, ha="right")
    plt.draw()

ax_radio = plt.axes([0.05, 0.3, 0.2, 0.6], facecolor='lightgoldenrodyellow')
radio = RadioButtons(ax_radio, opciones)
radio.on_clicked(actualizar)
actualizar("TimSort")
plt.show()