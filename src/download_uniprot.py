import os
import sys
import time

import requests

UNIPROT_BASE = "https://rest.uniprot.org/uniprotkb"
PROTEINS_FASTA = "data/proteins.fasta"


def fetch_fasta(uniprot_id: str) -> tuple[str, str]:
    url = f"{UNIPROT_BASE}/{uniprot_id}.fasta"
    try:
        resp = requests.get(url, timeout=30, headers={"User-Agent": "pfam_pipeline/1.0"})
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"HTTP error for {uniprot_id}: {e}")

    lines = resp.text.strip().splitlines()
    header = lines[0] if lines else ""
    sequence = "".join(line.strip() for line in lines[1:])
    return header, sequence


def run_uniprot_download(ids_file: str) -> list[dict]:
    if not os.path.exists(ids_file):
        print(f"[download_uniprot] ERROR: IDs file not found: {ids_file}", file=sys.stderr)
        sys.exit(1)

    with open(ids_file) as f:
        ids = [line.strip() for line in f if line.strip()]

    print(f"[download_uniprot] Downloading {len(ids)} protein sequences from UniProt ...")

    proteins_data = []
    os.makedirs("data", exist_ok=True)

    with open(PROTEINS_FASTA, "w") as out:
        for uid in ids:
            try:
                header, seq = fetch_fasta(uid)
                proteins_data.append({
                    "uniprot_id": uid,
                    "description": header,
                    "sequence": seq,
                })
                out.write(f">{uid} {header}\n")
                for i in range(0, len(seq), 80):
                    out.write(seq[i:i + 80] + "\n")
                print(f"    OK {uid} ({len(seq)} aa)")
            except Exception as e:
                print(f"    WARNING: Could not download {uid}: {e}")
            time.sleep(0.5)

    print(f"[download_uniprot] Downloaded {len(proteins_data)} proteins to {PROTEINS_FASTA}")
    return proteins_data
