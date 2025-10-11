#!/usr/bin/env python3
"""
Multilingual Reranking Model Testing Suite
Tests reranking models across 6 languages: Arabic, Chinese, English, German, French, Spanish
"""

import requests
import json
import subprocess
import time
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# --- Configuration ---
SERVER_URL = "http://localhost:8080/rerank"
MODEL_DIR = Path.home() / "Documents" / "reranking-models"
TEST_QUERIES_FILE = "test_queries_multilang.csv"
PORT = 8080
TIMEOUT_SECONDS = 30
REQUEST_TIMEOUT = 60

# Language codes
LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'ar': 'Arabic',
    'zh': 'Chinese'
}

def load_test_queries():
    """Load multilingual test queries from CSV file."""
    queries = []
    with open(TEST_QUERIES_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            query_data = {
                'language': row['language'],
                'domain': row['domain'],
                'query': row['query'],
                'documents': [row['doc1'], row['doc2'], row['doc3'], row['doc4'], row['doc5']],
                'correct_doc_index': int(row['correct_doc_index'])
            }
            queries.append(query_data)
    return queries

def get_model_files():
    """Get all .gguf model files from the models directory."""
    return sorted(MODEL_DIR.glob("*.gguf"))

def start_server(model_path):
    """Start llama-server with the specified model."""
    cmd = [
        "llama-server",
        "-m", str(model_path),
        "--port", str(PORT),
        "--rerank"
    ]

    print(f"Starting server with model: {model_path.name}")
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return process

def wait_for_server(timeout=TIMEOUT_SECONDS):
    """Wait for the server to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"http://localhost:{PORT}/health", timeout=2)
            if response.status_code == 200:
                print("Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)

    return False

def test_reranking(query, documents):
    """Test the reranking endpoint and return results."""
    payload = {
        "query": query,
        "documents": documents
    }

    headers = {
        "Content-Type": "application/json"
    }

    start_time = time.time()
    response = requests.post(
        SERVER_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=REQUEST_TIMEOUT
    )
    elapsed_time = time.time() - start_time

    response.raise_for_status()
    results = response.json()['results']

    # Sort by relevance score
    sorted_results = sorted(results, key=lambda x: x['relevance_score'], reverse=True)

    return sorted_results, elapsed_time

def stop_server(process):
    """Stop the llama-server process."""
    print("Stopping server...")
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()

    time.sleep(2)

def test_model_with_query(model_path, query_data):
    """Test a single model with a specific query."""
    model_name = model_path.name
    correct_doc_index = query_data['correct_doc_index']

    result = {
        'model_name': model_name,
        'model_size_mb': round(model_path.stat().st_size / (1024 * 1024), 2),
        'language': query_data['language'],
        'domain': query_data['domain'],
        'success': False,
        'response_time_seconds': None,
        'correct_answer': False,
        'timestamp': datetime.now().isoformat()
    }

    try:
        sorted_results, elapsed_time = test_reranking(query_data['query'], query_data['documents'])

        result['success'] = True
        result['response_time_seconds'] = round(elapsed_time, 3)

        top_result = sorted_results[0]
        result['correct_answer'] = (top_result['index'] == correct_doc_index)

        correct_mark = "✓" if result['correct_answer'] else "✗"
        lang_name = LANGUAGES.get(query_data['language'], query_data['language'])
        print(f"  {correct_mark} [{lang_name:7s}] {query_data['domain']:10s} Time={result['response_time_seconds']}s")

    except Exception as e:
        print(f"  ✗ [{query_data['language']}] {query_data['domain']}: Error - {e}")

    return result

def save_to_csv(results, filename='test_results_multilang.csv'):
    """Save results to CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'model_name',
            'model_size_mb',
            'language',
            'domain',
            'success',
            'response_time_seconds',
            'correct_answer',
            'timestamp'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✓ Results saved to {filename}")

def main():
    """Main function to test all models with multilingual queries."""
    print("=" * 80)
    print("MULTILINGUAL RERANKING MODEL TESTING SUITE")
    print("=" * 80)

    # Load test queries
    test_queries = load_test_queries()
    print(f"\nLoaded {len(test_queries)} test queries from {TEST_QUERIES_FILE}")

    # Count queries per language
    lang_counts = defaultdict(int)
    for q in test_queries:
        lang_counts[q['language']] += 1

    print("Languages tested:")
    for lang_code, count in sorted(lang_counts.items()):
        lang_name = LANGUAGES.get(lang_code, lang_code)
        print(f"  - {lang_name} ({lang_code}): {count} queries")

    # Get all model files
    model_files = get_model_files()
    print(f"\nFound {len(model_files)} models in {MODEL_DIR}")

    total_tests = len(model_files) * len(test_queries)
    print(f"\nTotal tests to run: {total_tests} ({len(model_files)} models × {len(test_queries)} queries)")
    print("=" * 80)

    # Test each model with all queries
    all_results = []
    test_count = 0

    for model_idx, model_path in enumerate(model_files, 1):
        print(f"\n[Model {model_idx}/{len(model_files)}] Testing: {model_path.name}")
        print("-" * 80)

        process = None
        try:
            process = start_server(model_path)

            if not wait_for_server():
                print(f"✗ Server failed to start - skipping model")
                for query_data in test_queries:
                    result = {
                        'model_name': model_path.name,
                        'model_size_mb': round(model_path.stat().st_size / (1024 * 1024), 2),
                        'language': query_data['language'],
                        'domain': query_data['domain'],
                        'success': False,
                        'response_time_seconds': None,
                        'correct_answer': False,
                        'timestamp': datetime.now().isoformat()
                    }
                    all_results.append(result)
                continue

            # Test all queries with this model
            for query_idx, query_data in enumerate(test_queries, 1):
                test_count += 1
                result = test_model_with_query(model_path, query_data)
                all_results.append(result)

        except Exception as e:
            print(f"✗ Unexpected error: {e}")

        finally:
            if process:
                stop_server(process)

    # Save results
    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETED")
    print("=" * 80)

    # Summary statistics
    successful = sum(1 for r in all_results if r['success'])
    correct_answers = sum(1 for r in all_results if r['success'] and r['correct_answer'])
    print(f"\nSuccessful: {successful}/{len(all_results)}")
    print(f"Failed: {len(all_results) - successful}/{len(all_results)}")
    if successful > 0:
        print(f"Correct Answers: {correct_answers}/{successful} ({100*correct_answers/successful:.1f}%)")

    # Save to CSV
    save_to_csv(all_results)

    # Language-specific analysis
    successful_results = [r for r in all_results if r['success']]
    if successful_results:
        print("\n" + "=" * 80)
        print("LANGUAGE-SPECIFIC PERFORMANCE")
        print("=" * 80)

        for lang_code in sorted(LANGUAGES.keys()):
            lang_name = LANGUAGES[lang_code]
            lang_results = [r for r in successful_results if r['language'] == lang_code]

            if lang_results:
                correct = sum(1 for r in lang_results if r['correct_answer'])
                total = len(lang_results)
                accuracy = 100 * correct / total if total > 0 else 0
                avg_time = sum(r['response_time_seconds'] for r in lang_results) / total

                print(f"\n{lang_name} ({lang_code}):")
                print(f"  Accuracy: {accuracy:.1f}% ({correct}/{total})")
                print(f"  Avg Time: {avg_time:.3f}s")

                # Top 3 models for this language
                model_perf = defaultdict(lambda: {'correct': 0, 'total': 0})
                for r in lang_results:
                    model_perf[r['model_name']]['total'] += 1
                    if r['correct_answer']:
                        model_perf[r['model_name']]['correct'] += 1

                top_models = sorted(
                    model_perf.items(),
                    key=lambda x: (x[1]['correct'] / x[1]['total'], -x[1]['total']),
                    reverse=True
                )[:3]

                print(f"  Top 3 models:")
                for i, (model, perf) in enumerate(top_models, 1):
                    acc = 100 * perf['correct'] / perf['total']
                    print(f"    {i}. {model}: {acc:.1f}% ({perf['correct']}/{perf['total']})")

        # Overall top performers across all languages
        print("\n" + "=" * 80)
        print("TOP PERFORMERS ACROSS ALL LANGUAGES")
        print("=" * 80)

        model_accuracy = {}
        for model_name in set(r['model_name'] for r in successful_results):
            model_results = [r for r in successful_results if r['model_name'] == model_name]
            correct = sum(1 for r in model_results if r['correct_answer'])
            accuracy = 100 * correct / len(model_results)
            avg_time = sum(r['response_time_seconds'] for r in model_results) / len(model_results)
            model_accuracy[model_name] = (accuracy, correct, len(model_results), avg_time)

        top_accuracy = sorted(model_accuracy.items(), key=lambda x: (-x[1][0], x[1][3]))[:10]
        print("\nTop 10 Models by Accuracy:")
        for i, (model, (acc, correct, total, avg_time)) in enumerate(top_accuracy, 1):
            print(f"  {i:2d}. {model:45s} {acc:5.1f}% ({correct:2d}/{total}) - {avg_time:.3f}s")

        # Language comparison: Models that work well across all languages
        print("\n" + "=" * 80)
        print("MULTILINGUAL CONSISTENCY (Models performing well across all languages)")
        print("=" * 80)

        model_lang_perf = defaultdict(lambda: defaultdict(lambda: {'correct': 0, 'total': 0}))
        for r in successful_results:
            model_lang_perf[r['model_name']][r['language']]['total'] += 1
            if r['correct_answer']:
                model_lang_perf[r['model_name']][r['language']]['correct'] += 1

        # Calculate consistency score (minimum accuracy across all languages)
        model_consistency = {}
        for model, lang_perf in model_lang_perf.items():
            if len(lang_perf) == len(LANGUAGES):  # Model tested on all languages
                min_acc = min(
                    100 * lang_perf[lang]['correct'] / lang_perf[lang]['total']
                    for lang in LANGUAGES.keys()
                )
                avg_acc = sum(
                    100 * lang_perf[lang]['correct'] / lang_perf[lang]['total']
                    for lang in LANGUAGES.keys()
                ) / len(LANGUAGES)
                model_consistency[model] = (min_acc, avg_acc)

        consistent_models = sorted(model_consistency.items(), key=lambda x: (-x[1][0], -x[1][1]))[:10]
        print("\nTop 10 Most Consistent Models (by minimum language accuracy):")
        for i, (model, (min_acc, avg_acc)) in enumerate(consistent_models, 1):
            print(f"  {i:2d}. {model:45s} Min: {min_acc:5.1f}% | Avg: {avg_acc:5.1f}%")

if __name__ == "__main__":
    main()
