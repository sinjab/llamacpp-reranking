#!/usr/bin/env python3
"""
Test Ollama's /api/rerank endpoint with bge-reranker models.

This script tests Ollama's reranking implementation using models from
~/.ollama/models/ directory.
"""

import requests
import json
import csv
import time
from pathlib import Path
from datetime import datetime

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/rerank"
TEST_QUERIES_FILE = "test_queries.csv"
REQUEST_TIMEOUT = 60  # Timeout for reranking request

# Model to test (must be already loaded in Ollama)
OLLAMA_MODEL = "bge-reranker-test"

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
        print(f"  {correct_mark} {query_data['domain']}: Score={result['top_score']}, Time={result['response_time_seconds']}s, Correct={result['correct_answer']}")

    except Exception as e:
        result['error'] = str(e)
        print(f"  ✗ {query_data['domain']}: Error - {e}")

    return result

def save_to_csv(results, filename='test_results_ollama.csv'):
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

def main():
    """Main function to test Ollama reranking."""
    print("=" * 80)
    print("OLLAMA RERANKING TEST SUITE")
    print("=" * 80)

    # Load test queries
    test_queries = load_test_queries()
    print(f"\nLoaded {len(test_queries)} test queries from {TEST_QUERIES_FILE}")
    print(f"Domains: {', '.join(q['domain'] for q in test_queries)}")
    print(f"Testing Ollama model: {OLLAMA_MODEL}")
    print("=" * 80)

    # Test all queries
    all_results = []

    for idx, query_data in enumerate(test_queries, 1):
        print(f"\n[{idx}/{len(test_queries)}] Query: {query_data['domain']}")
        result = test_query(OLLAMA_MODEL, query_data)
        all_results.append(result)

        # Small delay to avoid overwhelming Ollama
        if idx < len(test_queries):
            time.sleep(0.5)

    # Summary
    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)

    successful = sum(1 for r in all_results if r['success'])
    correct_answers = sum(1 for r in all_results if r['success'] and r['correct_answer'])

    print(f"\nSuccessful: {successful}/{len(all_results)}")
    print(f"Failed: {len(all_results) - successful}/{len(all_results)}")

    if successful > 0:
        print(f"Correct Answers: {correct_answers}/{successful} ({100*correct_answers/successful:.1f}%)")

        # Calculate average metrics
        successful_results = [r for r in all_results if r['success']]
        avg_time = sum(r['response_time_seconds'] for r in successful_results) / len(successful_results)
        avg_total = sum(r['total_duration_ms'] for r in successful_results) / len(successful_results)
        avg_load = sum(r['load_duration_ms'] for r in successful_results) / len(successful_results)
        avg_score = sum(r['top_score'] for r in successful_results) / len(successful_results)

        print(f"\nAverage Response Time: {avg_time:.3f}s")
        print(f"Average Total Duration: {avg_total:.2f}ms")
        print(f"Average Load Duration: {avg_load:.2f}ms")
        print(f"Average Top Score: {avg_score:.4f}")

        # Show per-domain accuracy
        print("\n--- Accuracy by Domain ---")
        domains = sorted(set(q['domain'] for q in test_queries))
        for domain in domains:
            domain_results = [r for r in successful_results if r['domain'] == domain]
            if domain_results:
                correct = sum(1 for r in domain_results if r['correct_answer'])
                total = len(domain_results)
                accuracy = 100 * correct / total
                avg_score_domain = sum(r['top_score'] for r in domain_results) / total
                print(f"  {domain:15s}: {correct}/{total} ({accuracy:.1f}%) - Avg Score: {avg_score_domain:.4f}")

    # Save to CSV
    save_to_csv(all_results)

if __name__ == "__main__":
    main()
