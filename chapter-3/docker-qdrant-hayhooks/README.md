## Docker deployment

🕹️ Demo
https://gist.github.com/assets/81156510/dc880d50-a3a3-433b-94e3-7b74cdb0cdfe
> P.S.: Since I ran the this earlier too I have the documents in the Qdrant Document Store. In your case this will not be the same.

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
- Then run the docker container: ```docker-compose --env-file .env up -d```. If you need to see the logs then disable the detached mode by removing the `-d` flag.
- If the containers are running successfully verify whether hayhooks and qdrant instances are up and running: http://localhost:1416/ and http://localhost:6333/dashboard.
- Then get an OpenAI API key from [here](https://platform.openai.com/api-keys) and store it in `.env` file in the current directory which will be used later.
- Please make sure to keep the server running and don't terminate the terminal as well as the container.

### Working (Using Python)
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
![final response](https://gist.github.com/assets/81156510/c9331498-7b5d-41e0-aada-0c9d9fb3cf43)

### Working (Using [Hayhooks](https://docs.haystack.deepset.ai/docs/hayhooks))
- This setup uses Hayhooks, an application server that exposes Haystack pipelines as HTTP Endpoints.
![hayhooks start server command with mount](https://gist.github.com/assets/81156510/6da7b48d-be71-46d6-adc2-32f55c20c021)
- We can add or delete the pipeline using `/deploy` or `/undeploy` endpoint on hayhooks endpoint at port `1416`.
- Alternatively, we can mount the directory that contains the pipelines in the `.yml` format. And we can use them as deployed pipelines with the endpoint as the file name.
![hayhooks deployment](https://gist.github.com/assets/81156510/5f08e1f4-2d13-4769-b305-fc47df2e620f)
P.S.: Reference can be found at [haystack-demos/qdrant_indexing](https://github.com/deepset-ai/haystack-demos/tree/main/qdrant_indexing).

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

#### REST API requests (using Postman or any other tools)
Contains the equivalent REST commands for the [cURL](https://github.com/LLM-Projects/haystack-book/blob/main/chapter-3/docker-qdrant-hayhooks/README.md#curl) methods from hayhooks served at `PORT::1416`:
- Indexing (/qdrant_indexing)
- Querying (/qdrant_query)
of the Qdrant Hayhooks Docker deployment.  
After the [setup](https://github.com/LLM-Projects/haystack-book/blob/main/chapter-3/docker-qdrant-hayhooks/README.md#prerequisites) with relevant data we can run the REST commands to perform the specified actions.

Postman link: https://documenter.getpostman.com/view/18446656/2sA3kPqQKi

---

##### `POST` Indexing
To add new indexes (documents) to the underlying document store in out case its [qdrant](https://qdrant.tech).

- - Request Headers

| Header | Value |
| --- | --- |
| Accept       | application/json     |
| Content-Type | application/json     |

- - Body raw(json)
```json
{
  "converter": {
    "sources": [
      {
        "meta": {},
        "data": "add_your_content_here"
      }
    ],
    "meta": {}
  },
  "writer": {}
}
```

##### `POST` Querying
To retrieve a list of the most closest documents from the document store based on query.

- - Request Headers

| Header | Value |
| --- | --- |
| Content-Type | application/json; charset=utf-8 |

- - Body raw(json)
```json
{
  "embedder": {
    "text": "ask_your_query_here"
  },
  "retriever": {}
}
```

#### REST API requests (from qdrant dashboard)
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
