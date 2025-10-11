# llamacpp-reranking

Comprehensive benchmarking and testing framework for llama.cpp's reranking endpoint, evaluating 14 quantized reranking models across 10 diverse domains.

## Overview

This project provides an automated testing framework to evaluate and compare reranking models through llama.cpp's `/rerank` endpoint. It includes:

- **Automated testing** of 14 different reranking models
- **10 diverse test queries** across different domains (geography, technology, medicine, law, etc.)
- **Accuracy validation** against ground truth answers
- **Performance metrics** (speed, relevance scores)
- **Comprehensive analysis** with detailed reports

## Key Results

**Top Models (100% Accuracy):**
- 🥇 **bge-reranker-v2-m3** (418 MB, 72ms avg) - Best overall
- 🥈 **ms-marco-MiniLM-L12-v2** (28 MB, 20ms avg) - Fastest & smallest
- 🥉 **jina-reranker-v2-base-multilingual** (212 MB, 43ms avg) - Multilingual

See `REPORT.md` for complete analysis.

## Prerequisites

- **Python:** 3.13 or higher
- **Package Manager:** [uv](https://github.com/astral-sh/uv)
- **llama.cpp:** Version 6730+ with server support
- **Models:** Q4_K_M quantized reranking models
- **Hardware:** Apple M4 Pro used for testing (Metal acceleration)

## Setup

### 1. Install Dependencies

```bash
# Clone this repository
git clone <repo-url>
cd llamacpp-reranking

# Create virtual environment and install dependencies
uv venv
uv add requests
```

### 2. Download Models

Download reranking models to `~/Documents/reranking-models/`:

**Recommended models:**
- [bge-reranker-v2-m3-Q4_K_M.gguf](https://huggingface.co/) (best overall)
- [ms-marco-MiniLM-L12-v2.Q4_K_M.gguf](https://huggingface.co/) (fastest)
- [jina-reranker-v2-base-multilingual-Q4_K_M.gguf](https://huggingface.co/) (multilingual)

See `CLAUDE.md` for the complete list of 14 models tested.

### 3. Install llama.cpp

```bash
# Make sure llama-server is in your PATH
llama-server --version
```

## Running the Benchmark

Test all models (takes ~10 minutes):

```bash
uv run python test_all_models.py
```

**Output files:**
- `test_results.csv` - Detailed metrics for all 140 tests (14 models × 10 queries)
- Console output - Real-time progress with accuracy indicators (✓/✗)

**The script automatically:**
- Starts llama-server for each model
- Runs all 10 test queries
- Records accuracy, speed, and relevance scores
- Generates performance rankings
- Stops the server cleanly

## Project Structure

```
llamacpp-reranking/
├── test_all_models.py    # Automated testing framework
├── test_queries.csv      # Test dataset (10 domains, 50 documents)
├── test_results.csv      # Benchmark results (generated)
├── REPORT.md            # Detailed analysis report
├── README.md            # This file
├── CLAUDE.md            # Project context for AI assistants
└── pyproject.toml       # Project metadata
```

## Test Dataset

### Domains Tested
1. **Geography** - Capital cities
2. **Technology** - Algorithms and programming
3. **Medicine** - Symptoms and conditions
4. **Law** - Legal concepts
5. **Cooking** - Recipes and techniques
6. **Finance** - Financial concepts
7. **History** - Historical events
8. **Sports** - Rules and regulations
9. **Literature** - Authors and works
10. **Science** - Scientific processes

Each test includes:
- 1 query
- 5 candidate documents (1 correct, 4 distractors)
- Ground truth answer for validation

## Results Format

### test_results.csv Columns

```csv
model_name, model_size_mb, domain, query, correct_doc_index,
success, response_time_seconds, top_score, top_document_index,
top_document, correct_answer, rank_2_score, rank_3_score,
rank_4_score, rank_5_score, all_scores, error, timestamp
```

**Key metrics:**
- `correct_answer` - Boolean: Did model rank correct document first?
- `response_time_seconds` - Query latency
- `top_score` - Relevance score of top-ranked document
- `all_scores` - All 5 relevance scores (JSON array)

## Performance Summary

| Category | Metric | Value |
|----------|--------|-------|
| Total Tests | Models × Queries | 140 (14 × 10) |
| Success Rate | No crashes/errors | 100% (140/140) |
| Overall Accuracy | Correct top-1 rankings | 65.7% (92/140) |
| Perfect Models | 100% accuracy | 3 models |
| Speed Range | Min - Max | 12ms - 540ms |
| Size Range | Smallest - Largest | 18 MB - 4.8 GB |

### Model Rankings

**By Accuracy:**
1. bge-reranker-v2-m3 (100%)
2. jina-reranker-v2-base-multilingual (100%)
3. ms-marco-MiniLM-L12-v2 (100%)
4. mxbai-rerank-large-v2 (90%)
5. jina-reranker-m0 (90%)

**By Speed:**
1. ms-marco-MiniLM-L4-v2 (12ms)
2. jina-reranker-v1-tiny-en (14ms)
3. ms-marco-MiniLM-L12-v2 (20ms)
4. bge-reranker-base (29ms)
5. colbertv2.0 (39ms)

## API Reference

### Endpoint: POST /rerank

**Request:**
```json
{
  "query": "What is the capital of France?",
  "documents": [
    "The Eiffel Tower is in Paris.",
    "Berlin is the capital of Germany.",
    "The city of Paris serves as the capital of France."
  ]
}
```

**Response:**
```json
{
  "results": [
    {"index": 2, "relevance_score": 8.1388},
    {"index": 0, "relevance_score": 1.0144},
    {"index": 1, "relevance_score": -4.5394}
  ]
}
```

**Notes:**
- Results sorted by relevance (highest first)
- `index` refers to position in input documents array
- Scores can be negative (model-dependent)
- Score magnitude varies by model

## Use Cases

### Production RAG Systems
Use `bge-reranker-v2-m3` for:
- Highest accuracy (100%)
- Strong score differentiation
- Reasonable speed (72ms)

### High-Throughput Applications
Use `ms-marco-MiniLM-L12-v2` for:
- Perfect accuracy (100%)
- Fastest of perfect models (20ms)
- Smallest footprint (28 MB)

### Multilingual Content
Use `jina-reranker-v2-base-multilingual` for:
- Perfect accuracy (100%)
- Multilingual support
- Good speed (43ms)

## Key Findings

### What Works
✅ Three models achieved perfect 100% accuracy
✅ Quantized models perform well (Q4_K_M format)
✅ Millisecond latencies on consumer hardware
✅ Small models can match large model accuracy

### Observations
- Score magnitude doesn't correlate with accuracy
- Negative scores are valid (model-dependent)
- Some models return tie scores (identical values)
- Qwen models incompatible with current endpoint

### Issues Found
❌ Qwen3 models return all zeros (incompatible)
❌ colbertv2.0 only 10% accuracy
❌ Some models show tie-scoring behavior

## Limitations

- **English only** - No multilingual queries tested
- **Short documents** - All 1-2 sentences
- **Factual queries** - Clear correct answers
- **Small dataset** - Only 10 test queries
- **Single platform** - Apple M4 Pro only

## Future Work

- [ ] Test with longer documents
- [ ] Add semantic similarity tests (no "correct" answer)
- [ ] Multilingual query evaluation
- [ ] Domain-specific corpus testing
- [ ] Batch processing optimization
- [ ] Multiple quantization levels (Q8, Q6, Q5)
- [ ] GPU scaling tests
- [ ] Fine-tuning evaluation

## Documentation

- **REPORT.md** - Comprehensive analysis with charts and rankings
- **CLAUDE.md** - Detailed project context for AI assistants
- **test_queries.csv** - Test dataset with correct answers
- **test_results.csv** - Raw benchmark data (generated)

## Contributing

This is a research/benchmarking project. Contributions welcome:
- Additional test queries
- New model evaluations
- Performance optimizations
- Documentation improvements

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- **llama.cpp** - Efficient LLM inference engine
- **Model creators** - BGE (BAAI), Jina AI, MS-MARCO, Qwen, MxBai, ColBERT
- **uv** - Fast Python package manager
- **Apple** - M4 Pro hardware and Metal acceleration

---

**Questions?** See `REPORT.md` for detailed analysis or `CLAUDE.md` for implementation details.
