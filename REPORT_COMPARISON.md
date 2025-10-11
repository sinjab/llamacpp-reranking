# Reranking Models - Quantization Comparison Report

## Overview

This report compares the performance of reranking models across three quantization levels:
- **F16**: Full 16-bit precision (highest quality, largest size)
- **Q8_0**: 8-bit quantization (middle ground)
- **Q4_K_M**: 4-bit quantization (smallest size, fastest)

## Quantization Impact Summary

| Quantization | Models | Avg Accuracy | Avg Speed | Avg Size | Perfect 100% |
|--------------|--------|--------------|-----------|----------|---------------|
| F16 | 19 | 66.3% | 148ms | 1.6 GB | 5 |
| Q8_0 | 18 | 69.4% | 165ms | 914 MB | 5 |
| Q4_K_M | 18 | 70.6% | 172ms | 553 MB | 6 |

## Model Family Performance Across Quantizations

### Models Available in All Quantizations (18 models)

**Qwen3-Reranker-4B**

| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |
|-------|----------|-------|------|-----------------|---------------|
| F16 | 100% | 727ms | 7.7 GB |  |  |
| Q8_0 | 100% | 742ms | 4.1 GB | (+0%) | (+2%) |
| Q4_K_M | 100% | 788ms | 2.4 GB | (+0%) | (+8%) |

**Qwen3-Reranker-8B**

| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |
|-------|----------|-------|------|-----------------|---------------|
| F16 | 100% | 1285ms | 14.4 GB |  |  |
| Q8_0 | 100% | 1438ms | 7.7 GB | (+0%) | (+12%) |
| Q4_K_M | 100% | 1484ms | 4.5 GB | (+0%) | (+15%) |

**bge-reranker-v2-m3**

| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |
|-------|----------|-------|------|-----------------|---------------|
| F16 | 100% | 63ms | 1.1 GB |  |  |
| Q8_0 | 100% | 69ms | 606 MB | (+0%) | (+10%) |
| Q4_K_M | 100% | 72ms | 418 MB | (+0%) | (+14%) |

**jina-reranker-v2-base-multilingual**

| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |
|-------|----------|-------|------|-----------------|---------------|
| F16 | 100% | 32ms | 539 MB |  |  |
| Q8_0 | 100% | 32ms | 291 MB | (+0%) | (-2%) |
| Q4_K_M | 100% | 38ms | 212 MB | (+0%) | (+17%) |

**ms-marco-MiniLM-L12-v2**

| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |
|-------|----------|-------|------|-----------------|---------------|
| F16 | 100% | 33ms | 64 MB |  |  |
| Q8_0 | 100% | 29ms | 34 MB | (+0%) | (-13%) |
| Q4_K_M | 100% | 29ms | 27 MB | (+0%) | (-12%) |

**Qwen3-Reranker-0.6B**

| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |
|-------|----------|-------|------|-----------------|---------------|
| F16 | 90% | 136ms | 1.1 GB |  |  |
| Q8_0 | 90% | 158ms | 609 MB | (+0%) | (+16%) |
| Q4_K_M | 100% | 165ms | 378 MB | (+10%) | (+21%) |

**mxbai-rerank-base-v2**

| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |
|-------|----------|-------|------|-----------------|---------------|
| F16 | 90% | 83ms | 948 MB |  |  |
| Q8_0 | 90% | 78ms | 506 MB | (+0%) | (-6%) |
| Q4_K_M | 90% | 80ms | 379 MB | (+0%) | (-4%) |

**mxbai-rerank-large-v2**

| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |
|-------|----------|-------|------|-----------------|---------------|
| F16 | 90% | 151ms | 3.0 GB |  |  |
| Q8_0 | 90% | 149ms | 1.6 GB | (+0%) | (-1%) |
| Q4_K_M | 90% | 164ms | 940 MB | (+0%) | (+9%) |

**bge-reranker-large**

| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |
|-------|----------|-------|------|-----------------|---------------|
| F16 | 80% | 63ms | 1.1 GB |  |  |
| Q8_0 | 80% | 71ms | 576 MB | (+0%) | (+13%) |
| Q4_K_M | 80% | 66ms | 388 MB | (+0%) | (+4%) |

**bge-reranker-base**

| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |
|-------|----------|-------|------|-----------------|---------------|
| F16 | 70% | 39ms | 537 MB |  |  |
| Q8_0 | 70% | 36ms | 289 MB | (+0%) | (-7%) |
| Q4_K_M | 70% | 38ms | 208 MB | (+0%) | (-1%) |


## Quantization Tradeoff Analysis

### Q4_K_M vs F16
- **Size Reduction**: ~60-70% smaller
- **Speed**: ~16% change
- **Accuracy Impact**: 4.2% change
- **Recommendation**: Best for production deployment - minimal accuracy loss with major size savings

### Q8_0 vs F16
- **Size Reduction**: ~45-50% smaller
- **Speed**: ~12% change
- **Accuracy Impact**: 3.1% change
- **Recommendation**: Middle ground for quality-sensitive applications


## Top Performer by Quantization Level

### F16 Winner: jina-reranker-v2-base-multilingual
- **Accuracy**: 100%
- **Speed**: 32ms
- **Size**: 539 MB

### Q8_0 Winner: ms-marco-MiniLM-L12-v2
- **Accuracy**: 100%
- **Speed**: 29ms
- **Size**: 34 MB

### Q4_K_M Winner: ms-marco-MiniLM-L12-v2
- **Accuracy**: 100%
- **Speed**: 29ms
- **Size**: 27 MB


## Final Recommendations

### When to Use Each Quantization:

**F16 (Full Precision)**
- Research and benchmarking
- Maximum accuracy requirements
- When storage is not a concern
- Model evaluation and comparison

**Q8_0 (8-bit)**
- Quality-sensitive production systems
- When slight accuracy drop is acceptable
- Moderate storage constraints
- Server deployments with good hardware

**Q4_K_M (4-bit)** ⭐ **RECOMMENDED**
- General production deployment
- Edge devices and mobile
- Cost-optimized cloud deployment
- Best balance of speed, size, and accuracy
- Minimal accuracy loss for most models


## Key Insights

- **5 models maintain 100% accuracy across ALL quantizations**: Qwen3-Reranker-4B, Qwen3-Reranker-8B, bge-reranker-v2-m3, jina-reranker-v2-base-multilingual, ms-marco-MiniLM-L12-v2
- **Models significantly affected by quantization** (>10% drop): ms-marco-TinyBERT-L6 (20%)
- **Total storage savings** (Q4_K_M vs F16): 20.4 GB saved (68% reduction)
