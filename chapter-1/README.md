# First RAG Pipeline
Creating Your First QA Pipeline with Retrieval-Augmentation On Custom Documents Using Haystack

This notebook primarily focusses on utilising Haystack for building a QA Piepline using RAG on Custom documents and uses Haystack v2.0(latest as of the time the book is written).

Learn how to create a RAG pipeline based on custom documents and answer questions based on this.

## Installation
Install all the requirements using `pip`. Use the command.
```bash
pip install -r requirements.txt
```

## Building Document Store
Then create the custom document store by fetching data. Document store is a place where you store multiple documents under a common name. A [document](https://docs.haystack.deepset.ai/docs/data-classes#document) is a individual unit that can hold data of text, image, json, and more with or with metadata.

An [document store](https://docs.haystack.deepset.ai/docs/document-store) is an indexed verison of your documents. It acts like database for your pipeline components to retrieve documents using [retrievers](https://docs.haystack.deepset.ai/docs/retrievers).

For our case we are considering the [InMemoryDocumentStore](https://docs.haystack.deepset.ai/docs/choosing-a-document-store#the-in-memory-document-store) document store that comes out of the box with `haystack`. This is the mostly preferred for small datasets and demo purposes. Haystack offers [various document stores](https://docs.haystack.deepset.ai/docs/choosing-a-document-store#summary) to choose from.

Now fetch the data from [PoetryDB](https://poetrydb.org/) API to obtain William Shakespeare poems. The response is JSON. TNext, convert the json object into individual chunks of documents.
Finally we write the `documents` into the document store and check the total number of documents that have been added.


## Pipeline
The various steps involved in building RAG Pipeline are:

![RAG Piepline](https://gist.github.com/assets/81156510/aa1c18a7-0ae5-4875-8999-a0fb228bdad7)

- Retrievers
- Prompt Template
- Generator

### Retrievers
Used to retrieve documents that closely match the input query. This example uses the InMemoryBM25Retriever, which uses keyword based matching according to the [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25). Additional parameters like search `filters` to reduce the search base, `top_k` list down the `k` document(s) default is 10 and `scale_score` if set to `true` can be used to set similarity scores in the range [0,1].

### Prompt Template
Now that we are building a QA RAG Pipeline there needs to be a prompt that would be fed into the LLM Generator, to be discussed next. Hence we, make use of [PromptBuilder](https://docs.haystack.deepset.ai/docs/promptbuilder). The template is built from [jinja2](https://palletsprojects.com/p/jinja/). It takes inputs as keyword arguments. These will be replaced with actual values gathered during pipeline execution.

Pass the query that's collected from the user into the generator.

### Generator
Next is to [generate](https://docs.haystack.deepset.ai/docs/generators) content. This is primarily used to answer the queries of the user. For our current use case we utilize the [`OpenAIGenerator`](https://docs.haystack.deepset.ai/docs/openaigenerator). Make sure to get OPENAI_API_KEY from [here](https://platform.openai.com).

This makes use of models gpt-3.5-turbo(default) and gpt-4 families. It takes a mandatory parameters like api key, `prompt` as `str`, and other optional parameters like [`generation_kwargs`](https://github.com/deepset-ai/haystack/blob/main/haystack/components/generators/openai.py#L71) which takes model parameters like `max_tokens`, `temperature`, `top_p`, `n`, `stop`, `presence_penalty`, `frequency_penalty`, and `logit_bias`. These are mostly left to default but the first 4 are widely used parameters amongst all of them. We are free to choose from other available generators that best choose your use case or stack.

Finally, you are ready to build the Pipeline by combining all the previous components together.

### What is a Haystack Pipeline?
A pipeline is a wrapper that contains multiple components connected together and hids the internal functionality from the user just exposing the input and the output data.
In haystack terms, Pipeline is defined as:
> The pipelines in Haystack 2.0 are directed [multigraphs](https://en.wikipedia.org/wiki/Multigraph) of different Haystack components and integrations.
We can achieve branching, looping, which speeds up the execution of the tasks. Through branching we achieve parallelism which in turn improves concurrency.

Then through loops we can iterate to the same pipeline again based on the past computation which improves the result, or captures errors until the loop is executed.

We can add multiple components using the `pipeline_name.add_component()` with 2 arguments namely: name of the component to be aliased inside pipeline, the actual pipeline component. There on we will use the alias name to address the component. One can find all possible list of components in the haystack [documentation](https://docs.haystack.deepset.ai/docs/) on the left side panel under the heading **PIPELINE COMPONENTS**.

Connect components using the `pipeline_name.connect()` method that takes 2 parameters i.e. input and output component respectively. We also pass the respective inputs and this method will validate if the types of input and output match the given connection.

We can infer the same from the pipeline graph. One key thing to notice is the lines that connects various components. Dotted lines represent it's not mandatory to pass the tail component to the head component. A solid line represents a mandatory connection where any issue in the tail component breaks the entire pipeline flow thereby hindering `pipeline.run()`.

## Executing RAG Pipeline
Run `pipeline_name.run()` to execute the pipeline. It takes a `data` as a dictionary that needs to be passed to the component(s) as input. Setting `debug` to true can be used to track pipeline execution and flag errors. The output response is returned as a dictionary.
