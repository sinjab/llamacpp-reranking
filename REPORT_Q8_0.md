# Reranking Models Benchmark Report - Q8_0 Quantization

## Executive Summary

**Tests Completed:** 180 (18 models × 10 domains)
**Overall Accuracy:** 69.4%
**Average Response Time:** 165ms
**Total Storage:** 16.5 GB
**Perfect Accuracy Models:** 5

## Performance Rankings

### Top 10 Models by Accuracy
1. **ms-marco-MiniLM-L12-v2** 🏆
   - Accuracy: 100% (10/10)
   - Speed: 29ms (range: 15ms-54ms)
   - Size: 34 MB

2. **jina-reranker-v2-base-multilingual** ⭐
   - Accuracy: 100% (10/10)
   - Speed: 32ms (range: 21ms-75ms)
   - Size: 291 MB

3. **bge-reranker-v2-m3** ⭐
   - Accuracy: 100% (10/10)
   - Speed: 69ms (range: 51ms-131ms)
   - Size: 606 MB

4. **Qwen3-Reranker-4B** 
   - Accuracy: 100% (10/10)
   - Speed: 742ms (range: 726ms-793ms)
   - Size: 4.1 GB

5. **Qwen3-Reranker-8B** 
   - Accuracy: 100% (10/10)
   - Speed: 1438ms (range: 1345ms-1608ms)
   - Size: 7.7 GB

6. **mxbai-rerank-base-v2** 
   - Accuracy: 90% (9/10)
   - Speed: 78ms (range: 74ms-86ms)
   - Size: 506 MB

7. **mxbai-rerank-large-v2** 
   - Accuracy: 90% (9/10)
   - Speed: 149ms (range: 142ms-188ms)
   - Size: 1.6 GB

8. **Qwen3-Reranker-0.6B** 
   - Accuracy: 90% (9/10)
   - Speed: 158ms (range: 149ms-170ms)
   - Size: 609 MB

9. **bge-reranker-large** 
   - Accuracy: 80% (8/10)
   - Speed: 71ms (range: 50ms-145ms)
   - Size: 576 MB

10. **jina-reranker-v1-tiny-en** 
   - Accuracy: 70% (7/10)
   - Speed: 26ms (range: 9ms-67ms)
   - Size: 34 MB


### Top 5 Fastest Models

1. **ms-marco-TinyBERT-L2-v2** - 15ms (10% accuracy, 5 MB)
2. **ms-marco-TinyBERT-L2** - 16ms (20% accuracy, 5 MB)
3. **ms-marco-MiniLM-L2-v2** - 19ms (40% accuracy, 16 MB)
4. **ms-marco-MiniLM-L4-v2** - 22ms (60% accuracy, 20 MB)
5. **ms-marco-MiniLM-L6-v2** - 22ms (40% accuracy, 24 MB)

### Top 5 Smallest Models

1. **ms-marco-TinyBERT-L2** - 5 MB (20% accuracy, 16ms)
2. **ms-marco-TinyBERT-L2-v2** - 5 MB (10% accuracy, 15ms)
3. **ms-marco-MiniLM-L2-v2** - 16 MB (40% accuracy, 19ms)
4. **ms-marco-MiniLM-L4-v2** - 20 MB (60% accuracy, 22ms)
5. **ms-marco-MiniLM-L6-v2** - 24 MB (40% accuracy, 22ms)

## Perfect Accuracy Models (100%)

**ms-marco-MiniLM-L12-v2**
- Speed: 29ms | Size: 34 MB
- Best for: Resource-constrained environments

**jina-reranker-v2-base-multilingual**
- Speed: 32ms | Size: 291 MB
- Best for: Low-latency applications

**bge-reranker-v2-m3**
- Speed: 69ms | Size: 606 MB
- Best for: Low-latency applications

**Qwen3-Reranker-4B**
- Speed: 742ms | Size: 4.1 GB
- Best for: Maximum quality requirements

**Qwen3-Reranker-8B**
- Speed: 1438ms | Size: 7.7 GB
- Best for: Maximum quality requirements

## Domain Performance Analysis - ms-marco-MiniLM-L12-v2

| Domain | Accuracy |
|--------|----------|
| Geography | 100% |
| Technology | 100% |
| Medicine | 100% |
| Law | 100% |
| Cooking | 100% |
| Finance | 100% |
| History | 100% |
| Sports | 100% |
| Literature | 100% |
| Science | 100% |

## Use Case Recommendations

### Real-Time Search (Low Latency)

### Edge Deployment (Small Size)

### Production RAG (Balanced)
- **ms-marco-MiniLM-L12-v2**: 100% accuracy, 29ms, 34 MB
- **jina-reranker-v2-base-multilingual**: 100% accuracy, 32ms, 291 MB
- **bge-reranker-v2-m3**: 100% accuracy, 69ms, 606 MB

### Maximum Accuracy (Quality Focus)
- **ms-marco-MiniLM-L12-v2**: 100% accuracy, 29ms, 34 MB
- **jina-reranker-v2-base-multilingual**: 100% accuracy, 32ms, 291 MB
- **bge-reranker-v2-m3**: 100% accuracy, 69ms, 606 MB

## Key Findings

- **Speed Range**: 15ms (ms-marco-TinyBERT-L2-v2) to 1438ms (Qwen3-Reranker-8B)
- **Size Range**: 5 MB (ms-marco-TinyBERT-L2) to 7.7 GB (Qwen3-Reranker-8B)
- **Accuracy Distribution**: 8 models ≥90%, 9 models ≥80%, 5 models <50%
- **Best Value**: ms-marco-MiniLM-L12-v2 achieves 100% in only 34 MB
