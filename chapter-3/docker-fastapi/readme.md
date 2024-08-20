# App for PDF document QA

This repository contains a question-answering system built with FastAPI and Haystack. It uses an in-memory vector store for document retrieval and PostgreSQL to store user interactions. The system allows users to upload documents, ask questions, and receive answers based on the uploaded content.
Key Components:

## app.py (FastAPI Application):

Main entry point of the application
Implements FastAPI routes for document upload, querying, and serving the frontend
Integrates Haystack pipelines for document processing and question answering
Connects to PostgreSQL for storing user interactions


## static/index.html:

Simple HTML frontend for user interaction
Allows users to upload documents and ask questions
Displays answers and relevant context


## In-Memory Vector Store:

Utilizes Haystack's InMemoryDocumentStore
Stores document embeddings for efficient retrieval
Allows for quick similarity search during the question-answering process


## PostgreSQL Database:

Stores user interactions (questions asked and answers provided)
Allows for analysis of user behavior and system performance



# Key Functionalities:

## Document Upload:

Users can upload PDF documents
Documents are processed, split into chunks, and stored in the vector store


## Question Answering:

Users can ask questions related to the uploaded documents
The system retrieves relevant document chunks and generates an answer


## Interaction Logging:

All user questions and system answers are logged in PostgreSQL

# For testing

uvicorn app:app --reload

## Docker
docker build -t fastapi-app-haystack:latest .
docker run -p 8000:8000 fastapi-app-haystack:latest

## Docker command with DB
docker run -p 8000:8000 -e DATABASE_URL=postgresql://username:password@host.docker.internal:5432/database_name fastapi-app-haystack:latest

![Image](./screenshot.jpg)