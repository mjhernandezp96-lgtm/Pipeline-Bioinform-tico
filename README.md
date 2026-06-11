# Pipeline Bioinformático: Identificación de Familias Pfam

Pipeline en Python que identifica familias de proteínas Pfam en un conjunto de proteínas de UniProt utilizando **HMMER** (Modelos Ocultos de Markov).

## Objetivo

Desarrollar un pipeline bioinformático automatizado que:

1. Descargue la base de datos Pfam-A.hmm desde el FTP de EBI
2. Extraiga un subconjunto de familias Pfam específicas
3. Descargue secuencias de proteínas desde UniProt
4. Ejecute `hmmscan` para identificar familias Pfam
5. Genere reportes CSV, HTML y gráficos estadísticos

## Requisitos

| Software | Versión |
|----------|---------|
| Python | 3.10+ |
| HMMER | 3.x (hmmscan, hmmpress, hmmfetch) |
| Git | 2.x |

## Instalación

### 1. Instalar HMMER

```bash
sudo apt update
sudo apt install hmmer -y
```

Verificar:

```bash
hmmscan -h
hmmpress -h
hmmfetch -h
```

### 2. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd pfam_pipeline
```

### 3. Crear entorno virtual e instalar dependencias

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

Activar el entorno virtual y ejecutar:

```bash
source .venv/bin/activate
python pipeline.py
```

El pipeline ejecuta automáticamente:

| Paso | Descripción |
|------|-------------|
| 1/6 | Descarga Pfam-A.hmm.gz (~399 MB) y extrae subconjunto |
| 2/6 | Descarga secuencias FASTA desde UniProt |
| 3/6 | Indexa con hmmpress y ejecuta hmmscan |
| 4/6 | Parsea resultados y genera CSV + HTML |
| 5/6 | Genera gráficos estadísticos |
| 6/6 | Muestra resumen final |

## Estructura del proyecto

```
pfam_pipeline/
│
├── pipeline.py                 # Orquestador principal
├── README.md                   # Documentación
├── .gitignore                  # Archivos ignorados
├── requirements.txt            # Dependencias Python
│
├── data/
│   ├── pfam_families.txt       # Familias Pfam a buscar (Anexo 1)
│   ├── uniprot_ids.txt         # IDs de UniProt (Anexo 2)
│   ├── Pfam_subset.hmm         # Subconjunto de Pfam (generado)
│   └── proteins.fasta          # Secuencias descargadas (generado)
│
├── src/
│   ├── protein.py              # Clase Protein (POO)
│   ├── download_pfam.py        # Descarga y extracción de Pfam
│   ├── download_uniprot.py     # Descarga de secuencias UniProt
│   ├── hmmer_scan.py           # Ejecución de HMMER
│   ├── results_parser.py       # Parseo de resultados
│   └── graphs.py               # Generación de gráficos
│
└── results/
    ├── final_results.csv       # Resultados en CSV
    ├── report.html             # Reporte HTML
    ├── hmmer_results.tbl       # Salida tabular de hmmscan
    ├── hits_per_protein.png    # Gráfico de proteínas con/sin hits
    ├── families_distribution.png # Distribución de familias
    └── score_distribution.png  # Distribución de scores
```

## Clase Protein (POO)

La clase `Protein` en `src/protein.py` utiliza **properties** (getters/setters) y encapsulación:

```python
class Protein:
    # Propiedades: uniprot_id, sequence, description,
    #              pfam_family, pfam_accession, score, evalue
    def __str__(self) -> str  # Representación legible
```

## Resultados

### CSV (`results/final_results.csv`)

```
Protein_ID,Pfam_Family,Score
P01112,Ras,204.80
P12931,SH2,97.60
P62993,SH3_1,122.40
```

### HTML (`results/report.html`)

Tabla HTML responsiva con todos los resultados.

### Gráficos

- `hits_per_protein.png`: Proporción de proteínas con/without hits
- `families_distribution.png`: Top 15 familias Pfam encontradas
- `score_distribution.png`: Distribución de scores de HMMER

## Notas

- 7 familias del Anexo 1 no se encontraron en Pfam 38.2 con esos nombres exactos:
  `Protein_kinase`, `Pkinase_Tyr`, `Homeobox`, `HlyD`, `GST_C_family`, `Immunoglobulin`, `Fibronectin`
- Las 31 familias restantes se extrajeron correctamente
- El pipeline omite descargas si los archivos ya existen (reanudable)
