## Docker deployment

### Utilities
- 📚 [Haystack](https://haystack.deepset.ai)
- 🪝 [Hayhooks](https://docs.haystack.deepset.ai/docs/hayhooks)
- 🐳 [Docker](https://www.docker.com)
- 🚦 [Qdrant](https://qdrant.tech)
- 🔑 [OpenAI](https://openai.com)

### Prerequisites
- Ensure docker is [installed](https://www.docker.com/get-started/) locally in your system and the docker daemon in running.
- Then clone the repository using the command: ```git clone https://github.com/LLM-Projects/haystack-book.git```.
- Move to the appropriate directory: ```cd chapter-3/docker-qdrant-hayhooks/```
- Then run the docker container: ```docker compose up -d```. If you need to see the logs then disable the detached mode by removing the `-d` flag.
- If the containers are running successfully verify whether hayhooks and qdrant instances are up and running: http://localhost:1416/ and http://localhost:6333/dashboard.
- Then get an OpenAI API key from [here](https://platform.openai.com/api-keys).
- Please make sure to keep the server running and don't terminate the terminal as well as the container.

### Working
- After the hayhooks and qdrant instances are up and running then we need to push the data to the qdrant data store and query the documents to get response.
- First we fetch the data. It can be from the API as shown or from anywhere. But the final output must be a list of documents where each [`Document`](https://docs.haystack.deepset.ai/docs/data-classes#document)  the `content` and the `metadata` which is optional.
- Then we make create a indexing [pipeline](https://docs.haystack.deepset.ai/reference/pipeline-api) to [write](https://docs.haystack.deepset.ai/docs/documentwriter) the documents into the [QdrantDocumentStore](https://docs.haystack.deepset.ai/docs/qdrant-document-store).
![indexing pipeline](https://gist.github.com/assets/81156510/6a6b7b9c-bdf8-4255-bb06-ac6c772118c9)
![documents inside qdrant db](https://gist.github.com/assets/81156510/08c128a1-8e26-4dbf-b6d1-b9e0072792d5)
- Also, ensure to set the OpenAI API key as a environment variable.
- Then we have the prompt template which will be used in the [PromptBuilder](https://docs.haystack.deepset.ai/docs/promptbuilder) component inside of Query Pipeline.
- Then we build the query pipeline where we [embed](https://docs.haystack.deepset.ai/docs/sentencetransformerstextembedder) the query, perform the [retrieval](https://docs.haystack.deepset.ai/docs/qdrantembeddingretriever) to get the closest documents using cosine similarity, and [generate](https://docs.haystack.deepset.ai/docs/openaigenerator) a response based on the prompt from the prompt template as mentioned above.
![querying pipeline](https://gist.github.com/assets/81156510/af827a3b-4707-4113-b998-6ca9cf06e8f5)
- Display the response to the user.

### Accessibility
- Python (as mentioned in the section above)
- CURL commands
- REST API requests

#### CURL
- For indexing (command for generic case):
```bash
curl -X "POST" "http://localhost:1416/qdrant_indexing" \
     -H 'Accept: application/json' \
     -H 'Content-Type: application/json' \
     -d $'{
  "converter": {
    "sources": [
      {
        "meta": {},
        "data": <add_your_content_here>
      }
    ],
    "meta": {}
  },
  "writer": {}
}'
```
- For querying:
```bash
curl -X "POST" "http://localhost:1416/qdrant_query" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "embedder": {
    "text": <ask_your_query_here>
  },
  "retriever": {}
}
```

#### REST API requests
Here are some example requests:
```bash
// List all collections
GET collections

// Get collection info
GET collections/Document

// List points in a collection, using filter
POST collections/Document/points/scroll
{
  "limit": 10,
  "filter": {
    "must": [
      {
        "key": "meta",
        "match": {
          "any": [
            ""
          ]
        }
      }
    ]
  }
}
```
