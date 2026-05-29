"""
Download and inspect FLIP Meltome dataset.

Requirements:
    pip install requests pandas

Usage:
    python 01_download_meltome.py
"""

import os
import io
import zipfile
import requests
import pandas as pd

DATA_DIR = "flip_meltome"
FLIP_URL = "https://github.com/J-SNACKKB/FLIP/raw/main/splits/meltome/splits.zip"


# ── Download ──────────────────────────────────────────────────────────────────

def download_meltome(data_dir: str = DATA_DIR) -> None:
    os.makedirs(data_dir, exist_ok=True)
    zip_path = os.path.join(data_dir, "splits.zip")

    if os.path.exists(zip_path):
        print(f"Already downloaded: {zip_path}")
    else:
        print(f"Downloading from {FLIP_URL} ...")
        r = requests.get(FLIP_URL, timeout=60)
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            f.write(r.content)
        print(f"Saved {len(r.content) / 1e6:.1f} MB to {zip_path}")

    print("Extracting ...")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(data_dir)
    print(f"Files in {data_dir}/:")
    for fname in sorted(os.listdir(data_dir)):
        fpath = os.path.join(data_dir, fname)
        size = os.path.getsize(fpath)
        print(f"  {fname:40s}  {size / 1e3:8.1f} KB")


# ── Inspect ───────────────────────────────────────────────────────────────────

def inspect_meltome(data_dir: str = DATA_DIR) -> dict[str, pd.DataFrame]:
    data_dir = os.path.join(data_dir, "splits")
    csv_files = sorted(
        f for f in os.listdir(data_dir) if f.endswith(".csv")
    )
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_dir}")

    splits = {}
    for fname in csv_files:
        split_name = fname.replace(".csv", "")
        df = pd.read_csv(os.path.join(data_dir, fname))
        splits[split_name] = df

    print("\n" + "=" * 60)
    print("FLIP MELTOME — DATASET SUMMARY")
    print("=" * 60)

    for name, df in splits.items():
        print(f"\n── Split: {name} ──")
        print(f"  Total rows : {len(df):,}")
        print(f"  Columns    : {list(df.columns)}")

        if "set" in df.columns:
            counts = df["set"].value_counts().sort_index()
            for subset, n in counts.items():
                print(f"  {subset:10s}: {n:,}")

        if "sequence" in df.columns:
            seq_lens = df["sequence"].str.len()
            print(f"  Seq length : min={seq_lens.min()}  "
                  f"median={seq_lens.median():.0f}  max={seq_lens.max()}")

        if "target" in df.columns:
            t = df["target"]
            print(f"  Target (Tm): min={t.min():.1f}  "
                  f"mean={t.mean():.1f}  max={t.max():.1f}  "
                  f"NaN={t.isna().sum()}")

    return splits


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    download_meltome()
    splits = inspect_meltome()

    # Save a quick peek at the first split
    first_name, first_df = next(iter(splits.items()))
    print(f"\nFirst 5 rows of '{first_name}':")
    print(first_df.head().to_string(max_colwidth=60))