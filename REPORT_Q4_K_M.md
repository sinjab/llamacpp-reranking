# Reranking Models Benchmark Report - Q4_K_M Quantization

## Executive Summary

**Tests Completed:** 180 (18 models × 10 domains)
**Overall Accuracy:** 70.6%
**Average Response Time:** 172ms
**Total Storage:** 10.0 GB
**Perfect Accuracy Models:** 6

## Performance Rankings

### Top 10 Models by Accuracy
1. **ms-marco-MiniLM-L12-v2** 🏆
   - Accuracy: 100% (10/10)
   - Speed: 29ms (range: 16ms-53ms)
   - Size: 27 MB

2. **jina-reranker-v2-base-multilingual** ⭐
   - Accuracy: 100% (10/10)
   - Speed: 38ms (range: 23ms-82ms)
   - Size: 212 MB

3. **bge-reranker-v2-m3** ⭐
   - Accuracy: 100% (10/10)
   - Speed: 72ms (range: 52ms-118ms)
   - Size: 418 MB

4. **Qwen3-Reranker-0.6B** 
   - Accuracy: 100% (10/10)
   - Speed: 165ms (range: 157ms-175ms)
   - Size: 378 MB

5. **Qwen3-Reranker-4B** 
   - Accuracy: 100% (10/10)
   - Speed: 788ms (range: 765ms-851ms)
   - Size: 2.4 GB

6. **Qwen3-Reranker-8B** 
   - Accuracy: 100% (10/10)
   - Speed: 1484ms (range: 1381ms-1678ms)
   - Size: 4.5 GB

7. **mxbai-rerank-base-v2** 
   - Accuracy: 90% (9/10)
   - Speed: 80ms (range: 72ms-91ms)
   - Size: 379 MB

8. **mxbai-rerank-large-v2** 
   - Accuracy: 90% (9/10)
   - Speed: 164ms (range: 154ms-187ms)
   - Size: 940 MB

9. **bge-reranker-large** 
   - Accuracy: 80% (8/10)
   - Speed: 66ms (range: 53ms-106ms)
   - Size: 388 MB

10. **ms-marco-MiniLM-L4-v2** 
   - Accuracy: 70% (7/10)
   - Speed: 18ms (range: 10ms-38ms)
   - Size: 18 MB


### Top 5 Fastest Models

1. **ms-marco-TinyBERT-L2-v2** - 16ms (20% accuracy, 5 MB)
2. **ms-marco-TinyBERT-L2** - 16ms (10% accuracy, 5 MB)
3. **ms-marco-MiniLM-L4-v2** - 18ms (70% accuracy, 18 MB)
4. **ms-marco-MiniLM-L2-v2** - 19ms (40% accuracy, 15 MB)
5. **ms-marco-MiniLM-L6-v2** - 22ms (60% accuracy, 20 MB)

### Top 5 Smallest Models

1. **ms-marco-TinyBERT-L2-v2** - 5 MB (20% accuracy, 16ms)
2. **ms-marco-TinyBERT-L2** - 5 MB (10% accuracy, 16ms)
3. **ms-marco-MiniLM-L2-v2** - 15 MB (40% accuracy, 19ms)
4. **ms-marco-MiniLM-L4-v2** - 18 MB (70% accuracy, 18ms)
5. **ms-marco-MiniLM-L6-v2** - 20 MB (60% accuracy, 22ms)

## Perfect Accuracy Models (100%)

**ms-marco-MiniLM-L12-v2**
- Speed: 29ms | Size: 27 MB
- Best for: Resource-constrained environments

**jina-reranker-v2-base-multilingual**
- Speed: 38ms | Size: 212 MB
- Best for: Low-latency applications

**bge-reranker-v2-m3**
- Speed: 72ms | Size: 418 MB
- Best for: Low-latency applications

**Qwen3-Reranker-0.6B**
- Speed: 165ms | Size: 378 MB
- Best for: Balanced performance

**Qwen3-Reranker-4B**
- Speed: 788ms | Size: 2.4 GB
- Best for: Maximum quality requirements

**Qwen3-Reranker-8B**
- Speed: 1484ms | Size: 4.5 GB
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
- **ms-marco-MiniLM-L4-v2**: 18ms, 70% accuracy

### Edge Deployment (Small Size)

### Production RAG (Balanced)
- **ms-marco-MiniLM-L12-v2**: 100% accuracy, 29ms, 27 MB
- **jina-reranker-v2-base-multilingual**: 100% accuracy, 38ms, 212 MB
- **bge-reranker-v2-m3**: 100% accuracy, 72ms, 418 MB

### Maximum Accuracy (Quality Focus)
- **ms-marco-MiniLM-L12-v2**: 100% accuracy, 29ms, 27 MB
- **jina-reranker-v2-base-multilingual**: 100% accuracy, 38ms, 212 MB
- **bge-reranker-v2-m3**: 100% accuracy, 72ms, 418 MB

## Key Findings

- **Speed Range**: 16ms (ms-marco-TinyBERT-L2) to 1484ms (Qwen3-Reranker-8B)
- **Size Range**: 5 MB (ms-marco-TinyBERT-L2) to 4.5 GB (Qwen3-Reranker-8B)
- **Accuracy Distribution**: 8 models ≥90%, 9 models ≥80%, 5 models <50%
- **Best Value**: ms-marco-MiniLM-L12-v2 achieves 100% in only 27 MB
