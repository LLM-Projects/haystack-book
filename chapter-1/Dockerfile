FROM deepset/haystack:base-v2.0.0-beta.7

EXPOSE 1416

COPY ./requirements.txt .

RUN pip install -r ../requirements.txt

CMD ["hayhooks", "run", "--pipelines-dir", "/pipelines", "--host", "0.0.0.0"]
