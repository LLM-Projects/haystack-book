from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
import tempfile
import psycopg2

from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter

#sentence transformer model for retrieval
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
document_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")

#GPT-3.5 for generation
import os
from getpass import getpass
from haystack.components.generators import OpenAIGenerator

# if "OPENAI_API_KEY" not in os.environ:
#     os.environ["OPENAI_API_KEY"] = getpass("Enter OpenAI API key:")
# generator = OpenAIGenerator(model="gpt-3.5-turbo")

from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder,AnswerBuilder

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load environment variables from .env file
load_dotenv()

# Get the OPENAI_API_KEY
openai_api_key = os.getenv("OPENAI_API_KEY")
generator = OpenAIGenerator(model="gpt-3.5-turbo")

# Initialize DocumentStore
document_store = InMemoryDocumentStore()
document_writer = DocumentWriter(document_store)

# Initialize components
# pdf_converter = PyPDFToDocument()
# splitter = DocumentSplitter(split_by="sentence", split_length=2048)
# document_embedder = SentenceTransformersDocumentEmbedder()
# text_embedder = SentenceTransformersTextEmbedder()
# document_writer = DocumentWriter(document_store=document_store)
# retriever = InMemoryEmbeddingRetriever(document_store=document_store)
# generator = OpenAIGenerator(api_key=openai_api_key, model_name="gpt-4")


# Create indexing pipeline
indexing_pipeline = Pipeline()
indexing_pipeline.add_component("converter", PyPDFToDocument())
indexing_pipeline.add_component("cleaner", DocumentCleaner())
indexing_pipeline.add_component("splitter", DocumentSplitter(split_by="sentence", split_length=5))
indexing_pipeline.add_component(instance=document_embedder, name="embedder")
indexing_pipeline.add_component("writer", DocumentWriter(document_store=document_store))

indexing_pipeline.connect("converter", "cleaner")
indexing_pipeline.connect("cleaner", "splitter")
indexing_pipeline.connect("splitter", "embedder")
indexing_pipeline.connect("embedder", "writer")


# Create querying pipeline
template = """
Answer the questions based on the given context.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{ question }}
Answer:
"""
querying_pipeline = Pipeline()
querying_pipeline.add_component("query_embedder", SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2"))
querying_pipeline.add_component("retriever", InMemoryEmbeddingRetriever(document_store=document_store))
querying_pipeline.add_component("prompt_builder", PromptBuilder(template=template))
querying_pipeline.add_component("llm", OpenAIGenerator(model="gpt-3.5-turbo"))
querying_pipeline.add_component("answer_builder", AnswerBuilder())
querying_pipeline.connect("query_embedder", "retriever.query_embedding")
querying_pipeline.connect("retriever", "prompt_builder.documents")
querying_pipeline.connect("prompt_builder", "llm")
querying_pipeline.connect("llm.replies", "answer_builder.replies")
querying_pipeline.connect("llm.meta", "answer_builder.meta")
querying_pipeline.connect("retriever", "answer_builder.documents")

# PostgreSQL connection
conn = psycopg2.connect(os.environ.get("DATABASE_URL"))

class Query(BaseModel):
    question: str

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    _, file_extension = os.path.splitext(file.filename)
    
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix=file_extension) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    # Run indexing pipeline
    result = indexing_pipeline.run({"converter": {"sources": [temp_file_path]}})
    print(f"Documents indexed: {result}")

    # Remove the temporary file
    os.unlink(temp_file_path)
    
    return {"message": "File uploaded and indexed successfully"}

@app.post("/query")
async def query(query: Query):
    try:
        # Run querying pipeline

        result = querying_pipeline.run(
                        data={"query_embedder": {"text": query.question}, "prompt_builder": {"question": query.question}, "answer_builder": {"query": query.question}})
                
        
        answer = result['answer_builder']['answers'][0].data
        
        # Safely get context, providing a default if not available
        context = [d.content for d in result['answer_builder']['answers'][0].documents]
        
        # Store query and response in PostgreSQL
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO queries (question, context, answer) VALUES (%s, %s, %s)",
            (query.question, str(context), answer)
        )
        conn.commit()
        
        print(f"answer: {answer}, context: {context}")
        return {"answer": answer, "context": context}
    
    except Exception as e:
        # Log the error (you might want to use a proper logging system)
        print(f"Error in query endpoint: {str(e)}")
        # Return a more informative error response
        return {"error": f"An error occurred: {str(e)}", "details": str(result) if 'result' in locals() else "No result available"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)