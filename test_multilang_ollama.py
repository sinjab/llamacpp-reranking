#!/usr/bin/env python3
"""
Test Ollama reranking models with multilingual queries.
Tests models across 6 languages (ar, zh, en, de, fr, es) with the same methodology.
"""

import json
import time
import csv
import subprocess
from datetime import datetime
from typing import List, Dict, Any

# --- Configuration ---
OLLAMA_API_URL = "http://localhost:11434/api/rerank"
TEST_QUERIES_FILE = "test_queries_multilang.csv"
REQUEST_TIMEOUT = 120  # Timeout for reranking request

# Focus on multilingual models from our previous test
MULTILINGUAL_MODELS = [
    # Models that showed good multilingual potential
    "jina-reranker-v2-base-multilingual-F16:latest",
    "jina-reranker-v2-base-multilingual-Q8_0:latest",
    "jina-reranker-v2-base-multilingual-Q4_K_M:latest",

    # BGE models that performed well
    "bge-reranker-v2-m3-F16:latest",
    "bge-reranker-v2-m3-Q8_0:latest",
    "bge-reranker-v2-m3-Q4_K_M:latest",

    # Test some other top performers for comparison
    "ms-marco-MiniLM-L12-v2-F16:latest",
    "ms-marco-MiniLM-L12-v2-Q4_K_M:latest"
]

def load_multilingual_queries() -> List[Dict[str, Any]]:
    """Load multilingual test queries from CSV file."""
    queries = []
    try:
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

def test_model_with_multilingual_query(model_name: str, query_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test a model with a multilingual query."""
    correct_doc_index = query_data['correct_doc_index']

    result = {
        'model_name': model_name,
        'language': query_data['language'],
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

        language_flag = {
            'en': '🇬🇧', 'fr': '🇫🇷', 'de': '🇩🇪',
            'es': '🇪🇸', 'zh': '🇨🇳', 'ar': '🇸🇦'
        }.get(query_data['language'], '🌐')

        correct_mark = "✓" if result['correct_answer'] else "✗"
        status = "✅" if result['success'] else "❌"
        print(f"  {language_flag} {correct_mark} {status} {query_data['domain']:12s} ({query_data['language']:2s}): Score={result['top_score']}, Time={result['response_time_seconds']}s")

    except Exception as e:
        result['error'] = str(e)
        print(f"  ❌ {query_data['language']} {query_data['domain']}: Error - {e}")

    return result

def save_to_csv(results: List[Dict[str, Any]], filename: str) -> None:
    """Save results to CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'model_name',
            'language',
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
    """Main function to test models with multilingual queries."""
    print("=" * 100)
    print("MULTILINGUAL OLLAMA RERANKING TEST SUITE")
    print("=" * 100)

    # Load multilingual queries
    test_queries = load_multilingual_queries()
    if not test_queries:
        print("❌ No test queries loaded. Exiting.")
        return

    print(f"\n📋 Loaded {len(test_queries)} multilingual test queries from {TEST_QUERIES_FILE}")

    # Show language distribution
    language_counts = {}
    for q in test_queries:
        language_counts[q['language']] = language_counts.get(q['language'], 0) + 1

    lang_strings = [f'{lang} ({count})' for lang, count in sorted(language_counts.items())]
    print(f"🌍 Languages: {', '.join(lang_strings)}")
    print(f"🤖 Testing {len(MULTILINGUAL_MODELS)} models")

    total_tests = len(MULTILINGUAL_MODELS) * len(test_queries)
    print(f"🎯 Total tests to run: {total_tests}")
    print("=" * 100)

    # Test each model with all multilingual queries
    all_results = []
    test_count = 0

    for model_idx, model_name in enumerate(MULTILINGUAL_MODELS, 1):
        print(f"\n[🤖 Model {model_idx}/{len(MULTILINGUAL_MODELS)}] Testing: {model_name}")
        print("-" * 100)

        model_results = []
        model_start_time = time.time()

        for query_idx, query_data in enumerate(test_queries, 1):
            test_count += 1
            progress = f"[{test_count}/{total_tests}]"
            print(f"  {progress} Query: {query_data['language']} - {query_data['domain']}")

            result = test_model_with_multilingual_query(model_name, query_data)
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

            # Group by language for detailed stats
            lang_stats = {}
            for r in successful:
                lang = r['language']
                if lang not in lang_stats:
                    lang_stats[lang] = {'total': 0, 'correct': 0}
                lang_stats[lang]['total'] += 1
                if r['correct_answer']:
                    lang_stats[lang]['correct'] += 1

            print(f"  📊 Model Summary: {correct}/{len(successful)} ({accuracy:.1f}% accuracy)")
            print(f"  ⏱️  Average Time: {avg_time:.3f}s")
            print(f"  🌍 Language Performance:")
            for lang in sorted(lang_stats.keys()):
                total, correct = lang_stats[lang]['total'], lang_stats[lang]['correct']
                acc = 100 * correct / total if total > 0 else 0
                print(f"      {lang}: {correct}/{total} ({acc:.1f}%)")
        else:
            print(f"  ❌ No successful tests for this model")

        print(f"  ⏰ Total Time: {model_elapsed:.2f}s")

        # Save intermediate results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'test_results_multilang_ollama_{timestamp}.csv'
        save_to_csv(all_results, filename)

        # Longer delay between models
        time.sleep(1.0)

    # Final Summary
    print("\n" + "=" * 100)
    print("🎉 MULTILINGUAL TEST COMPLETED")
    print("=" * 100)

    # Overall statistics
    successful = sum(1 for r in all_results if r['success'])
    correct_answers = sum(1 for r in all_results if r['success'] and r['correct_answer'])

    print(f"\n📊 OVERALL SUMMARY:")
    print(f"✅ Successful: {successful}/{len(all_results)} ({100*successful/len(all_results):.1f}%)")
    print(f"🎯 Correct Answers: {correct_answers}/{successful} ({100*correct_answers/successful:.1f}%)" if successful else "")

    # Language-specific analysis
    if successful:
        print(f"\n🌍 LANGUAGE PERFORMANCE:")
        lang_stats = {}
        for r in all_results:
            if r['success']:
                lang = r['language']
                if lang not in lang_stats:
                    lang_stats[lang] = {'total': 0, 'correct': 0}
                lang_stats[lang]['total'] += 1
                if r['correct_answer']:
                    lang_stats[lang]['correct'] += 1

        for lang in sorted(lang_stats.keys()):
            total, correct = lang_stats[lang]['total'], lang_stats[lang]['correct']
            acc = 100 * correct / total
            print(f"  {lang:2s}: {correct:2d}/{total:2d} ({acc:5.1f}%)")

        # Model performance
        print(f"\n🤖 MODEL PERFORMANCE:")
        model_stats = {}
        for r in all_results:
            if r['success']:
                model = r['model_name']
                if model not in model_stats:
                    model_stats[model] = {'total': 0, 'correct': 0}
                model_stats[model]['total'] += 1
                if r['correct_answer']:
                    model_stats[model]['correct'] += 1

        for model in sorted(model_stats.keys()):
            total, correct = model_stats[model]['total'], model_stats[model]['correct']
            acc = 100 * correct / total
            print(f"  {model}: {correct}/{total} ({acc:.1f}%)")

    print(f"\n{'=' * 100}")
    print(f"📁 Results saved to: {filename}")
    print("=" * 100)

if __name__ == "__main__":
    main()