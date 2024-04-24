FROM deepset/haystack:base-v2.0.0-beta.7

RUN python3 -m venv /opt/venv

COPY ./requirements.txt .

RUN . /opt/venv/bin/activate

RUN apt-get update && apt-get install -y gcc python3-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

RUN export HAYSTACK_TELEMETRY_ENABLED=False

COPY ./first_rag_pipeline_haystack.py /usr/src/myapp/first_rag_pipeline_haystack.py

ENTRYPOINT ["python", "/usr/src/myapp/first_rag_pipeline_haystack.py"]
