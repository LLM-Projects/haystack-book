import getpass
import os

import requests
from haystack import Document, Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder)
from haystack.components.generators import OpenAIGenerator
from haystack.components.writers import DocumentWriter
from haystack_integrations.components.retrievers.qdrant import \
    QdrantEmbeddingRetriever
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore


def get_data():
    url = "https://poetrydb.org/author/"
    author_name = "William Shakespeare"
    data = requests.get(url + author_name)
    data = data.json()

    documents = []
    for doc in data:
        sentence = " ".join(doc["lines"])

        documents.append(
            Document(
                content=sentence,
                meta={
                    "Title": doc["title"],
                    "Author": doc["author"],
                    "Linecount": doc["linecount"],
                },
            )
        )

    return documents


def build_indexing_pipeline():
    # Create a new index pipeline
    indexing_pipeline = Pipeline()

    # Define all the components
    indexing_pipeline.add_component("embedder", SentenceTransformersDocumentEmbedder())
    indexing_pipeline.add_component("writer", DocumentWriter(QdrantDocumentStore()))

    # Connect the components
    indexing_pipeline.connect("embedder", "writer")

    return indexing_pipeline


def build_query_pipeline():
    # Create a new query pipeline
    query_pipeline = Pipeline()

    # Define all the components
    query_pipeline.add_component("embedder", SentenceTransformersTextEmbedder())
    query_pipeline.add_component(
        "retriever", QdrantEmbeddingRetriever(QdrantDocumentStore())
    )

    query_pipeline.add_component("prompt_builder", PromptBuilder(template=template))
    query_pipeline.add_component(
        "generator",
        OpenAIGenerator(model="gpt-3.5-turbo"),
    )

    # Connect the components
    # query_pipeline.connect("embedder.embedding", "retriever.query_embedding", "prompt_builder.query_embedding")
    query_pipeline.connect("embedder.embedding", "retriever.query_embedding")
    query_pipeline.connect("retriever", "prompt_builder.documents")
    query_pipeline.connect("prompt_builder", "generator")

    return query_pipeline


if __name__ == "__main__":
    # Get the list of documents, you can modify the source of your data
    documents_list = get_data()

    # Establish the indexing pipeline
    indexing_pipeline = build_indexing_pipeline()

    # Run the index pipeline and flush the data as documents
    indexing_pipeline.run({"documents": documents_list})

    # Displays {"writer": {"documents_written": 1}}

    # Set the `OPENAI_API_KEY` as an environment variable
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = getpass("Enter OpenAI API key:")

    # Define the prompt template to be passed to the LLM generator
    template = """
                Given the following information, answer the query
                based on data from Document store.

                Context: 
                {% for document in documents %}
                    {{ document.content }}
                {% endfor %}

                Question: {{ query }}?
              """

    querying_pipeline = build_query_pipeline()

    question = input("Enter the query: ")

    print(
        querying_pipeline.run(
            {
                "embedder": {"text": question},
                "prompt_builder": {"query": question},
            }
        )
    )
