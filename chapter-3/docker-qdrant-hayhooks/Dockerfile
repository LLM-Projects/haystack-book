FROM deepset/haystack:base-v2.1.1

EXPOSE 1416

RUN pip install qdrant-haystack hayhooks sentence-transformers
RUN pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu

CMD ["hayhooks", "run", "--pipelines-dir", "/pipelines", "--host", "0.0.0.0"]
