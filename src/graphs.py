import os
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.models import Protein


def generate_graphs(proteins: list[Protein]):
    print("[graphs] Generating graphs ...")
    os.makedirs("results", exist_ok=True)

    with_hits = sum(1 for p in proteins if p.pfam_family)
    without_hits = len(proteins) - with_hits

    # --- Graph 1: Proteins with/without hits ---
    fig, ax = plt.subplots(figsize=(7, 6))
    labels = ["With Pfam hit", "Without hit"]
    sizes = [with_hits, without_hits]
    colors = ["#2ecc71", "#e74c3c"]
    ax.pie(sizes, labels=labels, autopct="%1.1f%%",
           colors=colors, startangle=90, textprops={"fontsize": 12})
    ax.set_title("Proteins with Pfam Hits", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("results/hits_per_protein.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("[graphs] Saved: results/hits_per_protein.png")

    # --- Graph 2: Family distribution (top 15) ---
    families = [p.pfam_family for p in proteins if p.pfam_family]
    counter = Counter(families)
    top = counter.most_common(15)
    names = [f"{fam} ({cnt})" for fam, cnt in top]
    counts = [cnt for _, cnt in top]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(range(len(names)), counts, color="#3498db", edgecolor="white")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel("Number of proteins", fontsize=12)
    ax.set_title("Pfam Family Distribution (Top 15)", fontsize=14, fontweight="bold")
    ax.invert_yaxis()

    for bar, val in zip(bars, counts):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=10)

    plt.tight_layout()
    plt.savefig("results/families_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("[graphs] Saved: results/families_distribution.png")

    # --- Graph 3: Score distribution ---
    fig, ax = plt.subplots(figsize=(10, 5))
    scores = [p.score for p in proteins if p.score > 0]
    if scores:
        ax.hist(scores, bins=20, color="#9b59b6", edgecolor="white", alpha=0.8)
        ax.set_xlabel("HMMER Score", fontsize=12)
        ax.set_ylabel("Number of proteins", fontsize=12)
        ax.set_title("Score Distribution of Pfam Hits", fontsize=14, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("results/score_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("[graphs] Saved: results/score_distribution.png")

    print("[graphs] All graphs generated successfully")
