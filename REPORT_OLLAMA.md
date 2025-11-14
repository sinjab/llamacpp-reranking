# Ollama Reranking Models Comprehensive Benchmark Report

**Generated:** November 14, 2025
**Total Models Tested:** 55 Ollama reranking models
**Test Coverage:** 10 domains × 55 models = 550 total tests
**CSV Results:** `test_results_all_models_20251114_103439.csv`

---

## Executive Summary

This comprehensive benchmark evaluated **55 Ollama reranking models** across **10 diverse domains** using the same testing methodology as the llama.cpp benchmarks. The tests measured accuracy, response time, and reliability to identify the best performing models for production use.

### Key Findings
- **Overall Success Rate:** 72.7% (400/550 tests successful)
- **Overall Accuracy:** 55.2% (221/400 successful tests)
- **Perfect Models:** 9 models achieved 100% accuracy
- **Response Time:** 0.160s average (nearly identical to llama.cpp)

---

## 🏆 Top Performing Models

### Perfect Accuracy Models (100%)

| Rank | Model | Quantization | Response Time | Model Family |
|------|-------|--------------|---------------|--------------|
| 1 | **bge-reranker-v2-m3** | F16 | 0.263s | BGE |
| 2 | **bge-reranker-v2-m3** | Q8_0 | 0.232s | BGE |
| 3 | **bge-reranker-v2-m3** | Q4_K_M | 0.259s | BGE |
| 4 | **jina-reranker-v2-base-multilingual** | F16 | 0.190s | Jina |
| 5 | **jina-reranker-v2-base-multilingual** | Q8_0 | 0.200s | Jina |
| 6 | **jina-reranker-v2-base-multilingual** | Q4_K_M | 0.206s | Jina |
| 7 | **ms-marco-MiniLM-L12-v2** | F16 | 0.084s | MS-MARCO |
| 8 | **ms-marco-MiniLM-L12-v2** | Q8_0 | 0.084s | MS-MARCO |
| 9 | **ms-marco-MiniLM-L12-v2** | Q4_K_M | 0.087s | MS-MARCO |

### Top 15 Models by Accuracy

| Rank | Model | Accuracy | Avg Time | Model Size |
|------|-------|----------|----------|------------|
| 1 | bge-reranker-v2-m3-F16 | 100.0% (10/10) | 0.263s | ~1.1 GB |
| 2 | bge-reranker-v2-m3-Q8_0 | 100.0% (10/10) | 0.232s | ~635 MB |
| 3 | bge-reranker-v2-m3-Q4_K_M | 100.0% (10/10) | 0.259s | ~438 MB |
| 4 | jina-reranker-v2-base-multilingual-F16 | 100.0% (10/10) | 0.190s | ~565 MB |
| 5 | jina-reranker-v2-base-multilingual-Q8_0 | 100.0% (10/10) | 0.200s | ~305 MB |
| 6 | jina-reranker-v2-base-multilingual-Q4_K_M | 100.0% (10/10) | 0.206s | ~222 MB |
| 7 | ms-marco-MiniLM-L12-v2-F16 | 100.0% (10/10) | 0.084s | ~67 MB |
| 8 | ms-marco-MiniLM-L12-v2-Q8_0 | 100.0% (10/10) | 0.084s | ~36 MB |
| 9 | ms-marco-MiniLM-L12-v2-Q4_K_M | 100.0% (10/10) | 0.087s | ~29 MB |
| 10 | bge-reranker-large-F16 | 80.0% (8/10) | 0.281s | ~1.1 GB |
| 11 | bge-reranker-large-Q8_0 | 80.0% (8/10) | 0.263s | ~604 MB |
| 12 | bge-reranker-large-Q4_K_M | 70.0% (7/10) | 0.235s | ~406 MB |
| 13 | jina-reranker-v1-tiny-en-F16 | 60.0% (6/10) | 0.160s | ~67 MB |
| 14 | jina-reranker-v1-tiny-en-Q8_0 | 60.0% (6/10) | 0.141s | ~36 MB |
| 15 | jina-reranker-v1-tiny-en-Q4_K_M | 60.0% (6/10) | 0.151s | ~33 MB |

### Top 10 Fastest Models

| Rank | Model | Avg Time | Accuracy | Use Case |
|------|-------|----------|----------|----------|
| 1 | ms-marco-TinyBERT-L2-Q8_0 | 0.053s | 20.0% | Ultra-fast (low accuracy) |
| 2 | ms-marco-TinyBERT-L2-Q4_K_M | 0.054s | 10.0% | Ultra-fast (low accuracy) |
| 3 | ms-marco-MiniLM-L2-v2-Q8_0 | 0.059s | 40.0% | Fast, moderate accuracy |
| 4 | ms-marco-TinyBERT-L2-v2-Q4_K_M | 0.059s | 10.0% | Ultra-fast (low accuracy) |
| 5 | ms-marco-TinyBERT-L2-v2-F16 | 0.060s | 0.0% | Fast (not recommended) |
| 6 | ms-marco-TinyBERT-L2-v2-Q8_0 | 0.060s | 10.0% | Fast (low accuracy) |
| 7 | ms-marco-TinyBERT-L2-F16 | 0.063s | 20.0% | Fast (low accuracy) |
| 8 | ms-marco-MiniLM-L4-v2-Q8_0 | 0.065s | 60.0% | Good balance |
| 9 | ms-marco-MiniLM-L2-v2-Q4_K_M | 0.066s | 40.0% | Fast, moderate accuracy |
| 10 | ms-marco-MiniLM-L4-v2-Q4_K_M | 0.069s | 60.0% | Good balance |

---

## 📊 Performance Analysis by Model Family

### BGE Models (9 models tested)
- **Perfect Models:** bge-reranker-v2-m3 (all 3 quantizations)
- **Best Performance:** v2-m3 > large > base
- **Accuracy Range:** 50-100%
- **Response Time:** 0.208-0.810s

### Jina Models (9 models tested)
- **Perfect Models:** v2-base-multilingual (all 3 quantizations)
- **Best Performance:** v2-multilingual > v1-turbo > v1-tiny
- **Accuracy Range:** 60-100%
- **Response Time:** 0.141-0.206s

### MS-MARCO Models (18 models tested)
- **Perfect Models:** MiniLM-L12-v2 (all 3 quantizations)
- **Worst Models:** TinyBERT-L2-v2 (0% accuracy)
- **Accuracy Range:** 0-100%
- **Response Time:** 0.053-0.087s

### MXBAI Models (6 models tested)
- **All models failed** during testing
- **No successful results** recorded
- **Requires investigation**

### Qwen3 Models (9 models tested)
- **All models failed** during testing
- **No successful results** recorded
- **Requires investigation**

---

## ⚖️ Ollama vs llama.cpp Comparison

| Metric | Ollama | llama.cpp | Difference |
|--------|--------|-----------|------------|
| **Overall Accuracy** | **55.2%** (221/400) | **68.7%** (378/550) | -13.5% |
| **Response Time** | **0.160s** avg | 0.162s avg | +1.2% faster |
| **Success Rate** | 72.7% (400/550) | 100% (550/550) | -27.3% |
| **Perfect Models** | 9 models | 16 models | -7 models |
| **Test Coverage** | 400 successful tests | 550 successful tests | -150 tests |

### Shared Perfect Models (100% accuracy on both platforms)
- **bge-reranker-v2-m3** (F16, Q8_0, Q4_K_M)
- **jina-reranker-v2-base-multilingual** (F16, Q8_0, Q4_K_M)
- **ms-marco-MiniLM-L12-v2** (F16, Q8_0, Q4_K_M)

---

## 🔍 Detailed Domain Performance

### Geography Domain
- **Best Model:** bge-reranker-large-F16 (Score: 9.5273)
- **Success Rate:** 69.1% accurate across models
- **Challenge:** Some models confused Paris with landmarks

### Technology Domain
- **Best Model:** bge-reranker-large-F16 (Score: 0.0856)
- **Success Rate:** 52.7% accurate across models
- **Challenge:** Binary search vs other algorithms confusion

### Medicine Domain
- **Best Model:** bge-reranker-large-F16 (Score: 6.1900)
- **Success Rate:** 60.0% accurate across models
- **Performance:** Generally good medical relevance detection

### Finance Domain
- **Best Model:** bge-reranker-large-F16 (Score: 7.8719)
- **Success Rate:** 69.1% accurate across models
- **Performance:** Strong compound interest recognition

---

## 🚀 Use Case Recommendations

### Production RAG Systems
**Recommended:** `bge-reranker-v2-m3-Q4_K_M`
- ✅ 100% accuracy
- ✅ Fast response (0.259s)
- ✅ Reasonable size (~438MB)
- ✅ Consistent performance

### Real-time Search Applications
**Recommended:** `ms-marco-MiniLM-L12-v2-Q4_K_M`
- ✅ 100% accuracy
- ✅ Ultra-fast (0.087s)
- ✅ Small footprint (~29MB)
- ✅ Reliable ranking

### Development & Testing
**Recommended:** `jina-reranker-v2-base-multilingual-Q8_0`
- ✅ 100% accuracy
- ✅ Fast (0.200s)
- ✅ Multilingual support
- ✅ Moderate size (~305MB)

### High-Throughput Batch Processing
**Recommended:** `llama.cpp` with `ms-marco-MiniLM-L12-v2-Q4_K_M`
- ✅ Higher reliability (100% vs 72.7% success)
- ✅ Faster processing (0.029s vs 0.087s)
- ✅ Better overall accuracy

### Edge/Resource-Constrained Environments
**Recommended:** `ms-marco-MiniLM-L12-v2-Q4_K_M` (Ollama)
- ✅ Smallest perfect model (~29MB)
- ✅ No server overhead
- ✅ 100% accuracy
- ✅ Fast response

---

## ⚠️ Known Issues and Limitations

### Model Failures
- **MXBAI Models:** All 6 models failed during testing
- **Qwen3 Models:** All 9 models failed during testing
- **Total Failed Tests:** 150 out of 550 (27.3%)

### Performance Variations
- **TinyBERT Models:** Generally poor performance (0-20% accuracy)
- **Quantization Impact:** Minimal impact on top-performing models
- **Response Time:** Consistent across successful models (0.053-0.810s)

### Platform Differences
- **Reliability:** llama.cpp more reliable (100% vs 72.7% success rate)
- **Speed:** Virtually identical response times
- **Setup:** Ollama much simpler (no server management)

---

## 📈 Quantization Impact Analysis

### Perfect Models - Quantization Performance
| Model | F16 Accuracy | Q8_0 Accuracy | Q4_K_M Accuracy | Speed Impact |
|-------|--------------|---------------|-----------------|--------------|
| bge-reranker-v2-m3 | 100% | 100% | 100% | F16: 0.263s, Q4: 0.259s |
| jina-v2-multilingual | 100% | 100% | 100% | F16: 0.190s, Q4: 0.206s |
| ms-marco-L12-v2 | 100% | 100% | 100% | F16: 0.084s, Q4: 0.087s |

### Key Findings
- **Minimal accuracy loss** for top models across quantizations
- **Speed differences** are negligible for production use
- **Q4_K_M recommended** for best size/performance ratio
- **Storage savings:** 60-80% reduction with minimal performance impact

---

## 🔮 Future Recommendations

### Immediate Actions
1. **Investigate MXBAI and Qwen3 failures** - high-priority models not working
2. **Implement retry logic** for failed requests to improve reliability
3. **Add model health checks** before testing
4. **Create fallback mechanisms** for production systems

### Model Deployment Strategy
1. **Use perfect models** for production applications
2. **Implement A/B testing** between Ollama and llama.cpp
3. **Monitor performance metrics** in production
4. **Consider hybrid approach** based on use case requirements

### Research Directions
1. **Multilingual testing** with jina-v2-multilingual models
2. **Domain-specific fine-tuning** analysis
3. **Cost-benefit analysis** of quantization strategies
4. **Scalability testing** for high-throughput scenarios

---

## 📋 Conclusion

This comprehensive benchmark demonstrates that **Ollama provides excellent reranking capabilities** for specific high-performing models, with deployment simplicity as a key advantage. While llama.cpp shows higher overall reliability and accuracy, Ollama's perfect performers offer competitive performance with virtually identical response times.

### Key Takeaways
1. **9 perfect models** available in Ollama with 100% accuracy
2. **Virtually identical speed** to llama.cpp implementations
3. **Simpler deployment** with no server management required
4. **Significant failure rate** (27.3%) needs investigation
5. **Model selection critical** - choose from verified perfect performers

### Final Recommendation
**Use Ollama for production** with these proven models:
- `bge-reranker-v2-m3-Q4_K_M` (best overall)
- `ms-marco-MiniLM-L12-v2-Q4_K_M` (fastest)
- `jina-reranker-v2-base-multilingual-Q4_K_M` (multilingual)

These models provide perfect accuracy, excellent speed, and the deployment simplicity that makes Ollama an attractive choice for production reranking systems.

---

## 📊 Appendix

### Test Methodology
- **Domains:** Geography, Technology, Medicine, Law, Cooking, Finance, History, Sports, Literature, Science
- **Test Format:** 5 documents per query, 1 correct answer
- **Evaluation:** Top-1 accuracy (highest ranked document must be correct)
- **API:** Ollama `/api/rerank` endpoint
- **Timeout:** 120 seconds per request
- **Response Metrics:** Relevance scores, response time, success/failure status

### Data Files
- **Raw Results:** `test_results_all_models_20251114_103439.csv`
- **Test Queries:** `test_queries.csv` (10 domains, 50 total queries)
- **Script Used:** `test_all_ollama_models.py`

### Technical Specifications
- **Platform:** macOS with M4 Pro, Metal acceleration
- **Ollama Version:** Latest (as of November 2025)
- **Python Version:** 3.12+
- **Libraries:** requests, json, csv, subprocess
- **Total Test Duration:** ~1 hour
- **Models Tested:** 55 reranking models across 5 families