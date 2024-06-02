import os
import getpass
import requests

from haystack import Pipeline
from haystack import Document
from haystack.components.writers import DocumentWriter
from haystack.components.embedders import (
    SentenceTransformersTextEmbedder,
    SentenceTransformersDocumentEmbedder,
)
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.utils import Secret
from haystack.components.generators import OpenAIGenerator


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


if __name__ == "__main__":
    indexing = Pipeline()
    indexing.add_component("embedder", SentenceTransformersDocumentEmbedder())
    indexing.add_component("writer", DocumentWriter(QdrantDocumentStore()))
    indexing.connect("embedder", "writer")

    documents_list = get_data()
    indexing.run({"documents": documents_list})
    print(indexing.dumps())
    # Displays {'writer': {'documents_written': 1}}

    template = """
                Given the following information, answer the query
                based on data from Document store.

                Context: 
                {% for document in documents %}
                    {{ document.content }}
                {% endfor %}

                Question: {{ query }}?
              """
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = getpass("Enter OpenAI API key:")

    generator = OpenAIGenerator(model="gpt-3.5-turbo")

    query = Pipeline()
    query.add_component("embedder", SentenceTransformersTextEmbedder())
    query.add_component("retriever", QdrantEmbeddingRetriever(QdrantDocumentStore()))
    query.add_component("prompt_builder", PromptBuilder(template=template))
    query.add_component(
        "generator",
        generator,
    )

    # query.connect("embedder.embedding", "retriever.query_embedding", "prompt_builder.query_embedding")
    query.connect("embedder.embedding", "retriever.query_embedding")
    query.connect("retriever", "prompt_builder.documents")
    query.connect("prompt_builder", "generator")
    question = "Summarize Sonnet 151."

    print(
        query.run(
            {
                "embedder": {"text": question},
                "prompt_builder": {"query": question},
            }
        )
    )
