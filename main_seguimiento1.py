import time
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import bibtexparser


#límite de recursión 
sys.setrecursionlimit(5000)  

# ----------------------- Algoritmos de Ordenamiento ------------------------

#*--------- TimSort: Utiliza el algoritmo `sorted()` de Python (O(n log n))
def timsort(arr):
    return sorted(arr)

#*--------- Comb Sort: Una mejora de Bubble Sort que reduce la distancia de comparación progresivamente (O(n^2) peor caso)
def comb_sort(arr):
    gap = len(arr)
    shrink = 1.3
    sorted = False
    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        i = 0
        while i + gap < len(arr):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
            i += 1

#*--------- Selection Sort: Encuentra el valor mínimo y lo coloca en su posición correcta (O(n^2))
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


#*--------- Tree Sort: Inserta elementos en un árbol binario y luego los recupera en orden ascendente (O(n log n))
def tree_sort(arr):
    if len(arr) == 0:
        return []
    root = Node(arr[0])
    for i in range(1, len(arr)):
        root = insert_iterative(root, arr[i])
    return inorder_traversal_iterative(root)

# ----------------------- Estructura de Árbol Binario para Tree Sort ------------------------
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

# Función auxiliar para insertar en el árbol de búsqueda binaria de forma iterativa
def insert_iterative(root, key):
    if root is None:
        return Node(key)
    current = root
    while True:
        if key < current.val:
            if current.left is None:
                current.left = Node(key)
                break
            else:
                current = current.left
        else:
            if current.right is None:
                current.right = Node(key)
                break
            else:
                current = current.right
    return root

# Recorrido en orden (inorder traversal) del árbol binario
def inorder_traversal_iterative(root):
    res = []
    stack = []
    current = root
    while current is not None or len(stack) > 0:
        while current is not None:
            stack.append(current)
            current = current.left
        current = stack.pop()
        res.append(current.val)
        current = current.right
    return res


#*--------- Pigeonhole Sort: Ordena números con un rango limitado de valores (O(n + range))
def pigeonhole_sort(arr):
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1
    holes = [0] * size
    for x in arr:
        holes[x - min_val] += 1
    sorted_arr = []
    for count in range(size):
        while holes[count] > 0:
            sorted_arr.append(count + min_val)
            holes[count] -= 1
    return sorted_arr

#*--------- Bucket Sort: Distribuye los elementos en "cubetas", ordena cada cubeta y luego combina (O(n + k))
def bucket_sort(arr):
    if len(arr) == 0:
        return []
    
    # Encontrar el valor máximo para determinar el número de cubetas
    max_val = max(arr)
    size = len(arr)
    
    # Crear cubetas vacías
    bucket = [[] for _ in range(size)]
    
    # Distribuir los elementos en las cubetas
    for j in arr:
        index_b = int(j * size / (max_val + 1))  # Evita índice fuera de rango
        bucket[index_b].append(j)
    
    # Ordenar los elementos de cada cubeta
    for i in range(size):
        bucket[i] = sorted(bucket[i])
    
    # Combinar los resultados de todas las cubetas
    sorted_arr = []
    for i in range(size):
        sorted_arr.extend(bucket[i])
    
    return sorted_arr

#*--------- QuickSort: Selecciona un pivote, particiona el arreglo y ordena recursivamente (O(n log n) promedio)
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)



#*--------- HeapSort: Convierte el arreglo en un heap y luego extrae los elementos (O(n log n))
def heap_sort(arr):
    n = len(arr)
    for i in range(n//2, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

# Función auxiliar para HeapSort: Reconstruye el heap (O(log n))
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[i] < arr[left]:
        largest = left

    if right < n and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


#*--------- Bitonic Sort: Algoritmo de ordenamiento basado en la secuencia bitónica (O(n log² n))
def comp_and_swap(arr, i, j, dir):
    if (dir == 1 and arr[i] > arr[j]) or (dir == 0 and arr[i] < arr[j]):
        arr[i], arr[j] = arr[j], arr[i]

def bitonic_merge(arr, low, cnt, dir):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            comp_and_swap(arr, i, i + k, dir)
        bitonic_merge(arr, low, k, dir)
        bitonic_merge(arr, low + k, k, dir)

def bitonic_sort(arr, low, cnt, dir):
    if cnt > 1:
        k = cnt // 2
        bitonic_sort(arr, low, k, 1)
        bitonic_sort(arr, low + k, k, 0)
        bitonic_merge(arr, low, cnt, dir)

# Función principal para invocar Bitonic Sort
def sort(arr):
    bitonic_sort(arr, 0, len(arr), 1)

#*--------- Gnome Sort: Algoritmo similar a Insertion Sort pero se mueve hacia adelante y atrás (O(n^2))
def gnome_sort(arr):
    index = 0
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1

#*--------- Binary Insertion Sort: Usa búsqueda binaria para insertar elementos de manera eficiente (O(n^2))
def binary_search(arr, val, start, end):
    if start == end:
        if arr[start] > val:
            return start
        else:
            return start + 1
    if start > end:
        return start
    mid = (start + end) // 2
    if arr[mid] < val:
        return binary_search(arr, val, mid + 1, end)
    elif arr[mid] > val:
        return binary_search(arr, val, start, mid - 1)
    else:
        return mid

def binary_insertion_sort(arr):
    for i in range(1, len(arr)):
        val = arr[i]
        j = binary_search(arr, val, 0, i - 1)
        arr = arr[:j] + [val] + arr[j:i] + arr[i + 1:]

#*--------- Radix Sort: Ordena los números dígito por dígito (O(nk))
def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
    for i in range(n):
        arr[i] = output[i]

# k es el número de dígitos en el número más grande y n es el número de elementos en el array.
def radix_sort(arr):
    max_val = max(arr)  # Encuentra el valor máximo en el array
    exp = 1  # Inicializa el valor de exponentes para la posición de los dígitos
    while max_val // exp > 0:  # Itera a través de cada posición de dígito (unidades, decenas, etc.)
        counting_sort(arr, exp)  # Ordena los números en función del dígito actual
        exp *= 10  # Mueve al siguiente dígito (decenas, centenas, etc.)

#? ------------------- Fin de los Algoritmos de Ordenamiento -------------------

# Función para medir el tiempo de los algoritmos
def medir_tiempo(algoritmo, arr):
    inicio = time.time()
    algoritmo(arr)
    fin = time.time()
    return fin - inicio

# Cargar los datos desde un archivo BIB
# Leer el archivo BibTeX
archivo_bibtex = r"C:\Users\Juan Pablo Vélez L\Desktop\Universidad\2. AnálisisDeAlgoritmos\ProyectoAlgoritmos\assets\temps\IEEEC"

with open(archivo_bibtex, encoding="utf-8") as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

# Extraer la información relevante y estructurarla en un DataFrame
data = []
for entry in bib_database.entries:
    year = entry.get("year", "N/A")  # Año
    authors = entry.get("author", "N/A")  # Autores
    title = entry.get("title", "N/A")  # Título
    doc_type = entry.get("ENTRYTYPE", "N/A")  # Tipo de documento (ejemplo: article, book)

    data.append({"Year": year, "Authors": authors, "Title": title, "Document Type": doc_type})

# Convertir a DataFrame de pandas
datos = pd.DataFrame(data)

# Asegurar que el campo "Year" sea numérico para ordenamientos correctos
datos["Year"] = pd.to_numeric(datos["Year"], errors="coerce")

# Definir las columnas a utilizar
columnas_validas = ["Year", "Authors", "Title", "Document Type"]

# Lista de algoritmos de ordenamiento
algoritmos_generales = [timsort, comb_sort, selection_sort, tree_sort, quicksort, heap_sort, sort, gnome_sort, binary_insertion_sort]
algoritmos_numericos = [pigeonhole_sort, bucket_sort, radix_sort]

# Diccionario para almacenar los tiempos de ejecución
resultados_tiempos = {columna: {} for columna in columnas_validas}

# Ejecutar los algoritmos sobre las 4 columnas
for columna in columnas_validas:
    print(f"\nTiempos de ejecución para la columna: {columna}\n")
    datos_lista = datos[columna].dropna().tolist()  # Eliminar valores NaN

    if columna != "Year":  
        datos_lista = [str(item) for item in datos_lista]  # Convertir a string si no es numérico
    
    # Elegir los algoritmos adecuados según el tipo de la columna
    if columna == "Year":
        algoritmos = algoritmos_generales + algoritmos_numericos
    else:
        algoritmos = algoritmos_generales

    # Medir tiempos de cada algoritmo para la columna actual
    for algoritmo in algoritmos:
        arr_copy = datos_lista.copy()
        tiempo = medir_tiempo(algoritmo, arr_copy)
        resultados_tiempos[columna][algoritmo.__name__] = tiempo
        print(f"{algoritmo.__name__}: {tiempo:.6f} segundos")

# Crear la visualización interactiva
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3)

def actualizar_grafico(label):
    ax.clear()
    tiempos_columna = resultados_tiempos[label]
    
    colores = plt.cm.plasma(np.linspace(0, 1, len(tiempos_columna)))

    # Crear gráfico de barras con colores personalizados
    ax.bar(tiempos_columna.keys(), tiempos_columna.values(),color=colores)
    
    ax.set_title(f"Tiempos de ejecución para la columna: {label}")
    ax.set_xlabel("Algoritmos de Ordenamiento")
    ax.set_ylabel("Tiempo de ejecución (segundos)")

    # Corrección: definir los ticks antes de asignar etiquetas
    ax.set_xticks(range(len(tiempos_columna)))  
    ax.set_xticklabels(tiempos_columna.keys(), rotation=45, ha="right")

    plt.draw()
    plt.show()


ax_radio = plt.axes([0.05, 0.4, 0.15, 0.15], facecolor='lightgoldenrodyellow')
radio = RadioButtons(ax_radio, columnas_validas)
radio.on_clicked(actualizar_grafico)

actualizar_grafico('Year')
plt.savefig('assets/temps/IEEEFinal.png')