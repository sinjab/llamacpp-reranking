# Multilingual Reranking Benchmark - Q4_K_M Quantization

## Executive Summary

**Quantization:** Q4_K_M
**Tests Completed:** 1080
**Models Tested:** 18
**Languages:** 6 (English, French, German, Spanish, Arabic, Chinese)
**Domains per Language:** 10

**Overall Accuracy:** 8.4%
**Average Response Time:** 167ms
**Total Storage:** 10.0 GB

**Perfect Accuracy Models (100%):** 0

## Top 10 Models - Overall Performance

| Rank | Model | Accuracy | Avg Time | Size | Queries |
|------|-------|----------|----------|------|----------|
| 1 🏆 | ms-marco-MiniLM-L2-v2 | 26.7% | 8ms | 15 MB | 16/60 |
| 2 ⭐ | ms-marco-TinyBERT-L2 | 25.0% | 8ms | 5 MB | 15/60 |
| 3 ⭐ | ms-marco-MiniLM-L4-v2 | 20.0% | 12ms | 18 MB | 12/60 |
| 4  | ms-marco-TinyBERT-L2-v2 | 13.3% | 7ms | 5 MB | 8/60 |
| 5  | ms-marco-MiniLM-L6-v2 | 13.3% | 12ms | 20 MB | 8/60 |
| 6  | jina-reranker-v1-turbo-en | 11.7% | 14ms | 34 MB | 7/60 |
| 7  | bge-reranker-base | 10.0% | 25ms | 208 MB | 6/60 |
| 8  | jina-reranker-v1-tiny-en | 8.3% | 12ms | 31 MB | 5/60 |
| 9  | ms-marco-TinyBERT-L6 | 8.3% | 16ms | 44 MB | 5/60 |
| 10  | bge-reranker-large | 8.3% | 55ms | 388 MB | 5/60 |

## Performance by Language

### Arabic (ar)
- Average Accuracy: 4.4%
- Models with 100%: 0
- **Top 5:** ms-marco-TinyBERT-L2 (20%), ms-marco-MiniLM-L2-v2 (20%), bge-reranker-base (20%), ms-marco-MiniLM-L6-v2 (10%), ms-marco-TinyBERT-L6 (10%)

### German (de)
- Average Accuracy: 8.9%
- Models with 100%: 0
- **Top 5:** ms-marco-MiniLM-L2-v2 (50%), ms-marco-MiniLM-L4-v2 (30%), ms-marco-TinyBERT-L2-v2 (20%), ms-marco-TinyBERT-L2 (20%), ms-marco-MiniLM-L6-v2 (10%)

### English (en)
- Average Accuracy: 7.8%
- Models with 100%: 0
- **Top 5:** ms-marco-MiniLM-L4-v2 (30%), ms-marco-TinyBERT-L2 (30%), ms-marco-MiniLM-L2-v2 (20%), ms-marco-TinyBERT-L2-v2 (10%), jina-reranker-v1-tiny-en (10%)

### Spanish (es)
- Average Accuracy: 8.9%
- Models with 100%: 0
- **Top 5:** ms-marco-TinyBERT-L2-v2 (20%), ms-marco-TinyBERT-L2 (20%), ms-marco-MiniLM-L2-v2 (20%), ms-marco-MiniLM-L4-v2 (20%), ms-marco-MiniLM-L6-v2 (20%)

### French (fr)
- Average Accuracy: 8.9%
- Models with 100%: 0
- **Top 5:** ms-marco-MiniLM-L2-v2 (30%), ms-marco-TinyBERT-L2 (30%), jina-reranker-v1-turbo-en (20%), bge-reranker-base (20%), bge-reranker-large (20%)

### Chinese (zh)
- Average Accuracy: 11.7%
- Models with 100%: 0
- **Top 5:** ms-marco-MiniLM-L4-v2 (40%), ms-marco-TinyBERT-L2 (30%), ms-marco-MiniLM-L6-v2 (30%), ms-marco-TinyBERT-L2-v2 (20%), ms-marco-MiniLM-L2-v2 (20%)

## Multilingual Consistency

Models performing well across ALL languages:

| Rank | Model | Min | Max | Avg | Variance |
|------|-------|-----|-----|-----|----------|
| 1 🌍 | ms-marco-MiniLM-L2-v2 | 20.0% | 50.0% | 26.7% | 30.0% |
| 2  | ms-marco-TinyBERT-L2 | 20.0% | 30.0% | 25.0% | 10.0% |
| 3  | ms-marco-MiniLM-L4-v2 | 0.0% | 40.0% | 20.0% | 40.0% |
| 4  | ms-marco-MiniLM-L6-v2 | 0.0% | 30.0% | 13.3% | 30.0% |
| 5  | ms-marco-TinyBERT-L2-v2 | 0.0% | 20.0% | 13.3% | 20.0% |
| 6  | jina-reranker-v1-turbo-en | 0.0% | 20.0% | 11.7% | 20.0% |
| 7  | bge-reranker-base | 0.0% | 20.0% | 10.0% | 20.0% |
| 8  | bge-reranker-large | 0.0% | 20.0% | 8.3% | 20.0% |
| 9  | jina-reranker-v1-tiny-en | 0.0% | 20.0% | 8.3% | 20.0% |
| 10  | ms-marco-TinyBERT-L6 | 0.0% | 10.0% | 8.3% | 10.0% |

## Language Performance Matrix (Top 10)

| Model | English | French | German | Spanish | Arabic | Chinese |
|-------|-----|-----|-----|-----|-----|-----|
| ms-marco-MiniLM-L2-v2 | 20% | 50% | 20% | 20% | 30% | 20% |
| ms-marco-TinyBERT-L2 | 20% | 20% | 30% | 20% | 30% | 30% |
| ms-marco-MiniLM-L4-v2 | 0% | 30% | 30% | 20% | 0% | 40% |
| ms-marco-TinyBERT-L2-v2 | 0% | 20% | 10% | 20% | 10% | 20% |
| ms-marco-MiniLM-L6-v2 | 10% | 10% | 0% | 20% | 10% | 30% |
| jina-reranker-v1-turbo-en | 0% | 10% | 10% | 10% | 20% | 20% |
| bge-reranker-base | 20% | 0% | 0% | 20% | 20% | 0% |
| jina-reranker-v1-tiny-en | 0% | 0% | 10% | 10% | 10% | 20% |
| ms-marco-TinyBERT-L6 | 10% | 0% | 10% | 10% | 10% | 10% |
| bge-reranker-large | 0% | 10% | 10% | 10% | 20% | 0% |

## Key Findings

- **Speed Range:** 7ms (ms-marco-TinyBERT-L2-v2) to 1464ms (Qwen3-Reranker-8B)
- **Size Range:** 5 MB (ms-marco-TinyBERT-L2) to 4.5 GB (Qwen3-Reranker-8B)
- **Language-Agnostic Models** (variance <10%): 5 models
