# Lab 2 — Image Classification: CNN Transfer Learning (GPU)

## Overview
Image classification with transfer learning on 224×224 inputs, comparing
VGG16, ResNet50, MobileNetV2, and EfficientNetB0 as frozen backbones with a
task-specific head. GPU training is roughly 10–20x faster than CPU.

## Methods
Per-architecture `preprocess_input` from `tf.keras.applications`; data augmentation
and batching with `ImageDataGenerator` and OpenCV preprocessing; training with
`EarlyStopping`, `ReduceLROnPlateau`, `ModelCheckpoint`, and `CSVLogger`;
evaluation with confusion matrices and classification reports; matplotlib/seaborn
diagnostics of overfitting via train/validation curves.

## Tech stack
Python 3.10, NumPy, pandas, scikit-learn, matplotlib, seaborn, tqdm, Pillow,
opencv-python, scikit-image, TensorFlow with CUDA support (`tensorflow[and-cuda]`),
JupyterLab.

## Reproduce with conda

```bash
conda env create -f ex2/environment-ex2.yml
conda activate ggsn_ex2
pip install -r ex2/requirements-lock-ex2.txt
python -m ipykernel install --user --name ggsn_ex2 --display-name "Python (ggsn_ex2)"
jupyter lab
```

Verify GPU visibility:

```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

## Reproduce with Docker

```bash
cd ex
docker build -t ex2:latest .
docker run --rm --gpus all -p 8888:8888 ex2:latest
```

GPU-based image (`nvidia/cuda` runtime + pip). Without `--gpus all` the same image
falls back to CPU.

## Skills demonstrated
- Selecting architectures against a compute budget (lightweight MobileNet/EfficientNet
  vs. heavier ResNet/VGG).
- Correct backbone-specific preprocessing and head design for transfer learning.
- Augmentation, learning-rate scheduling, checkpointing, and early stopping.
- Reproducible GPU setup for TensorFlow on WSL2, including CUDA library wiring
  (`[and-cuda]` extra + persistent `LD_LIBRARY_PATH` configuration).
