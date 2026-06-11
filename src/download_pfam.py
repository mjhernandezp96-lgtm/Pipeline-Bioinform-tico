import os
import gzip
import subprocess
import sys
import urllib.request
import urllib.error

PFAM_URL = "https://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam38.2/Pfam-A.hmm.gz"
PFAM_GZ = "Pfam-A.hmm.gz"
PFAM_HMM = "Pfam-A.hmm"
PFAM_SUBSET = "data/Pfam_subset.hmm"


def download_file(url: str, dest: str) -> bool:
    if os.path.exists(dest):
        print(f"  File already exists: {dest}")
        return True
    print(f"  Downloading {url} ...")
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"  Downloaded: {dest}")
        return True
    except Exception as e:
        print(f"  ERROR downloading {url}: {e}", file=sys.stderr)
        return False


def decompress_gz(gz_path: str) -> str:
    hmm_path = gz_path.replace(".gz", "")
    if os.path.exists(hmm_path):
        print(f"  Already decompressed: {hmm_path}")
        return hmm_path
    print(f"  Decompressing {gz_path} ...")
    with gzip.open(gz_path, "rb") as f_in:
        with open(hmm_path, "wb") as f_out:
            f_out.write(f_in.read())
    print(f"  Decompressed to {hmm_path}")
    return hmm_path


def extract_subset(pfam_hmm: str, families_file: str, output_hmm: str) -> int:
    if os.path.exists(output_hmm):
        print(f"  Subset already exists: {output_hmm}")
        count = sum(1 for _ in open(output_hmm) if _.startswith("NAME  "))
        return count

    with open(families_file) as f:
        families = [line.strip() for line in f if line.strip()]

    print(f"  Extracting {len(families)} families from {pfam_hmm} ...")

    keys_file = families_file + ".keys"
    with open(keys_file, "w") as f:
        for fam in families:
            f.write(fam + "\n")

    os.makedirs(os.path.dirname(output_hmm) or ".", exist_ok=True)
    cmd = ["hmmfetch", "-f", pfam_hmm, keys_file]
    with open(output_hmm, "w") as fout:
        result = subprocess.run(cmd, stdout=fout, stderr=subprocess.PIPE, text=True)

    os.remove(keys_file)

    if result.returncode != 0:
        print(f"  STDERR: {result.stderr}", file=sys.stderr)

    if os.path.exists(output_hmm):
        count = sum(1 for _ in open(output_hmm) if _.startswith("NAME  "))
        print(f"  Extracted {count} HMM models to {output_hmm}")
        if result.stderr:
            missing = [l for l in result.stderr.strip().split("\n") if l]
            print(f"  Not found: {', '.join(missing)}")
        return count

    print("  ERROR: No HMM models extracted.")
    return 0


def run_pfam_download(families_file: str) -> str:
    if os.path.exists(PFAM_HMM):
        print(f"[download_pfam] {PFAM_HMM} already exists, skipping download")
        pfam_hmm = PFAM_HMM
    else:
        print("[download_pfam] Step 1: Downloading Pfam-A.hmm.gz ...")
        download_file(PFAM_URL, PFAM_GZ)

        print("[download_pfam] Step 2: Decompressing ...")
        pfam_hmm = decompress_gz(PFAM_GZ)

    print("[download_pfam] Step 3: Extracting family subset ...")
    n = extract_subset(pfam_hmm, families_file, PFAM_SUBSET)

    if n == 0:
        print("[download_pfam] ERROR: No families extracted!", file=sys.stderr)
        sys.exit(1)

    return PFAM_SUBSET
