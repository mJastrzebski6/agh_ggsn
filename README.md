# Machine Learning Labs — Reproducible Environments (WSL2 + RTX 4060)

Four machine-learning lab assignments plus a capstone project, each with its own
minimal, reproducible environment. Developed on Windows + WSL2 (Ubuntu) with an
RTX 4060 8 GB.

## Results

The results of all cells were not cleared and are saved in the ipynb files.


## Engineering practices applied

- **One minimal environment per task.** Each recipe contains only what its notebook
  imports; nothing is shared or installed "just in case".
- **Pinned, generated locks.** All pins come from `pip freeze` after a verified GPU
  test run, so rebuilds are byte-identical.
- **CUDA consistency.** TensorFlow (`tensorflow[and-cuda]`, cu12 family) and PyTorch
  (cu128 / cu130 wheel index) are kept on matching CUDA builds with pinned
  `torch / torchvision / torchaudio` triples, avoiding mixed `cu12/cu13` states.
- **WSL2 GPU support.** TensorFlow GPU visibility is ensured via the `[and-cuda]`
  extra plus `LD_LIBRARY_PATH` entries for the pip-installed NVIDIA libraries,
  configured persistently through conda `activate.d` scripts.
- **PyTorch Geometric sourcing.** `pyg-lib` wheels come from the official PyG wheel
  index with a URL matched exactly to the installed torch + CUDA version.
- **Jupyter integration.** Every environment registers its own kernel
  (`python -m ipykernel install --user --name labX`).

GPU sanity check (WSL):

```bash
nvidia-smi
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
docker run --rm --gpus all nvidia/cuda:12.6.0-base-ubuntu22.04 nvidia-smi
```

See `README-lab1.md` … `README-proj.md` for per-task details.

## Repository layout

```
ex1/  Notebook, environment-ex1.yml, requirements-lock-ex1.txt, Dockerfile, README-ex1.md
ex2/  Notebook, environment-ex2.yml, requirements-lock-ex2.txt, Dockerfile, README-ex2.md
ex3/  Notebook, environment-ex3.yml, requirements-lock-ex3.txt, Dockerfile, README-ex3.md
ex4/  Notebook, environment-ex4.yml, requirements-lock-ex4.txt, Dockerfile, README-ex4.md
proj/  Notebook, environment-ex-proj.yml,  requirements-lock-proj.txt,  Dockerfile, README-proj.md
```

Reproducibility design (identical in every lab):
- `environment-*.yml` — a short, hand-written conda recipe: Python plus only the
  top-level packages the notebook actually imports.
- `requirements-lock-*.txt` — a fully pinned lock file generated with `pip freeze`.
  This is the exact input used to rebuild the environment and to build the Docker image.
- `Dockerfile` — a production image following the same recipe, so anyone can run the
  work without conda.

## Compute strategy

| Lab | Topic | Mode | Rationale |
|---|---|---|---|
| ex1 | Tabular classification, gradient boosting, small MLP, SHAP | CPU | Small tabular models; GPU offers no meaningful speedup. PyTorch intentionally excluded. |
| ex2 | Image classification, CNN transfer learning (VGG16, ResNet50, MobileNetV2, EfficientNetB0) | GPU | Roughly 10–20x faster than CPU training. |
| ex3 | Text classification, RNN/LSTM/GRU + DistilBERT/RoBERTa fine-tuning | GPU | 15–30x faster; transformer fine-tuning is impractical on CPU. |
| ex4 | Graph neural networks (GCN/SAGE/GAT on OGB) | GPU | 5–10x faster neighbor sampling and message passing. |
| proj | Text classification: TF-IDF baselines + MLP + BERT + LIME/Captum | GPU | About 10x faster BERT training and explanation. |

## Reproduce any lab

### Option A — conda (development)

```bash
conda env create -f ex2/environment_ex2.yml
conda activate ggsn_ex2
pip install -r ex2/requirements-lock-ex2.txt
jupyter lab
```

Notes for labs 3 and 4: PyTorch is installed in a separate step from the official
PyTorch wheel index so that its CUDA build matches the rest of the stack
(see `README-lab3.md` and `README-lab4.md` for the exact commands).

### Option B — Docker (sharing / production)

```bash
cd ex2
docker build -t ex2:latest .
docker run --rm -p 8888:8888 ex2:latest            # CPU
docker run --rm --gpus all -p 8888:8888 ex2:latest # GPU
```

CUDA drivers live on the host only; the image ships just the user-space CUDA
libraries (pip `nvidia-*` packages / `nvidia/cuda` runtime base). The same image
runs on CPU-only machines (omit `--gpus all`) — TensorFlow and PyTorch fall back
to CPU automatically.


