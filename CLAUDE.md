# llamacpp-reranking Project Context

## Project Overview
This is a Python client project that demonstrates how to use llama.cpp's reranking endpoint. It showcases document reranking functionality using the BGE-reranker-v2-m3 model through llama.cpp's server.

## Tech Stack
- **Language**: Python 3.13+
- **Package Manager**: uv (fast Python package installer and resolver)
- **Dependencies**: requests library only
- **Server**: llama.cpp server with reranking support
- **Model**: BGE-reranker-v2-m3-Q4_K_M (quantized reranking model)

## Project Structure
```
llamacpp-reranking/
├── main.py              # Client script that calls the reranking endpoint
├── pyproject.toml       # Project metadata and dependencies
├── README.md            # Project documentation
├── .gitignore          # Git ignore rules
├── .python-version     # Python version specification
├── .venv/              # Virtual environment
└── uv.lock            # Dependency lock file
```

## Key Files

### main.py
The main client script that:
- Defines a query and list of documents to rerank
- Sends POST request to `http://localhost:8080/rerank`
- Receives relevance scores for each document
- Sorts and displays results by relevance (highest to lowest)

**Important**: The server must be running before executing this script.

## How the Reranking Works

1. **Input**:
   - A query string (e.g., "What is the capital of France?")
   - A list of document strings to be ranked

2. **Process**:
   - Client sends JSON payload to llama.cpp server's `/rerank` endpoint
   - Server uses BGE-reranker model to compute relevance scores
   - Higher scores = more relevant to the query

3. **Output**:
   - List of results with `index` (original position) and `relevance_score`
   - Client sorts by score and displays documents in order of relevance

## Running the Project

**Start the llama.cpp server**:
```bash
llama-server -m ~/Documents/reranking-models/bge-reranker-v2-m3-Q4_K_M.gguf --port 8080 --rerank
```

**Run the client**:
```bash
uv run python main.py
```

## API Specification

**Endpoint**: `POST /rerank`

**Request Format**:
```json
{
  "query": "search query string",
  "documents": ["doc1", "doc2", "doc3"]
}
```

**Response Format**:
```json
{
  "results": [
    {"index": 0, "relevance_score": 8.1388},
    {"index": 4, "relevance_score": 1.0144}
  ]
}
```

## Development Workflow

1. **Adding dependencies**: `uv add package-name`
2. **Running scripts**: `uv run python script.py`
3. **Virtual environment**: Created with `uv venv`, activated with `source .venv/bin/activate`

## Use Cases
- RAG (Retrieval-Augmented Generation) systems
- Search result optimization
- Question-answering systems
- Document similarity ranking
- Content recommendation engines

## Notes for AI Assistants

- This is a demonstration/example project, not a production application
- The server must be running locally on port 8080 before the client can work
- The model file path is hardcoded to `~/Documents/reranking-models/`
- Error handling is basic (catches RequestException only)
- Results are always sorted by relevance score in descending order
- The code is intentionally simple and well-commented for educational purposes

### Important: Maintaining This Document
**You MUST update this CLAUDE.md file when making significant changes to the project**, including but not limited to:
- Adding or removing dependencies
- Changing project structure or file organization
- Modifying API endpoints or data formats
- Adding new features or functionality
- Changing configuration or environment requirements
- Updating the tech stack or development workflow
- Modifying error handling or logging approaches

Keep this document synchronized with the actual codebase to ensure accurate context for future AI assistance.

## Code Style
- Uses clear variable names and comments
- Follows standard Python conventions
- Minimal dependencies (only requests)
- Simple error handling with try/except
- Formatted output for readability

## Future Enhancements (if requested)
- Add command-line arguments for query and documents
- Support for batch processing multiple queries
- Configuration file for server URL and settings
- More robust error handling and retries
- Logging support
- Performance metrics (timing, throughput)
- Support for different reranking models
