#!/usr/bin/env python3
"""
Complete test of Ollama reranking models.
Tests all available reranking models across 10 domains with comprehensive analysis.
"""

import json
import time
import csv
import subprocess
from datetime import datetime
from typing import List, Dict, Any

# --- Configuration ---
OLLAMA_API_URL = "http://localhost:11434/api/rerank"
TEST_QUERIES_FILE = "test_queries.csv"
REQUEST_TIMEOUT = 120  # Timeout for reranking request

# Current available Ollama reranking models (updated list)
OLLAMA_MODELS = [
    # BGE Models
    "bge-reranker-base-F16:latest",
    "bge-reranker-base-Q8_0:latest",
    "bge-reranker-base-Q4_K_M:latest",
    "bge-reranker-large-F16:latest",
    "bge-reranker-large-Q8_0:latest",
    "bge-reranker-large-Q4_K_M:latest",
    "bge-reranker-v2-m3-F16:latest",
    "bge-reranker-v2-m3-Q8_0:latest",
    "bge-reranker-v2-m3-Q4_K_M:latest",

    # Jina Models
    "jina-reranker-v1-tiny-en-F16:latest",
    "jina-reranker-v1-tiny-en-Q8_0:latest",
    "jina-reranker-v1-tiny-en-Q4_K_M:latest",
    "jina-reranker-v1-turbo-en-F16:latest",
    "jina-reranker-v1-turbo-en-Q8_0:latest",
    "jina-reranker-v1-turbo-en-Q4_K_M:latest",
    "jina-reranker-v2-base-multilingual-F16:latest",
    "jina-reranker-v2-base-multilingual-Q8_0:latest",
    "jina-reranker-v2-base-multilingual-Q4_K_M:latest",

    # MXBAI Models
    "mxbai-rerank-base-v2-F16:latest",
    "mxbai-rerank-base-v2-Q8_0:latest",
    "mxbai-rerank-base-v2-Q4_K_M:latest",
    "mxbai-rerank-large-v2-F16:latest",
    "mxbai-rerank-large-v2-Q8_0:latest",
    "mxbai-rerank-large-v2-Q4_K_M:latest"
]

def load_test_queries() -> List[Dict[str, Any]]:
    """Load test queries from CSV file (same as llama.cpp tests)."""
    queries = []
    try:
        with open(TEST_QUERIES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                query_data = {
                    'domain': row['domain'],
                    'query': row['query'],
                    'documents': [row['doc1'], row['doc2'], row['doc3'], row['doc4'], row['doc5']],
                    'correct_doc_index': int(row['correct_doc_index'])
                }
                queries.append(query_data)
    except FileNotFoundError:
        print(f"❌ {TEST_QUERIES_FILE} not found.")
        return []
    return queries

def test_ollama_rerank(model_name: str, query: str, documents: List[str]) -> Dict[str, Any]:
    """Test Ollama reranking API for a specific model."""
    payload = {
        "model": model_name,
        "query": query,
        "documents": documents
    }

    try:
        start_time = time.time()
        result = subprocess.run([
            'curl', '-X', 'POST', OLLAMA_API_URL,
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(payload),
            '--max-time', str(REQUEST_TIMEOUT)
        ], capture_output=True, text=True)
        elapsed_time = time.time() - start_time

        if result.returncode == 0:
            response_text = result.stdout.strip()
            try:
                response_data = json.loads(response_text)
                if 'results' in response_data:
                    rankings = response_data['results']
                    return {
                        "success": True,
                        "response_time": elapsed_time,
                        "rankings": rankings,
                        "model": response_data.get('model', model_name)
                    }
                else:
                    return {
                        "success": False,
                        "error": "No results in response",
                        "response_time": elapsed_time,
                        "raw_response": response_text
                    }
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error": f"JSON decode error: {e}",
                    "response_time": elapsed_time,
                    "raw_response": response_text
                }
        else:
            return {
                "success": False,
                "error": f"Curl error: {result.stderr}",
                "response_time": elapsed_time
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Request timeout ({REQUEST_TIMEOUT}s)",
            "response_time": REQUEST_TIMEOUT
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_time": 0
        }

def test_model_with_query(model_name: str, query_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test a single model with a specific query."""
    correct_doc_index = query_data['correct_doc_index']

    result = {
        'model_name': model_name,
        'model_size_mb': 0,  # Will be extracted if needed
        'domain': query_data['domain'],
        'query': query_data['query'],
        'correct_doc_index': correct_doc_index,
        'success': False,
        'error': None,
        'response_time_seconds': None,
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
        test_result = test_ollama_rerank(model_name, query_data['query'], query_data['documents'])

        if test_result['success']:
            rankings = test_result['rankings']
            response_time = test_result['response_time']

            # Record results
            result['success'] = True
            result['response_time_seconds'] = round(response_time, 3)

            # Sort by relevance score (descending)
            sorted_rankings = sorted(rankings, key=lambda x: x['relevance_score'], reverse=True)

            # Store top 5 scores
            for i, res in enumerate(sorted_rankings[:5]):
                score = round(res['relevance_score'], 4)
                if i == 0:
                    result['top_score'] = score
                    result['top_document_index'] = res['index']
                    result['top_document'] = query_data['documents'][res['index']]
                    result['correct_answer'] = (res['index'] == correct_doc_index)
                elif i == 1:
                    result['rank_2_score'] = score
                elif i == 2:
                    result['rank_3_score'] = score
                elif i == 3:
                    result['rank_4_score'] = score
                elif i == 4:
                    result['rank_5_score'] = score

            result['all_scores'] = [round(r['relevance_score'], 4) for r in sorted_rankings]

        else:
            result['error'] = test_result['error']
            result['response_time_seconds'] = test_result.get('response_time', 0)

        correct_mark = "✓" if result['correct_answer'] else "✗"
        status = "✅" if result['success'] else "❌"
        print(f"  {correct_mark} {status} {query_data['domain']:12s}: Score={result['top_score']:>7.3f}, Time={result['response_time_seconds']:>6.3f}s")

    except Exception as e:
        result['error'] = str(e)
        print(f"  ❌ {query_data['domain']:12s}: Error - {e}")

    return result

def save_to_csv(results: List[Dict[str, Any]], filename: str) -> None:
    """Save results to CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'model_name',
            'model_size_mb',
            'domain',
            'query',
            'correct_doc_index',
            'success',
            'response_time_seconds',
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
    """Main function to test all models with all queries."""
    print("=" * 100)
    print("COMPLETE OLLAMA RERANKING MODEL TESTING SUITE")
    print("=" * 100)

    # Load test queries
    test_queries = load_test_queries()
    if not test_queries:
        print("❌ No test queries loaded. Exiting.")
        return

    print(f"\n📋 Loaded {len(test_queries)} test queries from {TEST_QUERIES_FILE}")
    print(f"🏷️  Domains: {', '.join(q['domain'] for q in test_queries)}")

    # Show model count
    print(f"\n🤖 Testing {len(OLLAMA_MODELS)} Ollama models:")

    # Group models by family for display
    model_families = {}
    for model in OLLAMA_MODELS:
        family = model.split('-')[0]  # e.g., "bge", "jina", "mxbai"
        if family not in model_families:
            model_families[family] = []
        model_families[family].append(model)

    for family, models in sorted(model_families.items()):
        print(f"  {family.upper():12s}: {len(models)} models")

    total_tests = len(OLLAMA_MODELS) * len(test_queries)
    print(f"\n🎯 Total tests to run: {total_tests} ({len(OLLAMA_MODELS)} models × {len(test_queries)} queries)")
    print("=" * 100)

    # Test each model with all queries
    all_results = []
    test_count = 0

    for model_idx, model_name in enumerate(OLLAMA_MODELS, 1):
        print(f"\n[🤖 Model {model_idx}/{len(OLLAMA_MODELS)}] Testing: {model_name}")
        print("-" * 100)

        model_results = []
        model_start_time = time.time()

        for query_idx, query_data in enumerate(test_queries, 1):
            test_count += 1
            progress = f"[{test_count}/{total_tests}]"
            print(f"  {progress} Query: {query_data['domain']}")

            result = test_model_with_query(model_name, query_data)
            model_results.append(result)
            all_results.append(result)

            # Small delay between queries
            time.sleep(0.1)

        model_elapsed = time.time() - model_start_time

        # Print model summary
        successful = [r for r in model_results if r['success']]
        if successful:
            correct = sum(1 for r in successful if r['correct_answer'])
            accuracy = 100 * correct / len(successful)
            avg_time = sum(r['response_time_seconds'] for r in successful) / len(successful)

            print(f"  📊 Model Summary: {correct}/{len(successful)} ({accuracy:.1f}% accuracy)")
            print(f"  ⏱️  Average Time: {avg_time:.3f}s")
        else:
            print(f"  ❌ No successful tests for this model")

        print(f"  ⏰ Total Time: {model_elapsed:.2f}s")

        # Save intermediate results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'test_results_ollama_complete_{timestamp}.csv'
        save_to_csv(all_results, filename)

        # Delay between models
        time.sleep(1.0)

    # Final Summary
    print("\n" + "=" * 100)
    print("🎉 ALL TESTS COMPLETED")
    print("=" * 100)

    # Overall statistics
    successful = sum(1 for r in all_results if r['success'])
    correct_answers = sum(1 for r in all_results if r['success'] and r['correct_answer'])
    failed = len(all_results) - successful

    print(f"\n📊 SUMMARY:")
    print(f"✅ Successful: {successful}/{len(all_results)} ({100*successful/len(all_results):.1f}%)")
    print(f"❌ Failed: {failed}/{len(all_results)} ({100*failed/len(all_results):.1f}%)")

    if successful > 0:
        print(f"🎯 Correct Answers: {correct_answers}/{successful} ({100*correct_answers/successful:.1f}%)")

    # Show top performers
    successful_results = [r for r in all_results if r['success']]
    if successful_results:
        print("\n🏆 TOP PERFORMERS:")

        print("\n--- Perfect Accuracy Models (100%) ---")
        model_stats = {}
        for result in successful_results:
            model = result['model_name']
            if model not in model_stats:
                model_stats[model] = {'total': 0, 'correct': 0, 'times': []}
            model_stats[model]['total'] += 1
            if result['correct_answer']:
                model_stats[model]['correct'] += 1
            if result['response_time_seconds']:
                model_stats[model]['times'].append(result['response_time_seconds'])

        perfect_models = [(model, stats) for model, stats in model_stats.items()
                         if stats['correct'] == stats['total'] and stats['total'] >= 5]

        if perfect_models:
            for i, (model, stats) in enumerate(sorted(perfect_models, key=lambda x: x[1]['times'][0]), 1):
                avg_time = sum(stats['times']) / len(stats['times'])
                print(f"  {i}. {model}: {avg_time:.3f}s avg time")
        else:
            print("  No models achieved 100% accuracy")

        print("\n--- Top 10 Models by Accuracy ---")
        model_accuracy = []
        for model, stats in model_stats.items():
            if stats['total'] >= 5:
                accuracy = 100 * stats['correct'] / stats['total']
                avg_time = sum(stats['times']) / len(stats['times'])
                model_accuracy.append((model, accuracy, stats['correct'], stats['total'], avg_time))

        top_accuracy = sorted(model_accuracy, key=lambda x: x[1], reverse=True)[:10]
        for i, (model, accuracy, correct, total, avg_time) in enumerate(top_accuracy, 1):
            print(f"  {i:2d}. {model}: {accuracy:5.1f}% ({correct}/{total}) - {avg_time:.3f}s")

        print("\n--- Top 10 Fastest Models ---")
        model_speed = []
        for model, stats in model_stats.items():
            if len(stats['times']) >= 5:
                avg_time = sum(stats['times']) / len(stats['times'])
                accuracy = 100 * stats['correct'] / stats['total']
                model_speed.append((model, avg_time, accuracy))

        fastest = sorted(model_speed, key=lambda x: x[1])[:10]
        for i, (model, avg_time, accuracy) in enumerate(fastest, 1):
            print(f"  {i:2d}. {model}: {avg_time:.3f}s - {accuracy:.1f}% accuracy")

    print(f"\n{'=' * 100}")
    print(f"📁 Results saved to: {filename}")
    print("=" * 100)

if __name__ == "__main__":
    main()