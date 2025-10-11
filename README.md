# llamacpp-reranking

A Python client demonstrating how to use llama.cpp's reranking endpoint with the BGE-reranker-v2-m3 model.

## Overview

This project shows how to rerank documents based on their relevance to a query using llama.cpp's `/rerank` endpoint. Reranking is useful for improving search results, question-answering systems, and information retrieval tasks.

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- llama.cpp compiled with server support
- A reranking model (e.g., BGE-reranker-v2-m3)

## Setup

1. Clone or download this repository

2. Create a virtual environment and install dependencies:
```bash
uv venv
uv add requests
```

3. Download a reranking model (if you haven't already):
```bash
# Example: BGE-reranker-v2-m3 quantized model
# Download from Hugging Face or other sources
```

## Running the Example

1. Start the llama.cpp server with a reranking model:
```bash
llama-server -m ~/Documents/reranking-models/bge-reranker-v2-m3-Q4_K_M.gguf --port 8080 --rerank
```

2. Run the Python client:
```bash
uv run python main.py
```

## How It Works

The `main.py` script:
1. Sends a query and list of documents to the llama.cpp server
2. Receives relevance scores for each document
3. Sorts and displays documents by relevance (highest to lowest)

### Example Output

```
--- Reranked Results (from most to least relevant) ---

Score: 8.1388
Document: "The city of Paris serves as the capital of France."

Score: 1.0144
Document: "Paris is known for its art, fashion, and culture."

Score: -0.3991
Document: "The Eiffel Tower is a famous landmark in Paris."
```

## Configuration

Edit `main.py` to customize:
- `SERVER_URL`: The llama.cpp server endpoint (default: `http://localhost:8080/rerank`)
- `query`: Your search query
- `documents`: List of documents to rerank

## API Format

The `/rerank` endpoint expects:
```json
{
  "query": "Your search query",
  "documents": ["doc1", "doc2", "doc3"]
}
```

And returns:
```json
{
  "results": [
    {"index": 0, "relevance_score": 8.1388},
    {"index": 1, "relevance_score": 1.0144}
  ]
}
```

## Use Cases

- Improving search results in RAG (Retrieval-Augmented Generation) systems
- Question-answering systems
- Document similarity ranking
- Content recommendation

## License

This project is provided as-is for demonstration purposes.
