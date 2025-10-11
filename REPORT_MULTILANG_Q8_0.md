# Multilingual Reranking Benchmark - Q8_0 Quantization

## Executive Summary

**Quantization:** Q8_0
**Tests Completed:** 1080
**Models Tested:** 18
**Languages:** 6 (English, French, German, Spanish, Arabic, Chinese)
**Domains per Language:** 10

**Overall Accuracy:** 8.7%
**Average Response Time:** 158ms
**Total Storage:** 16.5 GB

**Perfect Accuracy Models (100%):** 0

## Top 10 Models - Overall Performance

| Rank | Model | Accuracy | Avg Time | Size | Queries |
|------|-------|----------|----------|------|----------|
| 1 🏆 | ms-marco-MiniLM-L2-v2 | 26.7% | 8ms | 16 MB | 16/60 |
| 2 ⭐ | ms-marco-TinyBERT-L2 | 23.3% | 7ms | 5 MB | 14/60 |
| 3 ⭐ | ms-marco-MiniLM-L4-v2 | 18.3% | 11ms | 20 MB | 11/60 |
| 4  | ms-marco-MiniLM-L6-v2 | 16.7% | 12ms | 24 MB | 10/60 |
| 5  | ms-marco-TinyBERT-L2-v2 | 15.0% | 8ms | 5 MB | 9/60 |
| 6  | ms-marco-TinyBERT-L6 | 13.3% | 15ms | 69 MB | 8/60 |
| 7  | jina-reranker-v1-turbo-en | 11.7% | 13ms | 39 MB | 7/60 |
| 8  | jina-reranker-v1-tiny-en | 10.0% | 10ms | 34 MB | 6/60 |
| 9  | bge-reranker-base | 8.3% | 24ms | 289 MB | 5/60 |
| 10  | bge-reranker-large | 8.3% | 53ms | 576 MB | 5/60 |

## Performance by Language

### Arabic (ar)
- Average Accuracy: 3.9%
- Models with 100%: 0
- **Top 5:** ms-marco-MiniLM-L2-v2 (20%), ms-marco-TinyBERT-L6 (20%), ms-marco-TinyBERT-L2 (10%), ms-marco-MiniLM-L6-v2 (10%), bge-reranker-base (10%)

### German (de)
- Average Accuracy: 10.6%
- Models with 100%: 0
- **Top 5:** ms-marco-MiniLM-L2-v2 (50%), ms-marco-MiniLM-L4-v2 (30%), ms-marco-TinyBERT-L2 (20%), ms-marco-TinyBERT-L2-v2 (20%), ms-marco-MiniLM-L6-v2 (20%)

### English (en)
- Average Accuracy: 8.3%
- Models with 100%: 0
- **Top 5:** ms-marco-TinyBERT-L2 (40%), ms-marco-MiniLM-L4-v2 (30%), ms-marco-TinyBERT-L2-v2 (20%), bge-reranker-large (20%), jina-reranker-v1-tiny-en (10%)

### Spanish (es)
- Average Accuracy: 8.3%
- Models with 100%: 0
- **Top 5:** ms-marco-TinyBERT-L2 (20%), ms-marco-TinyBERT-L2-v2 (20%), ms-marco-MiniLM-L2-v2 (20%), ms-marco-MiniLM-L4-v2 (20%), ms-marco-MiniLM-L6-v2 (20%)

### French (fr)
- Average Accuracy: 8.9%
- Models with 100%: 0
- **Top 5:** ms-marco-MiniLM-L2-v2 (30%), ms-marco-TinyBERT-L2 (30%), jina-reranker-v1-turbo-en (20%), ms-marco-TinyBERT-L6 (20%), bge-reranker-base (20%)

### Chinese (zh)
- Average Accuracy: 12.2%
- Models with 100%: 0
- **Top 5:** ms-marco-MiniLM-L6-v2 (40%), ms-marco-MiniLM-L2-v2 (30%), ms-marco-MiniLM-L4-v2 (30%), ms-marco-TinyBERT-L2-v2 (20%), ms-marco-TinyBERT-L2 (20%)

## Multilingual Consistency

Models performing well across ALL languages:

| Rank | Model | Min | Max | Avg | Variance |
|------|-------|-----|-----|-----|----------|
| 1 🌍 | ms-marco-MiniLM-L2-v2 | 10.0% | 50.0% | 26.7% | 40.0% |
| 2  | ms-marco-TinyBERT-L2 | 10.0% | 40.0% | 23.3% | 30.0% |
| 3  | ms-marco-MiniLM-L4-v2 | 0.0% | 30.0% | 18.3% | 30.0% |
| 4  | ms-marco-MiniLM-L6-v2 | 0.0% | 40.0% | 16.7% | 40.0% |
| 5  | ms-marco-TinyBERT-L2-v2 | 0.0% | 20.0% | 15.0% | 20.0% |
| 6  | ms-marco-TinyBERT-L6 | 0.0% | 20.0% | 13.3% | 20.0% |
| 7  | jina-reranker-v1-turbo-en | 0.0% | 20.0% | 11.7% | 20.0% |
| 8  | jina-reranker-v1-tiny-en | 0.0% | 20.0% | 10.0% | 20.0% |
| 9  | bge-reranker-base | 0.0% | 20.0% | 8.3% | 20.0% |
| 10  | bge-reranker-large | 0.0% | 20.0% | 8.3% | 20.0% |

## Language Performance Matrix (Top 10)

| Model | English | French | German | Spanish | Arabic | Chinese |
|-------|-----|-----|-----|-----|-----|-----|
| ms-marco-MiniLM-L2-v2 | 20% | 50% | 10% | 20% | 30% | 30% |
| ms-marco-TinyBERT-L2 | 10% | 20% | 40% | 20% | 30% | 20% |
| ms-marco-MiniLM-L4-v2 | 0% | 30% | 30% | 20% | 0% | 30% |
| ms-marco-MiniLM-L6-v2 | 10% | 20% | 0% | 20% | 10% | 40% |
| ms-marco-TinyBERT-L2-v2 | 0% | 20% | 20% | 20% | 10% | 20% |
| ms-marco-TinyBERT-L6 | 20% | 0% | 10% | 10% | 20% | 20% |
| jina-reranker-v1-turbo-en | 0% | 10% | 10% | 10% | 20% | 20% |
| jina-reranker-v1-tiny-en | 0% | 10% | 10% | 10% | 10% | 20% |
| bge-reranker-base | 10% | 10% | 0% | 10% | 20% | 0% |
| bge-reranker-large | 0% | 10% | 20% | 10% | 10% | 0% |

## Key Findings

- **Speed Range:** 7ms (ms-marco-TinyBERT-L2) to 1408ms (Qwen3-Reranker-8B)
- **Size Range:** 5 MB (ms-marco-TinyBERT-L2) to 7.7 GB (Qwen3-Reranker-8B)
- **Language-Agnostic Models** (variance <10%): 5 models
