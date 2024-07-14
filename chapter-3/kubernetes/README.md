# K8s
Reference: https://docs.haystack.deepset.ai/docs/kubernetes

## Setup
There has to be some basic requirements like:
- Docker: https://www.docker.com/products/docker-desktop/
- Kubectl (cli): https://kubernetes.io/docs/tasks/tools/
- Minikube or equivalent: https://minikube.sigs.k8s.io/docs/start/
- Add the pipelines directory and openai api key as environment variables using the command: `export HAYHOOKS_PIPELINES_DIR/OPENAI_API_KEY=""`

## About
As this chapter focusses on Scalable AI, we have already spoke about docker. But for much better control over the resources few prefer k8s. That's what is being covered in this directory. This contains all the configuration to deploy your pipeline to containers that runs in a cluster. For scalability there is lots of flexibility offered by kubernetes which will be discussed further.

## Configurations
- Configmap: Contain any non-confidential configuration data in key-value pairs to be consumed by Pods. In this case it contains the [serialized](https://docs.haystack.deepset.ai/docs/serialization) output of the pipeline in `yaml` format
- Deployment: Deals with the creation and scaling of a specified number of replicas of a Pod and ensures they are up and running
- Pod: The smallest deployable unit in Kubernetes, which encapsulates one or more containers, storage resources, and much more

## Execution
- Ensure successful installation of requirements:
- - `kubectl version`
- - `minikube version`
- - `docker version`
- Move to this current directory/level where this `README.md` is present.

- Ultimate goal for this walkthrough is to deploy the pipeline on kubernetes and ensure even when the demand rises its scalable enough through hayhooks instance.
<img width="1511" alt="Screenshot 2024-07-08 at 11 47 50 PM" src="https://gist.github.com/assets/81156510/70a89058-81a3-4770-9a4e-1492092636fe">

- Initially, create a new configmap: `kubectl create configmap pipelines --from-file=./configmap.yaml` This creates a indexing pipeline where it uses In Memory Document Store. Also, it embeds the document content using OpenAI text embedder.
<img width="1512" alt="Screenshot 2024-07-08 at 11 26 14 PM" src="https://gist.github.com/assets/81156510/bd2b02c3-6cb9-432c-bb97-59648851e12a">

- As a next step, we will create a new [pod](https://kubernetes.io/docs/concepts/workloads/pods/) with basic configuration of a container with hayhooks image and map it to the created configmap. This contains the volume to mount and container configuration with hayhooks instance as image. Command: `kubectl apply -f pod.yaml`
<img width="1512" alt="Screenshot 2024-07-08 at 10 39 11 PM" src="https://gist.github.com/assets/81156510/da60a5c5-2e69-4833-8379-e589e965226e">

- Last but not the least now that pods are configured, we shall deploy the with multiple pods: `kubectl apply -f deployment.yaml`.
We can scale the pods based on the usage either up or down. Then while mapping with the ConfigMap ensure both the names match each other. We can create multiple replicas of the same pod configuration and help us serve the user request if any of them fails.
<img width="1313" alt="Screenshot 2024-07-08 at 10 38 11 PM" src="https://gist.github.com/assets/81156510/68999d70-c610-48b4-87aa-5d28c7d7f706">
