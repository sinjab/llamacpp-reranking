# Multilingual Reranking Benchmark - F16 Quantization

## Executive Summary

**Quantization:** F16
**Tests Completed:** 1140
**Models Tested:** 19
**Languages:** 6 (English, French, German, Spanish, Arabic, Chinese)
**Domains per Language:** 10

**Overall Accuracy:** 9.8%
**Average Response Time:** 146ms
**Total Storage:** 30.9 GB

**Perfect Accuracy Models (100%):** 0

## Top 10 Models - Overall Performance

| Rank | Model | Accuracy | Avg Time | Size | Queries |
|------|-------|----------|----------|------|----------|
| 1 🏆 | ms-marco-TinyBERT-L4 | 35.0% | 11ms | 28 MB | 21/60 |
| 2 ⭐ | ms-marco-MiniLM-L2-v2 | 26.7% | 8ms | 30 MB | 16/60 |
| 3 ⭐ | ms-marco-TinyBERT-L2 | 23.3% | 7ms | 9 MB | 14/60 |
| 4  | ms-marco-MiniLM-L4-v2 | 18.3% | 11ms | 37 MB | 11/60 |
| 5  | ms-marco-MiniLM-L6-v2 | 15.0% | 12ms | 44 MB | 9/60 |
| 6  | ms-marco-TinyBERT-L2-v2 | 13.3% | 9ms | 9 MB | 8/60 |
| 7  | jina-reranker-v1-turbo-en | 11.7% | 13ms | 73 MB | 7/60 |
| 8  | ms-marco-TinyBERT-L6 | 11.7% | 16ms | 128 MB | 7/60 |
| 9  | jina-reranker-v1-tiny-en | 8.3% | 16ms | 64 MB | 5/60 |
| 10  | bge-reranker-base | 8.3% | 27ms | 537 MB | 5/60 |

## Performance by Language

### Arabic (ar)
- Average Accuracy: 5.3%
- Models with 100%: 0
- **Top 5:** ms-marco-TinyBERT-L4 (30%), ms-marco-MiniLM-L2-v2 (20%), ms-marco-TinyBERT-L6 (20%), ms-marco-TinyBERT-L2 (10%), ms-marco-MiniLM-L6-v2 (10%)

### German (de)
- Average Accuracy: 11.1%
- Models with 100%: 0
- **Top 5:** ms-marco-MiniLM-L2-v2 (50%), ms-marco-TinyBERT-L4 (40%), ms-marco-MiniLM-L4-v2 (30%), ms-marco-TinyBERT-L2 (20%), ms-marco-TinyBERT-L2-v2 (20%)

### English (en)
- Average Accuracy: 8.9%
- Models with 100%: 0
- **Top 5:** ms-marco-TinyBERT-L2 (40%), ms-marco-TinyBERT-L4 (30%), ms-marco-MiniLM-L4-v2 (30%), bge-reranker-large (20%), ms-marco-TinyBERT-L2-v2 (10%)

### Spanish (es)
- Average Accuracy: 8.9%
- Models with 100%: 0
- **Top 5:** ms-marco-TinyBERT-L2 (20%), ms-marco-MiniLM-L2-v2 (20%), ms-marco-MiniLM-L4-v2 (20%), ms-marco-TinyBERT-L2-v2 (20%), ms-marco-TinyBERT-L4 (20%)

### French (fr)
- Average Accuracy: 11.1%
- Models with 100%: 0
- **Top 5:** ms-marco-TinyBERT-L4 (60%), ms-marco-MiniLM-L2-v2 (30%), ms-marco-TinyBERT-L2 (30%), jina-reranker-v1-turbo-en (20%), bge-reranker-base (20%)

### Chinese (zh)
- Average Accuracy: 13.7%
- Models with 100%: 0
- **Top 5:** ms-marco-MiniLM-L6-v2 (40%), ms-marco-MiniLM-L2-v2 (30%), ms-marco-MiniLM-L4-v2 (30%), ms-marco-TinyBERT-L4 (30%), ms-marco-TinyBERT-L2 (20%)

## Multilingual Consistency

Models performing well across ALL languages:

| Rank | Model | Min | Max | Avg | Variance |
|------|-------|-----|-----|-----|----------|
| 1 🌍 | ms-marco-TinyBERT-L4 | 20.0% | 60.0% | 35.0% | 40.0% |
| 2  | ms-marco-MiniLM-L2-v2 | 10.0% | 50.0% | 26.7% | 40.0% |
| 3  | ms-marco-TinyBERT-L2 | 10.0% | 40.0% | 23.3% | 30.0% |
| 4  | ms-marco-MiniLM-L4-v2 | 0.0% | 30.0% | 18.3% | 30.0% |
| 5  | ms-marco-MiniLM-L6-v2 | 0.0% | 40.0% | 15.0% | 40.0% |
| 6  | ms-marco-TinyBERT-L2-v2 | 0.0% | 20.0% | 13.3% | 20.0% |
| 7  | jina-reranker-v1-turbo-en | 0.0% | 20.0% | 11.7% | 20.0% |
| 8  | ms-marco-TinyBERT-L6 | 0.0% | 20.0% | 11.7% | 20.0% |
| 9  | bge-reranker-base | 0.0% | 20.0% | 8.3% | 20.0% |
| 10  | bge-reranker-large | 0.0% | 20.0% | 8.3% | 20.0% |

## Language Performance Matrix (Top 10)

| Model | English | French | German | Spanish | Arabic | Chinese |
|-------|-----|-----|-----|-----|-----|-----|
| ms-marco-TinyBERT-L4 | 30% | 40% | 30% | 20% | 60% | 30% |
| ms-marco-MiniLM-L2-v2 | 20% | 50% | 10% | 20% | 30% | 30% |
| ms-marco-TinyBERT-L2 | 10% | 20% | 40% | 20% | 30% | 20% |
| ms-marco-MiniLM-L4-v2 | 0% | 30% | 30% | 20% | 0% | 30% |
| ms-marco-MiniLM-L6-v2 | 10% | 10% | 0% | 20% | 10% | 40% |
| ms-marco-TinyBERT-L2-v2 | 0% | 20% | 10% | 20% | 10% | 20% |
| jina-reranker-v1-turbo-en | 0% | 10% | 10% | 10% | 20% | 20% |
| ms-marco-TinyBERT-L6 | 20% | 0% | 10% | 10% | 10% | 20% |
| jina-reranker-v1-tiny-en | 0% | 0% | 10% | 10% | 10% | 20% |
| bge-reranker-base | 10% | 10% | 0% | 10% | 20% | 0% |

## Key Findings

- **Speed Range:** 7ms (ms-marco-TinyBERT-L2) to 1364ms (Qwen3-Reranker-8B)
- **Size Range:** 9 MB (ms-marco-TinyBERT-L2) to 14.4 GB (Qwen3-Reranker-8B)
- **Language-Agnostic Models** (variance <10%): 4 models
