import requests
import json
import subprocess
import time
import csv
from pathlib import Path
from datetime import datetime

# --- Configuration ---
SERVER_URL = "http://localhost:8080/rerank"
MODEL_DIR = Path.home() / "Documents" / "reranking-models"
TEST_QUERIES_FILE = "test_queries.csv"
PORT = 8080
TIMEOUT_SECONDS = 30  # Timeout for server startup
REQUEST_TIMEOUT = 60  # Timeout for reranking request

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
            # Try to connect to the server (health check)
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

    # Give the port time to be released
    time.sleep(2)

def test_model_with_query(model_path, query_data, process=None):
    """Test a single model with a specific query."""
    model_name = model_path.name
    correct_doc_index = query_data['correct_doc_index']

    result = {
        'model_name': model_name,
        'model_size_mb': round(model_path.stat().st_size / (1024 * 1024), 2),
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
        sorted_results, elapsed_time = test_reranking(query_data['query'], query_data['documents'])

        # Record results
        result['success'] = True
        result['response_time_seconds'] = round(elapsed_time, 3)

        # Store top 5 scores
        for i, res in enumerate(sorted_results[:5]):
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

        result['all_scores'] = [round(r['relevance_score'], 4) for r in sorted_results]

        correct_mark = "✓" if result['correct_answer'] else "✗"
        print(f"  {correct_mark} {query_data['domain']}: Score={result['top_score']}, Time={result['response_time_seconds']}s, Correct={result['correct_answer']}")

    except Exception as e:
        result['error'] = str(e)
        print(f"  ✗ {query_data['domain']}: Error - {e}")

    return result

def save_to_csv(results, filename='test_results.csv'):
    """Save results to CSV file."""
    with open(filename, 'w', newline='') as csvfile:
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
    print("=" * 80)
    print("COMPREHENSIVE RERANKING MODEL TESTING SUITE")
    print("=" * 80)

    # Load test queries
    test_queries = load_test_queries()
    print(f"\nLoaded {len(test_queries)} test queries from {TEST_QUERIES_FILE}")
    print(f"Domains: {', '.join(q['domain'] for q in test_queries)}")

    # Get all model files
    model_files = get_model_files()
    print(f"Found {len(model_files)} models in {MODEL_DIR}")

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
            # Start server once per model
            process = start_server(model_path)

            # Wait for server to be ready
            if not wait_for_server():
                print(f"✗ Server failed to start - skipping all queries for this model")
                for query_data in test_queries:
                    result = {
                        'model_name': model_path.name,
                        'model_size_mb': round(model_path.stat().st_size / (1024 * 1024), 2),
                        'domain': query_data['domain'],
                        'query': query_data['query'],
                        'correct_doc_index': query_data['correct_doc_index'],
                        'success': False,
                        'error': 'Server failed to start',
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
                    all_results.append(result)
                continue

            # Test all queries with this model
            for query_idx, query_data in enumerate(test_queries, 1):
                test_count += 1
                print(f"  [{test_count}/{total_tests}] Query: {query_data['domain']}")

                result = test_model_with_query(model_path, query_data, process)
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
    print(f"Correct Answers: {correct_answers}/{successful} ({100*correct_answers/successful:.1f}%)" if successful > 0 else "")

    # Save to CSV
    save_to_csv(all_results)

    # Show top performers by domain
    successful_results = [r for r in all_results if r['success']]
    if successful_results:
        print("\n--- Best Models by Domain (Top Score) ---")
        for domain in sorted(set(q['domain'] for q in test_queries)):
            domain_results = [r for r in successful_results if r['domain'] == domain]
            if domain_results:
                best = max(domain_results, key=lambda x: x['top_score'])
                print(f"  {domain:15s}: {best['model_name']:40s} (score: {best['top_score']})")

        print("\n--- Overall Top 5 Models by Accuracy ---")
        model_accuracy = {}
        for model_name in set(r['model_name'] for r in successful_results):
            model_results = [r for r in successful_results if r['model_name'] == model_name]
            correct = sum(1 for r in model_results if r['correct_answer'])
            accuracy = 100 * correct / len(model_results)
            model_accuracy[model_name] = (accuracy, correct, len(model_results))

        top_accuracy = sorted(model_accuracy.items(), key=lambda x: x[1][0], reverse=True)[:5]
        for i, (model, (acc, correct, total)) in enumerate(top_accuracy, 1):
            print(f"  {i}. {model}: {acc:.1f}% ({correct}/{total})")

        print("\n--- Overall Top 5 Models by Average Score ---")
        model_avg_scores = {}
        for model_name in set(r['model_name'] for r in successful_results):
            model_results = [r for r in successful_results if r['model_name'] == model_name]
            avg_score = sum(r['top_score'] for r in model_results) / len(model_results)
            model_avg_scores[model_name] = avg_score

        top_models = sorted(model_avg_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (model, avg_score) in enumerate(top_models, 1):
            print(f"  {i}. {model}: {avg_score:.4f}")

        print("\n--- Top 5 Fastest Models (Average Time) ---")
        model_avg_times = {}
        for model_name in set(r['model_name'] for r in successful_results):
            model_results = [r for r in successful_results if r['model_name'] == model_name]
            avg_time = sum(r['response_time_seconds'] for r in model_results) / len(model_results)
            model_avg_times[model_name] = avg_time

        fastest_models = sorted(model_avg_times.items(), key=lambda x: x[1])[:5]
        for i, (model, avg_time) in enumerate(fastest_models, 1):
            print(f"  {i}. {model}: {avg_time:.3f}s")

if __name__ == "__main__":
    main()
