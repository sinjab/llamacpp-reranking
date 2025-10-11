# Reranking Models Benchmark Report - F16 Quantization

## Executive Summary

**Tests Completed:** 190 (19 models × 10 domains)
**Overall Accuracy:** 66.3%
**Average Response Time:** 148ms
**Total Storage:** 30.9 GB
**Perfect Accuracy Models:** 5

## Performance Rankings

### Top 10 Models by Accuracy
1. **jina-reranker-v2-base-multilingual** 🏆
   - Accuracy: 100% (10/10)
   - Speed: 32ms (range: 23ms-74ms)
   - Size: 539 MB

2. **ms-marco-MiniLM-L12-v2** ⭐
   - Accuracy: 100% (10/10)
   - Speed: 33ms (range: 22ms-57ms)
   - Size: 64 MB

3. **bge-reranker-v2-m3** ⭐
   - Accuracy: 100% (10/10)
   - Speed: 63ms (range: 54ms-94ms)
   - Size: 1.1 GB

4. **Qwen3-Reranker-4B** 
   - Accuracy: 100% (10/10)
   - Speed: 727ms (range: 707ms-784ms)
   - Size: 7.7 GB

5. **Qwen3-Reranker-8B** 
   - Accuracy: 100% (10/10)
   - Speed: 1285ms (range: 1241ms-1407ms)
   - Size: 14.4 GB

6. **mxbai-rerank-base-v2** 
   - Accuracy: 90% (9/10)
   - Speed: 83ms (range: 80ms-95ms)
   - Size: 948 MB

7. **Qwen3-Reranker-0.6B** 
   - Accuracy: 90% (9/10)
   - Speed: 136ms (range: 129ms-161ms)
   - Size: 1.1 GB

8. **mxbai-rerank-large-v2** 
   - Accuracy: 90% (9/10)
   - Speed: 151ms (range: 145ms-183ms)
   - Size: 3.0 GB

9. **bge-reranker-large** 
   - Accuracy: 80% (8/10)
   - Speed: 63ms (range: 53ms-101ms)
   - Size: 1.1 GB

10. **jina-reranker-v1-tiny-en** 
   - Accuracy: 70% (7/10)
   - Speed: 27ms (range: 10ms-47ms)
   - Size: 64 MB


### Top 5 Fastest Models

1. **ms-marco-TinyBERT-L2-v2** - 16ms (10% accuracy, 9 MB)
2. **ms-marco-TinyBERT-L2** - 16ms (20% accuracy, 9 MB)
3. **ms-marco-MiniLM-L2-v2** - 19ms (40% accuracy, 30 MB)
4. **ms-marco-TinyBERT-L4** - 20ms (0% accuracy, 28 MB)
5. **ms-marco-MiniLM-L6-v2** - 20ms (50% accuracy, 44 MB)

### Top 5 Smallest Models

1. **ms-marco-TinyBERT-L2** - 9 MB (20% accuracy, 16ms)
2. **ms-marco-TinyBERT-L2-v2** - 9 MB (10% accuracy, 16ms)
3. **ms-marco-TinyBERT-L4** - 28 MB (0% accuracy, 20ms)
4. **ms-marco-MiniLM-L2-v2** - 30 MB (40% accuracy, 19ms)
5. **ms-marco-MiniLM-L4-v2** - 37 MB (60% accuracy, 26ms)

## Perfect Accuracy Models (100%)

**jina-reranker-v2-base-multilingual**
- Speed: 32ms | Size: 539 MB
- Best for: Low-latency applications

**ms-marco-MiniLM-L12-v2**
- Speed: 33ms | Size: 64 MB
- Best for: Resource-constrained environments

**bge-reranker-v2-m3**
- Speed: 63ms | Size: 1.1 GB
- Best for: Low-latency applications

**Qwen3-Reranker-4B**
- Speed: 727ms | Size: 7.7 GB
- Best for: Maximum quality requirements

**Qwen3-Reranker-8B**
- Speed: 1285ms | Size: 14.4 GB
- Best for: Maximum quality requirements

## Domain Performance Analysis - jina-reranker-v2-base-multilingual

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
- **jina-reranker-v2-base-multilingual**: 100% accuracy, 32ms, 539 MB
- **ms-marco-MiniLM-L12-v2**: 100% accuracy, 33ms, 64 MB
- **mxbai-rerank-base-v2**: 90% accuracy, 83ms, 948 MB

### Maximum Accuracy (Quality Focus)
- **jina-reranker-v2-base-multilingual**: 100% accuracy, 32ms, 539 MB
- **ms-marco-MiniLM-L12-v2**: 100% accuracy, 33ms, 64 MB
- **bge-reranker-v2-m3**: 100% accuracy, 63ms, 1.1 GB

## Key Findings

- **Speed Range**: 16ms (ms-marco-TinyBERT-L2-v2) to 1285ms (Qwen3-Reranker-8B)
- **Size Range**: 9 MB (ms-marco-TinyBERT-L2) to 14.4 GB (Qwen3-Reranker-8B)
- **Accuracy Distribution**: 8 models ≥90%, 9 models ≥80%, 5 models <50%
- **Best Value**: ms-marco-MiniLM-L12-v2 achieves 100% in only 64 MB
