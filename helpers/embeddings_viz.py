"""Embeddings visualization using matplotlib."""

import json
import numpy as np
from pathlib import Path
from sklearn.decomposition import PCA
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATASETS = Path(__file__).resolve().parent.parent / "datasets"
OUTPUT = Path(__file__).resolve().parent / "embeddings.png"


def load_embeddings(name: str) -> dict:
    path = DATASETS / f"{name}.json"
    with open(path) as f:
        data = json.load(f)
    return {k: np.array(v) for k, v in data.items()}


def save_viz(n=5):
    embeds = load_embeddings("category_embeddings")
    labels = list(embeds.keys())
    vectors = np.array(list(embeds.values()))

    pca = PCA(n_components=2)
    coords = pca.fit_transform(vectors)

    plt.figure(figsize=(10, 8))
    colors = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A", "#F4A261"]

    for i in range(min(n, len(labels))):
        x, y = coords[i]
        plt.scatter(
            x,
            y,
            c=colors[i % len(colors)],
            s=300,
            label=labels[i],
            edgecolors="black",
            linewidth=2,
            zorder=5,
        )
        plt.annotate(
            labels[i],
            (x, y),
            xytext=(8, 8),
            textcoords="offset points",
            fontsize=11,
            fontweight="bold",
            color="#1B263B",
        )

    plt.title(f"Category Embeddings (PCA)", fontsize=16, fontweight="bold", pad=20)
    plt.xlabel("Principal Component 1", fontsize=12)
    plt.ylabel("Principal Component 2", fontsize=12)
    plt.grid(True, alpha=0.3, linestyle="--")
    plt.legend(loc="best", fontsize=10, framealpha=0.9)
    plt.tight_layout()
    plt.savefig(OUTPUT, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    save_viz()
