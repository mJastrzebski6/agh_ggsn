#!/usr/bin/env python3
"""Generuje prezentację PPTX z wyników projektu rozpoznawania emocji."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

PLOTS_DIR = "plots"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

SLIDE_W = Inches(13.333)

CLR_BG = RGBColor(0xF5, 0xF5, 0xF0)
CLR_TITLE = RGBColor(0x1A, 0x1A, 0x2E)
CLR_BODY = RGBColor(0x2C, 0x3E, 0x50)
CLR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CLR_ACCENT = RGBColor(0x29, 0x80, 0xB9)
CLR_GREEN = RGBColor(0x27, 0xAE, 0x60)

def add_bg(slide, color=CLR_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape_bg(slide, left, top, width, height, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18, bold=False, color=CLR_BODY, alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_bullet_slide(slide, left, top, width, height, items, font_size=16, color=CLR_BODY):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.space_after = Pt(4)
    return txBox

def add_table(slide, left, top, width, height, data, col_widths=None, font_size=11, header_color=CLR_ACCENT):
    rows, cols = len(data), len(data[0])
    ts = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = ts.table
    for ci in range(cols):
        if col_widths and ci < len(col_widths):
            table.columns[ci].width = col_widths[ci]
    for ri, row_data in enumerate(data):
        for ci, cell_text in enumerate(row_data):
            cell = table.cell(ri, ci)
            cell.text = str(cell_text)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(font_size)
                p.font.name = "Calibri"
                p.alignment = PP_ALIGN.CENTER
                if ri == 0:
                    p.font.bold = True
                    p.font.color.rgb = CLR_WHITE
                else:
                    p.font.color.rgb = CLR_BODY
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if ri == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_color
            elif ri % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xEB, 0xF5, 0xFB)
    return ts

def add_title_bar(slide, text):
    add_shape_bg(slide, Inches(0), Inches(0.2), SLIDE_W, Inches(0.9), CLR_TITLE)
    add_text_box(slide, Inches(0.5), Inches(0.3), Inches(12), Inches(0.7), text, font_size=28, bold=True, color=CLR_WHITE)

# SLAJD 1: Tytuł
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, CLR_TITLE)
add_shape_bg(slide, Inches(0), Inches(2.5), SLIDE_W, Inches(3.2), RGBColor(0x1A, 0x1A, 0x2E))
add_text_box(slide, Inches(0.5), Inches(1.0), Inches(12), Inches(1.5), "Rozpoznawanie Emocji z Tekstu", font_size=44, bold=True, color=CLR_WHITE, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.5), Inches(2.6), Inches(12), Inches(1.0), "Klasyczne ML · RNN · Transformery · XAI", font_size=28, color=RGBColor(0xEB, 0xF5, 0xFB), alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.5), Inches(3.8), Inches(12), Inches(0.8), "Gniew · Radość · Smutek · Strach — porównanie na 3 zbiorach danych", font_size=20, color=RGBColor(0x85, 0xC1, 0xE9), alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.5), Inches(6.0), Inches(12), Inches(0.5), "Raport projektu · Maj 2026", font_size=16, color=RGBColor(0x7F, 0x8C, 0x8D), alignment=PP_ALIGN.CENTER)

# SLAJD 2: Cele
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Cele Projektu")
add_bullet_slide(slide, Inches(0.8), Inches(1.5), Inches(11.5), Inches(5.5), [
    "Zbudowanie i porównanie modeli klasyfikacji emocji 3 podejściami: klasyczne ML, RNN, Transformery",
    "4 docelowe emocje: gniew (anger), radość (joy), smutek (sadness), strach (fear)",
    "Ewaluacja na 3 zbiorach danych: Combined (60k zbalansowanych), ISEAR (4.3k), GoEmotions (11k)",
    "Analiza generalizacji modeli na danych spoza domeny uczącej",
    "Zastosowanie technik XAI (LIME, Integrated Gradients) do interpretacji modeli",
    "Wybór najlepszego modelu z uwzględnieniem dokładności, generalizacji i wyjaśnialności"
], font_size=18)

# SLAJD 3: Zbiory danych
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Zbiory Danych")
add_table(slide, Inches(0.5), Inches(1.5), Inches(12.3), Inches(2.5), [
    ["Zbiór", "Próbki ogółem", "Gniew", "Radość", "Smutek", "Strach", "Źródło"],
    ["Combined", "60 000", "15 000", "15 000", "15 000", "15 000", "kushagra3204/sentiment-and-emotion"],
    ["ISEAR", "4 284", "1 078", "1 080", "1 054", "1 072", "faisalsanto007/isear-dataset"],
    ["GoEmotions", "11 092", "3 833", "3 317", "2 757", "1 185", "debarshichanda/goemotions"],
], col_widths=[Inches(1.8), Inches(1.5), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2), Inches(4.5)], font_size=13)
add_bullet_slide(slide, Inches(0.8), Inches(4.2), Inches(11.5), Inches(3.0), [
    "Combined: 6-emocji (422k zdań), przefiltrowany do 4 emocji, zbalansowany do 60k (15k/klasę)",
    "ISEAR: dane z kwestionariuszy psychologicznych, naturalnie zbalansowane",
    "GoEmotions: komentarze z Reddita, niezbalansowane — strach niedoreprezentowany (1 185), gniew dominujący (3 833)",
], font_size=16)

# SLAJD 4: Rozkład danych
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Rozkład Danych")
dist_path = os.path.join(PLOTS_DIR, "dataset_distributions.png")
if os.path.exists(dist_path):
    slide.shapes.add_picture(dist_path, Inches(0.3), Inches(1.5), Inches(12.7), Inches(3.5))
add_bullet_slide(slide, Inches(0.8), Inches(5.2), Inches(11.5), Inches(2.0), [
    "Combined (zbiór treningowy): idealnie zbalansowany (42k po podziale)",
    "ISEAR: prawie zbalansowany (1 054–1 080 na klasę)",
    "GoEmotions: niezbalansowany — strach ma tylko 1 185 próbek vs 3 833 gniewu",
    "Podział train/val/test: 70/15/15% stratyfikowany według klasy"
], font_size=16)

# SLAJD 5: Metodologia
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Metodologia i Modele")
add_bullet_slide(slide, Inches(0.5), Inches(1.3), Inches(12.3), Inches(6.0), [
    "Klasyczne ML (TF-IDF + Klasyfikator):",
    "  • SVM (LinearSVC, class_weight='balanced')",
    "  • Drzewo Decyzyjne (DecisionTree, max_depth=50)",
    "  • Naiwny Bayes (NaiveBayes, MultinomialNB)",
    "",
    "Sieci Rekurencyjne (BiRNN):",
    "  • BiLSTM — 2-warstwowy dwukierunkowy LSTM",
    "  • BiGRU — 2-warstwowy dwukierunkowy GRU",
    "  • Embedding dim=128, Hidden dim=128",
    "",
    "Fine-tuned Transformery (HuggingFace Trainer):",
    "  • Own-DistilBERT (distilbert-base-uncased)",
    "  • Own-DistilRoBERTa (distilroberta-base)",
    "",
    "Gotowe modele emocji z HF:",
    "  • Emotion-BERT (bhadresh-savani/bert-base-uncased-emotion)",
    "  • Emotion-RoBERTa (SamLowe/roberta-base-go_emotions)",
    "",
    "XAI: LIME (modele klasyczne + transformery), Integrated Gradients (RNN)",
], font_size=16)

# SLAJD 6: Wyniki
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Wyniki — Macro F1 na wszystkich zbiorach")
tbl_data = [
    ["Model", "Combined_test", "ISEAR", "GoEmotions", "Średnia"],
    ["Own-DistilBERT", "0.9810", "0.7409", "0.5937", "0.7719"],
    ["Own-DistilRoBERTa", "0.9808", "0.6941", "0.5479", "0.7409"],
    ["BiLSTM", "0.9766", "0.4065", "0.3714", "0.5848"],
    ["BiGRU", "0.9758", "0.5230", "0.3750", "0.6246"],
    ["Emotion-BERT", "0.9730", "0.7089", "0.5799", "0.7539"],
    ["SVM", "0.9513", "0.6132", "0.4156", "0.6600"],
    ["NaiveBayes", "0.9138", "0.5998", "0.4563", "0.6566"],
    ["Emotion-RoBERTa", "0.5804", "0.6421", "0.7814", "0.6680"],
    ["DecisionTree", "0.5157", "0.2839", "0.1980", "0.3325"],
]
ts = add_table(slide, Inches(0.5), Inches(1.4), Inches(10.5), Inches(5.0), tbl_data, col_widths=[Inches(2.5), Inches(2.0), Inches(2.0), Inches(2.0), Inches(2.0)], font_size=14)
for ri in range(1, len(tbl_data)):
    for ci in [1, 2, 3]:
        cell = ts.table.cell(ri, ci)
        val = float(tbl_data[ri][ci])
        if val >= 0.90:
            cell.fill.solid()
            cell.fill.fore_color.rgb = CLR_GREEN
            for p in cell.text_frame.paragraphs:
                p.font.color.rgb = CLR_WHITE; p.font.bold = True
        elif val >= 0.70:
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0x2E, 0xCC, 0x71)
            for p in cell.text_frame.paragraphs:
                p.font.color.rgb = CLR_WHITE
add_text_box(slide, Inches(0.5), Inches(6.5), Inches(12), Inches(0.5),
             "Zielone = wysoka skuteczność. Own-DistilBERT najlepszy ogólnie (średnie macro F1 = 0.7719)",
             font_size=14, color=CLR_GREEN, bold=True)

# SLAJD 7: Najlepszy model
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Najlepszy Model: Own-DistilBERT — Szczegółowa Analiza")
add_table(slide, Inches(0.5), Inches(1.3), Inches(12.0), Inches(2.0), [
    ["Zbiór", "Gniew", "Strach", "Radość", "Smutek", "Średnie F1"],
    ["Combined_test", "0.9718", "0.9761", "0.9929", "0.9832", "0.9810"],
    ["ISEAR", "0.7169", "0.8006", "0.7648", "0.6816", "0.7409"],
    ["GoEmotions", "0.6631", "0.4422", "0.7168", "0.5528", "0.5937"],
], col_widths=[Inches(2.5), Inches(2.0), Inches(2.0), Inches(2.0), Inches(2.0), Inches(1.5)], font_size=14)
add_bullet_slide(slide, Inches(0.8), Inches(3.5), Inches(11.5), Inches(3.5), [
    "Own-DistilBERT: fine-tuned distilbert-base-uncased (67M parametrów) na 42k próbek Combined",
    "Najlepszy w domenie (Combined_test): 0.9810 macro F1 — klasyfikacja niemal idealna",
    "Dobra generalizacja na ISEAR (0.7409) — bardziej formalny, psychologiczny język",
    "Umiarkowana na GoEmotions (0.5937) — nieformalny tekst z Reddita, inny rozkład",
    "Strach najtrudniejszą klasą na GoEmotions (0.4422) — przez niezbalansowanie zbioru",
    "Konfiguracja: 3 epoki, batch_size=16, lr=2e-5, max_len=64, fp16"
], font_size=16)

# SLAJD 8: Porównanie
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Porównanie Modeli — Wnioski")
add_bullet_slide(slide, Inches(0.5), Inches(1.3), Inches(12.3), Inches(6.0), [
    "W domenie (Combined_test):",
    "  • Wszystkie Transformery + RNN >0.97 macro F1 — nasycenie na danych wewnątrz domeny",
    "  • SVM i NaiveBayes też mocne (0.95, 0.91) przy dużo niższym koszcie treningu",
    "  • DecisionTree bardzo słaby (0.52) — niewystarczająca głębokość dla tekstu",
    "",
    "Poza domeną — ISEAR (tekst psychologiczny):",
    "  • Own-DistilBERT (0.74) i Emotion-BERT (0.71) generalizują najlepiej",
    "  • BiLSTM spada do 0.41 — przetrenowany na dystrybucji Combined",
    "",
    "Poza domeną — GoEmotions (Reddit):",
    "  • Emotion-RoBERTa (0.78) najlepszy — był pretrenowany na GoEmotions!",
    "  • Own-DistilBERT (0.59) i Emotion-BERT (0.58) w następnej kolejności",
    "  • Modele klasyczne i RNN spadają poniżej 0.46 — różnice słownictwa szkodzą TF-IDF"
], font_size=16)

# SLAJD 9: Krzywe uczenia
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Krzywe Uczenia — Transformery")
curves_path = os.path.join(PLOTS_DIR, "training_curves.png")
if os.path.exists(curves_path):
    slide.shapes.add_picture(curves_path, Inches(0.5), Inches(1.4), Inches(12.3), Inches(4.5))
    add_bullet_slide(slide, Inches(0.8), Inches(6.0), Inches(11.5), Inches(1.3), [
        "Own-DistilBERT osiągnął ~0.98 walidacyjnego macro F1 po 3 epokach",
        "Own-DistilRoBERTa nieznacznie niższy — różnice w tokenizerze/słownictwie"
    ], font_size=16)
else:
    add_bullet_slide(slide, Inches(0.8), Inches(2.5), Inches(11.5), Inches(3.0), [
        "Krzywe uczenia niedostępne (checkpoints/ musi zawierać trainer_state.json)",
        "Oba modele zbiegły dobrze w ciągu 3 epok z walidacyjnym macro F1 ~0.98"
    ], font_size=18)

# SLAJD 10: Macierze pomyłek
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Macierze Pomyłek — Najlepszy Model")
grid_path = os.path.join(PLOTS_DIR, "confusion_matrix_grid.png")
if os.path.exists(grid_path):
    slide.shapes.add_picture(grid_path, Inches(0.3), Inches(1.3), Inches(12.7), Inches(5.8))
else:
    add_bullet_slide(slide, Inches(0.8), Inches(2.0), Inches(11.5), Inches(4.0), [
        "Macierz pomyłek niedostępna (uruchom notebook by wygenerować plots/)",
        "Own-DistilBERT na Combined_test: macierz prawie diagonalna (0.97-0.99 F1 na klasę)",
        "Own-DistilBERT na ISEAR: gniew/strach dobrze separowane, radość/smutek umiarkowane pomyłki",
        "Own-DistilBERT na GoEmotions: znaczące pomyłki poza przekątną, zwłaszcza strach mylony z gniewem"
    ], font_size=18)

# SLAJD 11: XAI
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "XAI — Analiza Wyjaśnialności Modeli")
add_bullet_slide(slide, Inches(0.5), Inches(1.3), Inches(12.3), Inches(6.0), [
    "LIME (Local Interpretable Model-agnostic Explanations):",
    "  • Zastosowany do klasycznych ML (NaiveBayes, DecisionTree) i transformerów",
    "  • Wskazuje poszczególne tokeny wpływające na predykcję",
    "  • Oblicza ważność cech przez perturbację tekstu wejściowego",
    "",
    "Integrated Gradients (Captum):",
    "  • Zastosowany do BiLSTM i BiGRU przez atrybucję warstwy embeddingu",
    "  • Przypisuje wagi ważności każdemu tokenowi wejściowemu",
    "  • Metoda oparta na gradientach z porównaniem do baseline'u",
    "",
    "Analiza podobieństwa XAI (Jaccard, Spearman, Cosine):",
    "  • BiGRU vs BiLSTM: najwyższa zgodność (cosine=0.86, jaccard=0.69) — podobna architektura RNN",
    "  • LIME_Own-DistilBERT vs LIME_Own-DistilRoBERTa: wysoka zgodność (cosine=0.93) — podobne attention",
    "  • DecisionTree vs wszystkie: najniższa zgodność — fundamentalnie inny proces decyzyjny",
    "  • RNN i Transformery wykazują umiarkowaną korelację: oba chwytają podobne wzorce językowe"
], font_size=15)

# SLAJD 12: XAI tokeny
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "XAI — Najważniejsze Tokeny (Przykład)")
xai_files = []
if os.path.isdir(PLOTS_DIR):
    xai_files = sorted([f for f in os.listdir(PLOTS_DIR) if f.startswith("xai_") and f.endswith(".png")])
if xai_files:
    for i, fname in enumerate(xai_files[:6]):
        idx = i % 3; row = i // 3
        x_pos = Inches(0.3) + idx * Inches(4.3)
        y_pos = Inches(1.5) + row * Inches(2.8)
        fpath = os.path.join(PLOTS_DIR, fname)
        try:
            slide.shapes.add_picture(fpath, x_pos, y_pos, Inches(4.1), Inches(2.5))
        except: pass
        add_text_box(slide, x_pos, y_pos + Inches(2.55), Inches(4.1), Inches(0.3),
                     fname.replace("xai_", "").replace(".png", ""), font_size=10, color=CLR_BODY, alignment=PP_ALIGN.CENTER)
    add_bullet_slide(slide, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.9), [
        "LIME: najważniejsze tokeny to zwykle słowa nacechowane emocjonalnie (np. 'love', 'hate', 'cried', 'scared')",
        "Integrated Gradients: skupia się na słowach kluczowych emocji i przeczeniach",
        "Transformery pokazują bardziej rozproszoną uwagę między tokenami niż modele klasyczne",
    ], font_size=13)
else:
    add_bullet_slide(slide, Inches(0.8), Inches(2.0), Inches(11.5), Inches(4.0), [
        "Wykresy XAI niedostępne (uruchom notebook by wygenerować plots/)",
        "LIME: najważniejsze tokeny to zwykle słowa nacechowane emocjonalnie",
        "Integrated Gradients: skupia się na słowach kluczowych emocji i przeczeniach",
        "Transformery pokazują bardziej rozproszoną uwagę między tokenami niż modele klasyczne"
    ], font_size=18)

# SLAJD 13: Wnioski
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Wnioski")
add_table(slide, Inches(0.5), Inches(1.3), Inches(11.5), Inches(3.0), [
    ["Model", "Combined_test", "ISEAR", "GoEmotions", "Najlepszy do"],
    ["Own-DistilBERT", "0.9810", "0.7409", "0.5937", "Ogólnie najlepsza generalizacja"],
    ["Emotion-BERT", "0.9730", "0.7089", "0.5799", "Zero-shot bez fine-tuningu"],
    ["Emotion-RoBERTa", "0.5804", "0.6421", "0.7814", "Specjalista GoEmotions"],
    ["SVM + TF-IDF", "0.9513", "0.6132", "0.4156", "Szybki, interpretowalny baseline"],
    ["BiGRU", "0.9758", "0.5230", "0.3750", "Tylko w domenie"],
], col_widths=[Inches(2.5), Inches(2.0), Inches(2.0), Inches(2.0), Inches(3.0)], font_size=14)
add_bullet_slide(slide, Inches(0.5), Inches(4.5), Inches(12.3), Inches(2.8), [
    "Own-DistilBERT (fine-tuned) zapewnia najlepszy balans dokładności i generalizacji między domenami",
    "Gotowy Emotion-BERT działa dobrze zero-shot bez fine-tuningu na docelowych danych",
    "Klasyczne ML (SVM) jest zaskakująco konkurencyjne w domenie i na formalnym tekście (ISEAR)",
    "Generalizacja między domenami pozostaje kluczowym wyzwaniem — zwłaszcza z tekstu formalnego na social media",
    "RNN (BiLSTM, BiGRU) działają dobrze w domenie, ale przetrenowują się i nie przenoszą na inne domeny",
    "XAI ujawnia, że różne rodziny modeli skupiają się na podobnych słowach kluczowych emocji"
], font_size=16)

# SLAJD 14: Bibliografia
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Bibliografia")
add_bullet_slide(slide, Inches(0.5), Inches(1.3), Inches(12.3), Inches(6.0), [
    "Zbiory danych:",
    "  • Combined: kaggle.com/datasets/kushagra3204/sentiment-and-emotion-analysis-dataset",
    "  • ISEAR: kaggle.com/datasets/faisalsanto007/isear-dataset",
    "  • GoEmotions: kaggle.com/datasets/debarshichanda/goemotions",
    "",
    "Modele pretrenowane (HuggingFace):",
    "  • Emotion-RoBERTa: SamLowe/roberta-base-go_emotions",
    "  • Emotion-BERT: bhadresh-savani/bert-base-uncased-emotion",
    "  • DistilBERT: distilbert-base-uncased",
    "  • DistilRoBERTa: distilroberta-base",
    "",
    "Biblioteki: scikit-learn, PyTorch, HuggingFace Transformers, Captum, LIME, matplotlib, seaborn",
], font_size=16)

output_path = "reports/Emotion_Recognition_Prezentacja.pptx"
os.makedirs("reports", exist_ok=True)
prs.save(output_path)
print(f"Prezentacja zapisana do: {output_path}")
print(f"Liczba slajdów: {len(prs.slides)}")