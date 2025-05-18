import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_distances
from scipy.cluster.hierarchy import dendrogram, linkage
import re
import nltk
from nltk.corpus import stopwords
from cleaning import clean_data as cd
import time

# Descargar stopwords si no están
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

# --- Preprocesamiento ---
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)  # quitar puntuación
    stop_words = set(stopwords.words('english'))
    palabras = texto.split()
    palabras_limpias = [w for w in palabras if w not in stop_words]
    return ' '.join(palabras_limpias)

# --- Cargar abstracts desde archivo .bib ---
def get_abstracts_from_bibtex(bibtex_file):
    archivos = cd.leer_bibtex_con_mmap_regex(bibtex_file)
    resúmenes = []
    for entry in archivos:
        if 'abstract' in entry:
            resúmenes.append(entry['abstract'])
    return resúmenes

# Cargar y preprocesar
abstracts = get_abstracts_from_bibtex("assets/temps/Consolidated.bib")
abstracts_limpios = [limpiar_texto(abstract) for abstract in abstracts]
df = pd.DataFrame({'abstract': abstracts, 'abstract_limpio': abstracts_limpios})

# --- Vectorización TF-IDF optimizada ---
vectorizer = TfidfVectorizer(max_features=1000)
X_tfidf = vectorizer.fit_transform(df["abstract_limpio"])

# --- Clustering jerárquico 1: Ward linkage ---
start_ward = time.time()
model_ward = AgglomerativeClustering(n_clusters=3, linkage='ward')
df["cluster_ward"] = model_ward.fit_predict(X_tfidf.toarray())
end_ward = time.time()

# --- Clustering jerárquico 2: Average linkage con matriz de distancias ---
start_avg = time.time()
dist_matrix = cosine_distances(X_tfidf)
model_avg = AgglomerativeClustering(n_clusters=3, metric='precomputed', linkage='average')
df["cluster_avg"] = model_avg.fit_predict(dist_matrix)
end_avg = time.time()

# --- Dendrogramas con límite de muestras para mayor claridad ---
max_muestras = 100
subset = min(max_muestras, len(df))

# Ward
linkage_matrix_ward = linkage(X_tfidf.toarray()[:subset], method='ward')
plt.figure(figsize=(10, 5))
dendrogram(linkage_matrix_ward, labels=np.arange(subset))
plt.title("Dendrograma - Ward Linkage (muestras limitadas)")
plt.tight_layout()
plt.savefig("assets/dendrograma_ward.png")
plt.show()

# Average
linkage_matrix_avg = linkage(dist_matrix[:subset, :subset], method='average')
plt.figure(figsize=(10, 5))
dendrogram(linkage_matrix_avg, labels=np.arange(subset))
plt.title("Dendrograma - Average Linkage (muestras limitadas)")
plt.tight_layout()
plt.savefig("assets/dendrograma_avg.png")
plt.show()

# --- Evaluación sin categorías reales ---
sil_ward = silhouette_score(X_tfidf, df["cluster_ward"])
sil_avg = silhouette_score(X_tfidf, df["cluster_avg"])

print(f"Silhouette Score - Ward: {sil_ward:.3f} (Tiempo: {end_ward - start_ward:.2f}s)")
print(f"Silhouette Score - Average: {sil_avg:.3f} (Tiempo: {end_avg - start_avg:.2f}s)")

# --- Conteo por cluster ---
print("\nDistribución por cluster (Ward):")
print(df["cluster_ward"].value_counts().sort_index())

print("\nDistribución por cluster (Average):")
print(df["cluster_avg"].value_counts().sort_index())
