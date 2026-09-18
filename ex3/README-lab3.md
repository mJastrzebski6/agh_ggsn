# Lab 3 — NLP: Recurrent Models + BERT Fine-Tuning (GPU)

## Overview
Text classification through two complementary tracks: recurrent/convolutional
baselines and transformer fine-tuning (DistilBERT, RoBERTa). GPU acceleration
(15–30x) makes the transformer track feasible.

## Methods
Classical track: Keras `Tokenizer`, padded sequences, `Embedding` followed by
`SimpleRNN / GRU / LSTM / Bidirectional / Conv1D` blocks, class weights via
`compute_class_weight`, callbacks (`ModelCheckpoint`, `EarlyStopping`,
`ReduceLROnPlateau`), word-cloud EDA, and accuracy/F1/precision/recall reporting.
Transformer track: Hugging Face `Trainer` / `TrainingArguments` with
`DataCollatorWithPadding`, `datasets` for data handling, and `evaluate` for metrics.

## Tech stack
Python 3.10, NumPy 1.26, pandas 2.3, scikit-learn, matplotlib, seaborn, wordcloud,
TensorFlow with CUDA support, PyTorch 2.7.0 + torchvision 0.22.0 + torchaudio 2.7.0
(CUDA 12.8 wheels), transformers 4.44, datasets 2.20, evaluate 0.4.2, accelerate 0.33.

## Reproduce with conda

PyTorch is installed separately from the official wheel index so its CUDA build
matches TensorFlow's (both CUDA 12 family):

```bash
conda env create -f ex3/environment-ex3.yml
conda activate ggsn_ex3
pip install "torch==2.7.0" "torchvision==0.22.0" "torchaudio==2.7.0" --index-url https://download.pytorch.org/whl/cu128
pip install -r ex3/requirements-lock-ex3.txt
python -m ipykernel install --user --name ggsn_ex3 --display-name "Python (ggsn_ex3)"
```

Verify both frameworks see the GPU:

```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

## Reproduce with Docker

```bash
cd ex3
docker build -t ex3:latest .
docker run --rm --gpus all -p 8888:8888 ex3:latest
```

## Skills demonstrated
- Sequence modeling progression from RNNs through LSTMs/GRUs to fine-tuned transformers.
- Handling text imbalance, padding/masking, and leak-free train/validation/test splits.
- Hugging Face training loop (`Trainer`, data collators, metric computation).
- Managing a dual-framework (TensorFlow + PyTorch) CUDA environment with pinned,
  mutually compatible builds and a generated lock file.
