# RAG Optimization Components

This repository contains implementations and evaluations of Retrieval Augmented Generation (RAG) pipelines, focusing on basic and optimized versions along with various evaluation metrics.

## Table of Contents

1. [Basic RAG Pipeline](#basic-rag-pipeline)
2. [Evaluations](#evaluations)
   - [Semantic Answer Similarity (SAS)](#semantic-answer-similarity-sas)
   - [Context Relevance](#context-relevance)
   - [Faithfulness](#faithfulness)
3. [Optimized Pipeline](#optimized-pipeline)
4. [Evaluation Results](#evaluation-results)

## Basic RAG Pipeline

The basic RAG pipeline consists of the following components:

```python
basic_rag = Pipeline()
basic_rag.add_component("query_embedder", SentenceTransformersTextEmbedder(
    model="sentence-transformers/all-MiniLM-L6-v2", progress_bar=False
))
basic_rag.add_component("retriever", InMemoryEmbeddingRetriever(document_store, top_k=3))
basic_rag.add_component("prompt_builder", PromptBuilder(template=template))
basic_rag.add_component("llm", OpenAIGenerator(model="gpt-3.5-turbo"))
basic_rag.add_component("answer_builder", AnswerBuilder())

# Connections
basic_rag.connect("query_embedder", "retriever.query_embedding")
basic_rag.connect("retriever", "prompt_builder.documents")
basic_rag.connect("prompt_builder", "llm")
basic_rag.connect("llm.replies", "answer_builder.replies")
basic_rag.connect("llm.meta", "answer_builder.meta")
basic_rag.connect("retriever", "answer_builder.documents")
```

## Evaluations

We use three main evaluation metrics:

### Semantic Answer Similarity (SAS)

SAS measures the semantic similarity between predicted and ground truth answers.

```python
from haystack.components.evaluators import SASEvaluator

sas_evaluator = SASEvaluator()
```

### Context Relevance

This metric assesses the relevance of the retrieved context to the query.

```python
from haystack.components.evaluators import ContextRelevanceEvaluator

context_relevance_evaluator = ContextRelevanceEvaluator(raise_on_failure=False)
```

### Faithfulness

Faithfulness evaluates how well the generated answer adheres to the retrieved context.

```python
from haystack.components.evaluators import FaithfulnessEvaluator

faithfulness_evaluator = FaithfulnessEvaluator(raise_on_failure=False)
```

## Optimized Pipeline

The optimized pipeline incorporates hybrid search and re-ranking:

```python
hybrid_retrieval = Pipeline()
hybrid_retrieval.add_component("text_embedder", text_embedder)
hybrid_retrieval.add_component("embedding_retriever", embedding_retriever)
hybrid_retrieval.add_component("bm25_retriever", bm25_retriever)
hybrid_retrieval.add_component("document_joiner", document_joiner)
hybrid_retrieval.add_component("ranker", ranker)
hybrid_retrieval.add_component("prompt_builder", PromptBuilder(template=template))
hybrid_retrieval.add_component("llm", OpenAIGenerator(model="gpt-3.5-turbo"))
hybrid_retrieval.add_component("answer_builder", AnswerBuilder())

# Connections
hybrid_retrieval.connect("text_embedder", "embedding_retriever")
hybrid_retrieval.connect("bm25_retriever", "document_joiner")
hybrid_retrieval.connect("embedding_retriever", "document_joiner")
hybrid_retrieval.connect("document_joiner", "ranker")
hybrid_retrieval.connect("ranker", "prompt_builder.documents")
hybrid_retrieval.connect("prompt_builder", "llm")
hybrid_retrieval.connect("llm.replies", "answer_builder.replies")
hybrid_retrieval.connect("llm.meta", "answer_builder.meta")
hybrid_retrieval.connect("ranker", "answer_builder.documents")
```

## Evaluation Results

To evaluate both pipelines:

```python
eval_pipeline = Pipeline()
eval_pipeline.add_component("context_relevance", ContextRelevanceEvaluator(raise_on_failure=False))
eval_pipeline.add_component("faithfulness", FaithfulnessEvaluator(raise_on_failure=False))
eval_pipeline.add_component("sas", SASEvaluator())

eval_pipeline_results = eval_pipeline.run(
    {
        "context_relevance": {"questions": questions, "contexts": retrieved_contexts},
        "faithfulness": {"questions": questions, "contexts": retrieved_contexts, "predicted_answers": predicted_answers},
        "sas": {"predicted_answers": predicted_answers, "ground_truth_answers": answers},
    }
)

results = {
    "context_relevance": eval_pipeline_results['context_relevance'],
    "faithfulness": eval_pipeline_results['faithfulness'],
    "sas": eval_pipeline_results['sas']
}

eval_results = EvaluationRunResult(run_name="RAG Pipeline", inputs=inputs, results=results)
eval_results.score_report()
```

This README provides an overview of the key components in our Haystack based RAG optimization project. For detailed implementation and usage instructions, please refer to the individual code files and documentation within the repository.
