# First RAG Pipeline
Creating Your First QA Pipeline with Retrieval-Augmentation On Custom Documents Using Haystack

This notebook primarily focusses on utilising Haystack for building a QA Piepline using RAG on Custom documents. This notebook makes use of Haystack v2.0(latest as of the time the book is written).

We are running a RAG pipeline on the custom documents (gathered from API source) and answer questions on the same.

## Installation
Install all the requirements using `pip`. Use the command.
```bash
pip install -r requirements.txt
```

## Building Document Store
Then create the custom document store by fetching data. Document store is a place where you store multiple documents under a common name. A [document](https://docs.haystack.deepset.ai/docs/data-classes#document) is a individual unit that can hold data of text, image, json, and more with or with metadata.

An [document store](https://docs.haystack.deepset.ai/docs/document-store) is an indexed verison of your documents. It can act like database for your pipeline components to retrieve documents using [retrievers](https://docs.haystack.deepset.ai/docs/retrievers).

For our case we are considering the [InMemoryDocumentStore](https://docs.haystack.deepset.ai/docs/choosing-a-document-store#the-in-memory-document-store). It's a document store that comes out of the box with `haystack`. It doesn't require any external dependencies. This is the mostly preferred for small datasets and demo purposes. But if you are still looking for a robust use case Haystack has got to offer [various choices](https://docs.haystack.deepset.ai/docs/choosing-a-document-store#summary) to choose that best suits your use case.

Now we fetch the data from [PoetryDB](https://poetrydb.org/) API to obtain William Shakespeare poems. The response is in the form of JSON. Then we convert the json object into individual chunks of documents.
Finally we write the `documents` into the document store and check the total number of documents that have been added.


## Pipeline
Now let's shift our focus towards building the RAG Pipeline (Retrieval Augmentation). The various steps involved in building RAG Pipeline are:

![RAG Piepline](https://gist.github.com/assets/81156510/aa1c18a7-0ae5-4875-8999-a0fb228bdad7)

- Retrievers
- Prompt Template
- Generator

### Retrievers
As the name suggest, we use it to retrieve the documents that closely match the query/question. The most commonly used one is the InMemoryBM25Retriever. The reason that best suits our use case is that we make use of InMemoryDocumentStore. These both go hand in hand. It makes of keyword based matching using the [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25). It takes in list of Documents as input. Additional parameter, like search `filters` to reduce the search base, `top_k` list down the `k` document(s) default is 10 and `scale_score` if set to `true` then scales down the similarity scores in the range [0,1].

### Prompt Template
Now that we are building a QA RAG Pipeline there needs to be a prompt that would be fed into the LLM Generator, to be discussed next. Hence we, make use of [PromptBuilder](https://docs.haystack.deepset.ai/docs/promptbuilder). The template is built from [jinja2](https://palletsprojects.com/p/jinja/). It takes inputs as keyword arguments. These will be replace with actual values gathered during pipeline execution.

Then at this stage we pass the query that's collected from the user into the generator.

### Generator
As the title suggets, we are going to [generate](https://docs.haystack.deepset.ai/docs/generators) content. This is primarily used to answer the queries of the user. For our current use case we utilize the [`OpenAIGenerator`](https://docs.haystack.deepset.ai/docs/openaigenerator). Make sure to get OPENAI_API_KEY from [here](https://platform.openai.com).

This makes use of models gpt-3.5-turbo(default) and gpt-4 families. It takes a mandatory parameters like api key, `prompt` as `str`, and other optional parameters like [`generation_kwargs`](https://github.com/deepset-ai/haystack/blob/main/haystack/components/generators/openai.py#L71) which takes model parameters like `max_tokens`, `temperature`, `top_p`, `n`, `stop`, `presence_penalty`, `frequency_penalty`, and `logit_bias`. These are mostly left to default but the first 4 are widely used parameters amongst all of them. We are free to choose from other available generators that best choose your use case or stack.

Finally, we are ready to build the Pipeline by combining all the previous components together.

### What is a Haystack Pipeline?
A pipeline is a wrapper that contains multiple components connected together and hids the internal functionality from the user just exposing the input and the output data.
In haystack terms, Pipeline is defined as:
> The pipelines in Haystack 2.0 are directed [multigraphs](https://en.wikipedia.org/wiki/Multigraph) of different Haystack components and integrations.
We can achieve branching, looping, which speeds up the execution of the tasks. Through branching we achieve parallelism which in turn improves concurrency.

Then through loops we can iterate to the same pipeline again based on the past computation which improves the result, or capture the error until the loop can be executed. This is similar to a RCNN as in comparsion to deep learning.

We can add multiple components using the `pipeline_name.add_component()` with 2 arguments namely: name of the component to be aliased inside pipeline, the actual pipeline component. There on we will use the alias name to address the component. One can find all possible list of components in the haystack [documentation](https://docs.haystack.deepset.ai/docs/) on the left side panel under the heading **PIPELINE COMPONENTS**.

Now that we have components we have to connect them using the `pipeline_name.connect()` method that takes 2 parameters i.e. input and output component respectively. We also pass the respective inputs and this method will validate if the types of input and output match the given connection.

We can infer the same from the pipeline graph that haystack has to offer. One key thing to notice is the lines that connects various components. Dotted lines represent it's not mandatory to pass the tail component to the head component. A solid line represents a mandatory connection where any issue in the tail component breaks the entire pipeline flow thereby hindering `pipeline.run()`.
<!-- If need more content can add more about Pipeline Serialization and Graph Output generation -->

## Executing RAG Pipeline
Haystack provides us with this handy method called `pipeline_name.run()` to start executing the pipeline. It takes a `data` as a dictionary that needs to be passed to the component(s) as input. Then if we set the `debug` to true it will used to track the pipeline execution. It can be useful to log the pipeline execution and capture errors or mismatch if any.

This returns a dictionary of desired data type as result which can be used for further preprocessing. Then we can display the relevant information as output to the user.
