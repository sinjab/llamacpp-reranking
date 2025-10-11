# Multilingual Performance - Quantization Comparison

## Overview

This report compares multilingual performance across three quantization levels.

## Quantization Summary

| Quantization | Models | Avg Accuracy | Avg Time | Perfect 100% |
|--------------|--------|--------------|----------|---------------|
| F16 | 19 | 9.8% | 146ms | 0 |
| Q8_0 | 18 | 8.7% | 158ms | 0 |
| Q4_K_M | 18 | 8.4% | 167ms | 0 |

## Model Family Comparison

### Top Models Available in All Quantizations (18 models)

**ms-marco-MiniLM-L2-v2**

| Quant | Accuracy | Time | Size | Languages Tested |
|-------|----------|------|------|------------------|
| F16 | 26.7% | 8ms | 30 MB | 6 |
| Q8_0 | 26.7% | 8ms | 16 MB | 6 |
| Q4_K_M | 26.7% | 8ms | 15 MB | 6 |

**ms-marco-TinyBERT-L2**

| Quant | Accuracy | Time | Size | Languages Tested |
|-------|----------|------|------|------------------|
| F16 | 23.3% | 7ms | 9 MB | 6 |
| Q8_0 | 23.3% | 7ms | 5 MB | 6 |
| Q4_K_M | 25.0% | 8ms | 5 MB | 6 |

**ms-marco-MiniLM-L4-v2**

| Quant | Accuracy | Time | Size | Languages Tested |
|-------|----------|------|------|------------------|
| F16 | 18.3% | 11ms | 37 MB | 6 |
| Q8_0 | 18.3% | 11ms | 20 MB | 6 |
| Q4_K_M | 20.0% | 12ms | 18 MB | 6 |

**ms-marco-MiniLM-L6-v2**

| Quant | Accuracy | Time | Size | Languages Tested |
|-------|----------|------|------|------------------|
| F16 | 15.0% | 12ms | 44 MB | 6 |
| Q8_0 | 16.7% | 12ms | 24 MB | 6 |
| Q4_K_M | 13.3% | 12ms | 20 MB | 6 |

**ms-marco-TinyBERT-L2-v2**

| Quant | Accuracy | Time | Size | Languages Tested |
|-------|----------|------|------|------------------|
| F16 | 13.3% | 9ms | 9 MB | 6 |
| Q8_0 | 15.0% | 8ms | 5 MB | 6 |
| Q4_K_M | 13.3% | 7ms | 5 MB | 6 |

**jina-reranker-v1-turbo-en**

| Quant | Accuracy | Time | Size | Languages Tested |
|-------|----------|------|------|------------------|
| F16 | 11.7% | 13ms | 73 MB | 6 |
| Q8_0 | 11.7% | 13ms | 39 MB | 6 |
| Q4_K_M | 11.7% | 14ms | 34 MB | 6 |

**ms-marco-TinyBERT-L6**

| Quant | Accuracy | Time | Size | Languages Tested |
|-------|----------|------|------|------------------|
| F16 | 11.7% | 16ms | 128 MB | 6 |
| Q8_0 | 13.3% | 15ms | 69 MB | 6 |
| Q4_K_M | 8.3% | 16ms | 44 MB | 6 |

**bge-reranker-base**

| Quant | Accuracy | Time | Size | Languages Tested |
|-------|----------|------|------|------------------|
| F16 | 8.3% | 27ms | 537 MB | 6 |
| Q8_0 | 8.3% | 24ms | 289 MB | 6 |
| Q4_K_M | 10.0% | 25ms | 208 MB | 6 |

**bge-reranker-large**

| Quant | Accuracy | Time | Size | Languages Tested |
|-------|----------|------|------|------------------|
| F16 | 8.3% | 56ms | 1.1 GB | 6 |
| Q8_0 | 8.3% | 53ms | 576 MB | 6 |
| Q4_K_M | 8.3% | 55ms | 388 MB | 6 |

**jina-reranker-v1-tiny-en**

| Quant | Accuracy | Time | Size | Languages Tested |
|-------|----------|------|------|------------------|
| F16 | 8.3% | 16ms | 64 MB | 6 |
| Q8_0 | 10.0% | 10ms | 34 MB | 6 |
| Q4_K_M | 8.3% | 12ms | 31 MB | 6 |


## Quantization Impact by Language

### Arabic

| Quantization | Avg Accuracy | Best Model | Best Accuracy |
|--------------|--------------|------------|---------------|
| F16 | 5.3% | ms-marco-TinyBERT-L4 | 30% |
| Q8_0 | 3.9% | ms-marco-MiniLM-L2-v2 | 20% |
| Q4_K_M | 4.4% | bge-reranker-base | 20% |

### German

| Quantization | Avg Accuracy | Best Model | Best Accuracy |
|--------------|--------------|------------|---------------|
| F16 | 11.1% | ms-marco-MiniLM-L2-v2 | 50% |
| Q8_0 | 10.6% | ms-marco-MiniLM-L2-v2 | 50% |
| Q4_K_M | 8.9% | ms-marco-MiniLM-L2-v2 | 50% |

### English

| Quantization | Avg Accuracy | Best Model | Best Accuracy |
|--------------|--------------|------------|---------------|
| F16 | 8.9% | ms-marco-TinyBERT-L2 | 40% |
| Q8_0 | 8.3% | ms-marco-TinyBERT-L2 | 40% |
| Q4_K_M | 7.8% | ms-marco-MiniLM-L4-v2 | 30% |

### Spanish

| Quantization | Avg Accuracy | Best Model | Best Accuracy |
|--------------|--------------|------------|---------------|
| F16 | 8.9% | ms-marco-MiniLM-L2-v2 | 20% |
| Q8_0 | 8.3% | ms-marco-MiniLM-L2-v2 | 20% |
| Q4_K_M | 8.9% | bge-reranker-base | 20% |

### French

| Quantization | Avg Accuracy | Best Model | Best Accuracy |
|--------------|--------------|------------|---------------|
| F16 | 11.1% | ms-marco-TinyBERT-L4 | 60% |
| Q8_0 | 8.9% | ms-marco-MiniLM-L2-v2 | 30% |
| Q4_K_M | 8.9% | ms-marco-MiniLM-L2-v2 | 30% |

### Chinese

| Quantization | Avg Accuracy | Best Model | Best Accuracy |
|--------------|--------------|------------|---------------|
| F16 | 13.7% | ms-marco-MiniLM-L6-v2 | 40% |
| Q8_0 | 12.2% | ms-marco-MiniLM-L6-v2 | 40% |
| Q4_K_M | 11.7% | ms-marco-MiniLM-L4-v2 | 40% |


## Recommendations

### By Use Case:

**Production Deployment (Balanced):**
1. ms-marco-MiniLM-L2-v2 - 27%, 8ms, 15 MB
2. ms-marco-TinyBERT-L2 - 25%, 8ms, 5 MB
3. ms-marco-MiniLM-L4-v2 - 20%, 12ms, 18 MB

**Maximum Quality:**
1. ms-marco-TinyBERT-L4 - 35%, 11ms, 28 MB
2. ms-marco-MiniLM-L2-v2 - 27%, 8ms, 30 MB
3. ms-marco-TinyBERT-L2 - 23%, 7ms, 9 MB

**Balance (Q8):**
1. ms-marco-MiniLM-L2-v2 - 27%, 8ms, 16 MB
2. ms-marco-TinyBERT-L2 - 23%, 7ms, 5 MB
3. ms-marco-MiniLM-L4-v2 - 18%, 11ms, 20 MB
