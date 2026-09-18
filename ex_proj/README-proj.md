# Capstone Project — Text Classification: Baselines to BERT with Explainability (GPU)

## Overview
An end-to-end text-classification project: exploratory analysis, strong TF-IDF
baselines, a PyTorch MLP, and BERT fine-tuning, closed out with model explanations
and statistical comparison. GPU training speeds up the BERT track about 10x.

## Methods
EDA with class distributions and token statistics; `Pipeline`-based baselines
(`TfidfVectorizer` + `LinearSVC` / `DecisionTree` / `MultinomialNB`); a custom
torch `Dataset`/`DataLoader` MLP; fine-tuning via `AutoModelForSequenceClassification`
with `TrainingArguments`, `Trainer`, `DataCollatorWithPadding`, `accelerate`, and
`evaluate`; local explanations with LIME (`LimeTextExplainer`) and gradient
attribution with Captum (`LayerIntegratedGradients`); similarity and significance
analysis (`cosine_similarity`, Spearman, Mann–Whitney U); model persistence with joblib
and full seeding (`random` / NumPy / torch).

## Tech stack
Python 3.10, NumPy, pandas, scikit-learn, matplotlib, seaborn, NLTK, scikit-image,
LIME, Captum, SHAP, PyTorch 2.7.0 (CUDA 12.8 wheels), transformers, datasets,
evaluate, accelerate, sentencepiece, JupyterLab with widgets.

## Reproduce with conda

```bash
conda env create -f ex-proj/environment-ex-proj.yml
conda activate ggsn_proj
pip install "torch==2.7.0" "torchvision==0.22.0" --index-url https://download.pytorch.org/whl/cu128
pip install -r ex-proj/requirements-lock-proj.txt
python -m ipykernel install --user --name proj --display-name "proj"
jupyter lab
```

## Reproduce with Docker

```bash
cd ex-proj
docker build -t ex_proj:latest .
docker run --rm --gpus all -p 8888:8888 ex_proj:latest
```

## Skills demonstrated
- Project design: honest baselines before deep models, clean train/validation/test
  protocol, seeded and logged experiments with persisted artifacts.
- Modern NLP stack: Hugging Face training, data collation, and metric-driven tuning.
- Explainable ML: contrasting perturbation-based (LIME) and gradient-based (Captum)
  explanations, plus statistical testing of model differences.
- Release engineering for ML: minimal conda recipe + generated lock file + Docker
  image, so the full project rebuilds identically on CPU or GPU machines.
