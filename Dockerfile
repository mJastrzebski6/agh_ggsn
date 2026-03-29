FROM mambaorg/micromamba:latest

WORKDIR /app

COPY --chown=$MAMBA_USER:$MAMBA_USER environment_cuda.yml /tmp/environment_cuda.yml

RUN micromamba install -y -n base -f /tmp/environment_cuda.yml && \
    micromamba clean --all --yes

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]