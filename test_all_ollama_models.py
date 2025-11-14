#!/usr/bin/env python3
"""
Test ALL Ollama reranking models with comprehensive test queries.

This script tests all imported reranking models against the test query suite.
Results are saved to a comprehensive CSV file for analysis.
"""

import requests
import json
import csv
import time
from pathlib import Path
from datetime import datetime
import sys

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/rerank"
TEST_QUERIES_FILE = "test_queries.csv"
REQUEST_TIMEOUT = 120  # Longer timeout for large models
RESULTS_FILE = f"test_results_all_models_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# All reranking models to test (exactly matching your Ollama list)
RERANKING_MODELS = [
    # BGE Models (3 base models x 3 quantizations = 9)
    "bge-reranker-base-F16:latest",
    "bge-reranker-base-Q8_0:latest",
    "bge-reranker-base-Q4_K_M:latest",
    "bge-reranker-large-F16:latest",
    "bge-reranker-large-Q8_0:latest",
    "bge-reranker-large-Q4_K_M:latest",
    "bge-reranker-v2-m3-F16:latest",
    "bge-reranker-v2-m3-Q8_0:latest",
    "bge-reranker-v2-m3-Q4_K_M:latest",

    # Jina Models (3 base models x 3 quantizations = 9)
    "jina-reranker-v1-tiny-en-F16:latest",
    "jina-reranker-v1-tiny-en-Q8_0:latest",
    "jina-reranker-v1-tiny-en-Q4_K_M:latest",
    "jina-reranker-v1-turbo-en-F16:latest",
    "jina-reranker-v1-turbo-en-Q8_0:latest",
    "jina-reranker-v1-turbo-en-Q4_K_M:latest",
    "jina-reranker-v2-base-multilingual-F16:latest",
    "jina-reranker-v2-base-multilingual-Q8_0:latest",
    "jina-reranker-v2-base-multilingual-Q4_K_M:latest",

    # MS-MARCO Models (multiple variants)
    "ms-marco-MiniLM-L2-v2-F16:latest",
    "ms-marco-MiniLM-L2-v2-Q8_0:latest",
    "ms-marco-MiniLM-L2-v2-Q4_K_M:latest",
    "ms-marco-MiniLM-L4-v2-F16:latest",
    "ms-marco-MiniLM-L4-v2-Q8_0:latest",
    "ms-marco-MiniLM-L4-v2-Q4_K_M:latest",
    "ms-marco-MiniLM-L6-v2-F16:latest",
    "ms-marco-MiniLM-L6-v2-Q8_0:latest",
    "ms-marco-MiniLM-L6-v2-Q4_K_M:latest",
    "ms-marco-MiniLM-L12-v2-F16:latest",
    "ms-marco-MiniLM-L12-v2-Q8_0:latest",
    "ms-marco-MiniLM-L12-v2-Q4_K_M:latest",
    "ms-marco-TinyBERT-L2-F16:latest",
    "ms-marco-TinyBERT-L2-Q8_0:latest",
    "ms-marco-TinyBERT-L2-Q4_K_M:latest",
    "ms-marco-TinyBERT-L2-v2-F16:latest",
    "ms-marco-TinyBERT-L2-v2-Q8_0:latest",
    "ms-marco-TinyBERT-L2-v2-Q4_K_M:latest",
    "ms-marco-TinyBERT-L4-F16:latest",
    "ms-marco-TinyBERT-L6-F16:latest",
    "ms-marco-TinyBERT-L6-Q8_0:latest",
    "ms-marco-TinyBERT-L6-Q4_K_M:latest",

    # mxbai Models (2 base models x 3 quantizations = 6)
    "mxbai-rerank-base-v2-F16:latest",
    "mxbai-rerank-base-v2-Q8_0:latest",
    "mxbai-rerank-base-v2-Q4_K_M:latest",
    "mxbai-rerank-large-v2-F16:latest",
    "mxbai-rerank-large-v2-Q8_0:latest",
    "mxbai-rerank-large-v2-Q4_K_M:latest",

    # Qwen3 Models (3 base models x 3 quantizations = 9)
    "Qwen3-Reranker-0.6B-F16:latest",
    "Qwen3-Reranker-0.6B-Q8_0:latest",
    "Qwen3-Reranker-0.6B-Q4_K_M:latest",
    "Qwen3-Reranker-4B-F16:latest",
    "Qwen3-Reranker-4B-Q8_0:latest",
    "Qwen3-Reranker-4B-Q4_K_M:latest",
    "Qwen3-Reranker-8B-F16:latest",
    "Qwen3-Reranker-8B-Q8_0:latest",
    "Qwen3-Reranker-8B-Q4_K_M:latest"
]

def load_test_queries():
    """Load test queries from CSV file."""
    queries = []
    with open(TEST_QUERIES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            query_data = {
                'domain': row['domain'],
                'query': row['query'],
                'documents': [row['doc1'], row['doc2'], row['doc3'], row['doc4'], row['doc5']],
                'correct_doc_index': int(row['correct_doc_index'])
            }
            queries.append(query_data)
    return queries

def test_ollama_reranking(model, query, documents):
    """Test the Ollama reranking endpoint and return results."""
    payload = {
        "model": model,
        "query": query,
        "documents": documents
    }

    headers = {
        "Content-Type": "application/json"
    }

    start_time = time.time()
    response = requests.post(
        OLLAMA_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=REQUEST_TIMEOUT
    )
    elapsed_time = time.time() - start_time

    response.raise_for_status()
    result = response.json()

    return result, elapsed_time

def test_query(model, query_data):
    """Test a single query."""
    correct_doc_index = query_data['correct_doc_index']

    result = {
        'model_name': model,
        'domain': query_data['domain'],
        'query': query_data['query'],
        'correct_doc_index': correct_doc_index,
        'success': False,
        'error': None,
        'response_time_seconds': None,
        'total_duration_ms': None,
        'load_duration_ms': None,
        'top_score': None,
        'top_document_index': None,
        'top_document': None,
        'correct_answer': False,
        'rank_2_score': None,
        'rank_3_score': None,
        'rank_4_score': None,
        'rank_5_score': None,
        'all_scores': None,
        'timestamp': datetime.now().isoformat()
    }

    try:
        # Test reranking
        response_data, elapsed_time = test_ollama_reranking(
            model,
            query_data['query'],
            query_data['documents']
        )

        # Extract results (already sorted by Ollama)
        sorted_results = response_data.get('results', [])

        # Record results
        result['success'] = True
        result['response_time_seconds'] = round(elapsed_time, 3)
        result['total_duration_ms'] = round(response_data.get('total_duration', 0) / 1_000_000, 2)
        result['load_duration_ms'] = round(response_data.get('load_duration', 0) / 1_000_000, 2)

        # Store top 5 scores
        for i, res in enumerate(sorted_results[:5]):
            score = round(res['relevance_score'], 4)
            if i == 0:
                result['top_score'] = score
                result['top_document_index'] = res['index']
                result['top_document'] = res.get('document', query_data['documents'][res['index']])
                result['correct_answer'] = (res['index'] == correct_doc_index)
            elif i == 1:
                result['rank_2_score'] = score
            elif i == 2:
                result['rank_3_score'] = score
            elif i == 3:
                result['rank_4_score'] = score
            elif i == 4:
                result['rank_5_score'] = score

        result['all_scores'] = [round(r['relevance_score'], 4) for r in sorted_results]

        correct_mark = "✓" if result['correct_answer'] else "✗"
        print(f"    {correct_mark} {query_data['domain']:15s}: Score={result['top_score']:8.4f}, Time={result['response_time_seconds']:6.3f}s")

    except Exception as e:
        result['error'] = str(e)
        print(f"    ✗ {query_data['domain']:15s}: Error - {e}")

    return result

def save_to_csv(results, filename):
    """Save results to CSV file."""
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = [
            'model_name',
            'domain',
            'query',
            'correct_doc_index',
            'success',
            'response_time_seconds',
            'total_duration_ms',
            'load_duration_ms',
            'top_score',
            'top_document_index',
            'top_document',
            'correct_answer',
            'rank_2_score',
            'rank_3_score',
            'rank_4_score',
            'rank_5_score',
            'all_scores',
            'error',
            'timestamp'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            # Convert all_scores list to string for CSV
            csv_result = result.copy()
            if csv_result['all_scores']:
                csv_result['all_scores'] = str(csv_result['all_scores'])
            writer.writerow(csv_result)

    print(f"\n✓ Results saved to {filename}")

def print_model_summary(model, results):
    """Print summary for a single model."""
    successful = [r for r in results if r['success']]
    if not successful:
        print(f"  No successful tests")
        return

    correct = sum(1 for r in successful if r['correct_answer'])
    accuracy = 100 * correct / len(successful)
    avg_time = sum(r['response_time_seconds'] for r in successful) / len(successful)
    avg_score = sum(r['top_score'] for r in successful) / len(successful)

    print(f"  Accuracy: {correct}/{len(successful)} ({accuracy:.1f}%), Avg Time: {avg_time:.3f}s, Avg Score: {avg_score:.4f}")

def main():
    """Main function to test all Ollama reranking models."""
    print("=" * 100)
    print("COMPREHENSIVE OLLAMA RERANKING TEST SUITE")
    print("=" * 100)

    # Load test queries
    test_queries = load_test_queries()
    print(f"\nLoaded {len(test_queries)} test queries from {TEST_QUERIES_FILE}")
    print(f"Domains: {', '.join(q['domain'] for q in test_queries)}")
    print(f"\nTesting {len(RERANKING_MODELS)} reranking models")
    print(f"Results will be saved to: {RESULTS_FILE}")
    print("=" * 100)

    # Test all models
    all_results = []
    model_summaries = []

    for model_idx, model in enumerate(RERANKING_MODELS, 1):
        print(f"\n[{model_idx}/{len(RERANKING_MODELS)}] Testing Model: {model}")
        print("-" * 100)

        model_results = []
        model_start_time = time.time()

        for query_idx, query_data in enumerate(test_queries, 1):
            result = test_query(model, query_data)
            model_results.append(result)
            all_results.append(result)

            # Small delay between queries
            if query_idx < len(test_queries):
                time.sleep(0.2)

        model_elapsed = time.time() - model_start_time

        # Print model summary
        print_model_summary(model, model_results)
        print(f"  Total Time: {model_elapsed:.2f}s")

        # Store summary
        successful = [r for r in model_results if r['success']]
        if successful:
            correct = sum(1 for r in successful if r['correct_answer'])
            accuracy = 100 * correct / len(successful)
            avg_time = sum(r['response_time_seconds'] for r in successful) / len(successful)
            avg_score = sum(r['top_score'] for r in successful) / len(successful)

            model_summaries.append({
                'model': model,
                'accuracy': accuracy,
                'correct': correct,
                'total': len(successful),
                'avg_time': avg_time,
                'avg_score': avg_score,
                'total_time': model_elapsed
            })

        # Save intermediate results after each model
        save_to_csv(all_results, RESULTS_FILE)

        # Longer delay between models to prevent overheating
        if model_idx < len(RERANKING_MODELS):
            time.sleep(1.0)

    # Final Summary
    print("\n" + "=" * 100)
    print("COMPREHENSIVE TEST COMPLETED")
    print("=" * 100)

    print(f"\nTotal Tests: {len(all_results)}")
    successful = sum(1 for r in all_results if r['success'])
    print(f"Successful: {successful}/{len(all_results)}")
    print(f"Failed: {len(all_results) - successful}/{len(all_results)}")

    if model_summaries:
        print("\n" + "=" * 100)
        print("MODEL RANKINGS BY ACCURACY")
        print("=" * 100)

        # Sort by accuracy
        sorted_summaries = sorted(model_summaries, key=lambda x: (x['accuracy'], x['avg_score']), reverse=True)

        print(f"\n{'Rank':<6} {'Model':<50} {'Accuracy':<15} {'Avg Score':<12} {'Avg Time':<12}")
        print("-" * 100)

        for rank, summary in enumerate(sorted_summaries[:20], 1):  # Top 20
            model_short = summary['model'].replace(':latest', '')
            accuracy_str = f"{summary['correct']}/{summary['total']} ({summary['accuracy']:.1f}%)"
            print(f"{rank:<6} {model_short:<50} {accuracy_str:<15} {summary['avg_score']:<12.4f} {summary['avg_time']:<12.3f}s")

        print("\n" + "=" * 100)
        print("MODEL RANKINGS BY SPEED (Fastest)")
        print("=" * 100)

        # Sort by speed
        sorted_by_speed = sorted(model_summaries, key=lambda x: x['avg_time'])

        print(f"\n{'Rank':<6} {'Model':<50} {'Avg Time':<12} {'Accuracy':<15}")
        print("-" * 100)

        for rank, summary in enumerate(sorted_by_speed[:20], 1):  # Top 20
            model_short = summary['model'].replace(':latest', '')
            accuracy_str = f"{summary['correct']}/{summary['total']} ({summary['accuracy']:.1f}%)"
            print(f"{rank:<6} {model_short:<50} {summary['avg_time']:<12.3f}s {accuracy_str:<15}")

    print(f"\n{'=' * 100}")
    print(f"Full results saved to: {RESULTS_FILE}")
    print("=" * 100)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user. Partial results may have been saved.")
        sys.exit(1)
