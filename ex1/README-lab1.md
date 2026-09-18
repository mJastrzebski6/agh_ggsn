# Lab 1 — Tabular Classification: Classical ML + Small MLP (CPU)

## Overview
Binary/multi-class classification on tabular data, comparing linear models, tree
ensembles, gradient boosting, and a small `tf.keras` MLP, with attention to class
imbalance and model explainability.

## Methods
Preprocessing with `SimpleImputer`, `StandardScaler`, and `LabelEncoder`;
stratified splits and cross-validation (`train_test_split`, `StratifiedKFold`,
`cross_val_score`, `GridSearchCV`); models including `LogisticRegression`,
`DecisionTree`, `RandomForest`, `GradientBoosting`, `LinearSVC`, `KNeighbors`,
and `XGBClassifier`; imbalance handling with `SMOTE` (`imbalanced-learn`);
a regularized MLP (`Dense / Dropout / BatchNormalization`, Adam/RMSprop/SGD);
evaluation with learning curves and confusion matrices; feature attribution with SHAP.

## Tech stack
Python 3.10, NumPy, pandas, scikit-learn, matplotlib, seaborn, XGBoost,
imbalanced-learn, SHAP, TensorFlow (CPU build), JupyterLab. Runs on CPU by design;
PyTorch is intentionally not part of this environment.

## Reproduce with conda

```bash
conda env create -f ex1/environment-ex1.yml
conda activate ggsn_ex1
pip install -r ex1/requirements-lock-ex1.txt
python -m ipykernel install --user --name ggsn_ex1 --display-name "Python (ggsn_ex1)"
jupyter lab
```

## Reproduce with Docker

```bash
cd ex1
docker build -t ex1:latest .
docker run --rm -p 8888:8888 ex1:latest
```

CPU-based image (`python:3.10-slim`); no GPU flags needed.

## Skills demonstrated
- Tabular preprocessing pipelines and leakage-safe validation design.
- Handling imbalanced classes (SMOTE, class weights, stratified CV).
- Hyperparameter search with `GridSearchCV` and model selection across model families.
- Comparing boosting, forests, linear models, and neural nets on equal footing.
- Explaining predictions with SHAP and communicating results with clear visualizations.
