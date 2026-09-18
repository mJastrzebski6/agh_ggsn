FROM python:3.11-slim
WORKDIR /app
COPY requirements-lock-ex4.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu130 --find-links https://data.pyg.org/whl/torch-2.14.0+cu130.html -r requirements-lock-ex4.txt
COPY . .
EXPOSE 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]