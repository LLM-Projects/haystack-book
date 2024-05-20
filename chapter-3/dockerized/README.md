## Deployment using [Docker](https://docs.haystack.deepset.ai/v2.0/docs/docker)

### Basic Docker Container
The basic form of Haystack deployment occurs through Docker containers. Haystack releases are available publically as a ready to pull docker image named `deepset:haystack` in the docker [hub](https://hub.docker.com/r/deepset/haystack).

We can pull the latest image through the command:

```bash
docker pull deepset/haystack
```

The above commnand pulls the same dependencies and version which we get by installing through `pip install haystack-ai`.
If we need the specific version we can install that image through the command:

```bash
docker pull deepset/haystack:base-v2.0.0-beta.7
```

#### Fine tune the image
Let's consider the First RAG Pipeline from Chapter-1. Now, lets see how we can deploy that image using docker. Create a file named `Dockerfile`. Then we must have `requirements.txt` that can be copied from the root of the repository. Then a `.py` version of the first rag pipeline notebook that can be found within the same directory.

The `Dockerfile` file contains the configuration of the docker container that needs to be created. Contents of that file can be found below:

```shell
FROM deepset/haystack:base-v2.0.0-beta.7

RUN python3 -m venv /opt/venv

COPY ../requirements.txt .

RUN . /opt/venv/bin/activate

RUN apt-get update && apt-get install -y gcc python3-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install -r ./requirements.txt

RUN export HAYSTACK_TELEMETRY_ENABLED=False

COPY ./first_rag_pipeline_haystack.py /usr/src/myapp/first_rag_pipeline_haystack.py

ENTRYPOINT ["python", "/usr/src/myapp/first_rag_pipeline_haystack.py"]
```

Lets breakdown code snippet:
- We intially pull the specific haystack docker image from docker hub.
- Then we are creating the virtual environment.
- This virtual environment needs to be activated.
- We are ensuring the latest version of the linux instance, python, and cleaning the local repository of package files.
- The we install the required dependencies needed to run the file.
- We disable the default OpenTelemetry tracking provided by Haystack.
- Copy the first rag pipeline file to the container instace.
- Finally, run the pipeline from the command line and ask the query.

Now that we have all set up. Let's build from the docker image using the `build` command:

```bash
docker build . -t <image_name>
```

This will take some time. We can verify the same using the command:

```bash
docker images
```

![docker images list](https://github.com/LLM-Projects/haystack-book/assets/81156510/d2afe380-25f7-44fc-a5e5-ecea3a408cea)

Then after this has been executed successfully we can run the docker image using the command:

```bash
docker run -it --rm <image_id>
```

This enables a interactive terminal where we can view the output of the file.
![docker interactive terminal](https://github.com/LLM-Projects/haystack-book/assets/81156510/0f87b565-edb6-41a7-82dc-1d47b6c942da)

<!-- ### Complex Application with Docker Deployment -->
