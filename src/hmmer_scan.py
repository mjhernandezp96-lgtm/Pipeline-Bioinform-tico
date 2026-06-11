import os
import subprocess
import sys

HMMER_RESULTS = "results/hmmer_results.tbl"
PFAM_SUBSET = "data/Pfam_subset.hmm"
PROTEINS_FASTA = "data/proteins.fasta"


def run_hmmpress(hmm_db: str):
    """Index the HMM database using hmmpress."""
    exts = [".h3f", ".h3i", ".h3m", ".h3p"]
    if all(os.path.exists(hmm_db + ext) for ext in exts):
        print("[hmmer_scan] hmmpress already done")
        return

    print(f"[hmmer_scan] Running hmmpress on {hmm_db} ...")
    result = subprocess.run(["hmmpress", hmm_db], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  STDERR: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"hmmpress failed with return code {result.returncode}")
    print("[hmmer_scan] hmmpress completed successfully")


def run_hmmscan(hmm_db: str, fasta_file: str, output_tbl: str):
    """Run hmmscan to search sequences against the HMM database."""
    print(f"[hmmer_scan] Running hmmscan ...")
    cmd = [
        "hmmscan",
        "--tblout", output_tbl,
        "--noali",
        "-E", "10",
        hmm_db,
        fasta_file,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  STDERR: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"hmmscan failed with return code {result.returncode}")
    print(f"[hmmer_scan] Results saved to {output_tbl}")


def run_hmmer_scan():
    """Orchestrate hmmpress and hmmscan."""
    if not os.path.exists(PFAM_SUBSET):
        print(f"[hmmer_scan] ERROR: {PFAM_SUBSET} not found", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(PROTEINS_FASTA):
        print(f"[hmmer_scan] ERROR: {PROTEINS_FASTA} not found", file=sys.stderr)
        sys.exit(1)

    os.makedirs("results", exist_ok=True)
    run_hmmpress(PFAM_SUBSET)
    run_hmmscan(PFAM_SUBSET, PROTEINS_FASTA, HMMER_RESULTS)
    return HMMER_RESULTS
