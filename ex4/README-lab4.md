# Lab 4 — Graph Neural Networks on OGB (GPU)

## Overview
Node classification on an Open Graph Benchmark dataset with graph neural networks,
comparing GCN, GraphSAGE, and GAT architectures under neighbor sampling. GPU
execution accelerates sampling and message passing roughly 5–10x.

## Methods
OGB `PygNodePropPredDataset` loading and evaluation; `GCNConv`, `SAGEConv`, and
`GATConv` layers; scalable training with `NeighborLoader`; `SIGN` transforms,
`k_hop_subgraph` analysis, conversion with `to_networkx`; embedding inspection
with TSNE; evaluation with confusion matrices, classification reports, and F1.
Data loading is tuned for 8 GB VRAM and a 16 GB RAM host (`num_neighbors`,
`num_workers=2–4`).

## Tech stack
Python 3.11, NumPy 2.2, pandas 2.3, scikit-learn, matplotlib, seaborn, networkx,
OGB, umap-learn, python-louvain, PyTorch (CUDA 13.0 wheels), torch-geometric,
pyg-lib (installed from the official PyG wheel index with a URL matched exactly
to the torch + CUDA version).

## Reproduce with conda

```bash
conda env create -f ex4/environment-ex4.yml
conda activate ggsn_ex4
pip install "torch==2.7.0" "torchvision==0.22.0" "torchaudio==2.7.0" --index-url https://download.pytorch.org/whl/cu128
pip install pyg-lib -f https://data.pyg.org/whl/torch-2.14.0+cu130.html
pip install -r ex4/requirements-lock-ex4.txt
python -m ipykernel install --user --name ggsn_ex4 --display-name "Python (ggsn_ex4)"
```

Verify with a forward pass on CUDA, including `pyg_lib`.

## Reproduce with Docker

```bash
cd ex4
docker build -t ex4:latest .
docker run --rm --gpus all -p 8888:8888 ex4:latest
```

## Skills demonstrated
- GNN architecture selection (GCN vs. GraphSAGE vs. GAT) and self-loop/degree handling.
- Scaling to large graphs with neighbor sampling and mini-batch loaders.
- Sourcing hardware-specific wheels (PyG index) with exact torch/CUDA version matching.
- Embedding analysis (TSNE/UMAP), community structure (Louvain), and OGB-standard evaluation.
