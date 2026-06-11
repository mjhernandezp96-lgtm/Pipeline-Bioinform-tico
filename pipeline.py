#!/usr/bin/env python3
"""
Pipeline Bioinformático: Identificación de Familias Pfam en Proteínas

Uso:
    python pipeline.py

El pipeline ejecuta automáticamente:
  1. Descarga y extracción de Pfam-A.hmm
  2. Descarga de secuencias UniProt
  3. Indexación con hmmpress
  4. Búsqueda con hmmscan
  5. Parseo de resultados
  6. Generación de CSV y HTML
  7. Generación de gráficos
"""

import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from src.download_pfam import run_pfam_download
from src.download_uniprot import run_uniprot_download
from src.hmmer_scan import run_hmmer_scan
from src.results_parser import run_results_parser, FINAL_CSV, REPORT_HTML
from src.graphs import generate_graphs


def main():
    start = time.time()

    print("=" * 65)
    print("  Pfam Protein Family Identification Pipeline")
    print("=" * 65)

    # Step 1: Download and extract Pfam subset
    print("\n[1/6] Downloading and extracting Pfam families ...")
    pfam_subset = run_pfam_download("data/pfam_families.txt")

    # Step 2: Download UniProt sequences
    print("\n[2/6] Downloading UniProt protein sequences ...")
    proteins_data = run_uniprot_download("data/uniprot_ids.txt")

    # Step 3: Run hmmpress + hmmscan
    print("\n[3/6] Running HMMER (hmmpress + hmmscan) ...")
    tbl_file = run_hmmer_scan()

    # Step 4: Parse results
    print("\n[4/6] Parsing hmmscan results ...")
    uniprot_ids = [p["uniprot_id"] for p in proteins_data]
    proteins = run_results_parser(tbl_file, uniprot_ids)

    # Step 5: Update protein sequences
    for prot in proteins:
        for pd in proteins_data:
            if prot.uniprot_id == pd["uniprot_id"]:
                prot.sequence = pd["sequence"]
                prot.description = pd["description"]
                break

    # Step 6: Generate graphs
    print("\n[5/6] Generating graphs ...")
    generate_graphs(proteins)

    # Summary
    print("\n[6/6] Final summary")
    elapsed = time.time() - start
    n_hits = sum(1 for p in proteins if p.pfam_family)

    print()
    print("=" * 65)
    print("  PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print(f"  Total proteins analyzed:  {len(proteins)}")
    print(f"  With Pfam hits:           {n_hits}")
    print(f"  Without hits:             {len(proteins) - n_hits}")
    print(f"  Hit rate:                 {n_hits / len(proteins) * 100:.1f}%")
    print(f"  Time elapsed:             {elapsed:.1f} seconds")
    print()
    print("  Output files:")
    print(f"    CSV:     {FINAL_CSV}")
    print(f"    HTML:    {REPORT_HTML}")
    print(f"    Graphs:  results/hits_per_protein.png")
    print(f"             results/families_distribution.png")
    print(f"             results/score_distribution.png")
    print("=" * 65)


if __name__ == "__main__":
    main()
