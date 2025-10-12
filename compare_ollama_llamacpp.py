#!/usr/bin/env python3
"""
Compare Ollama vs llama-server reranking performance.

Tests the same query with both implementations to see if results match.
"""

import requests
import json

# Test query
QUERY = "what is a panda?"
DOCUMENTS = [
    "The giant panda is a bear species endemic to China.",
    "The red panda is a small mammal native to the eastern Himalayas.",
    "Panda Express is an American fast food restaurant chain.",
    "A panda is a popular icon in conservation efforts.",
    "Pandas eat bamboo as their primary food source."
]

def test_ollama():
    """Test Ollama's rerank endpoint."""
    print("Testing Ollama...")
    url = "http://localhost:11434/api/rerank"
    payload = {
        "model": "bge-reranker-test",
        "query": QUERY,
        "documents": DOCUMENTS
    }

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()

    print(f"Model: {data['model']}")
    print(f"Total Duration: {data.get('total_duration', 0) / 1_000_000:.2f}ms")
    print("\nResults:")
    for i, result in enumerate(data['results'], 1):
        print(f"  {i}. [{result['index']}] Score: {result['relevance_score']:.4f}")
        print(f"     {result['document'][:80]}...")

    return data['results']

def test_llamacpp():
    """Test llama-server's rerank endpoint."""
    print("\nTesting llama-server (brew)...")
    url = "http://localhost:8080/rerank"
    payload = {
        "query": QUERY,
        "documents": DOCUMENTS
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        print("Results:")
        results = data['results']
        # Sort by relevance_score descending
        sorted_results = sorted(results, key=lambda x: x['relevance_score'], reverse=True)

        for i, result in enumerate(sorted_results, 1):
            print(f"  {i}. [{result['index']}] Score: {result['relevance_score']:.4f}")
            doc = DOCUMENTS[result['index']]
            print(f"     {doc[:80]}...")

        return sorted_results
    except requests.exceptions.ConnectionError:
        print("  ✗ llama-server not running. Start with:")
        print("    llama-server -m ~/Documents/reranking-models/bge-reranker-v2-m3-Q4_K_M.gguf --port 8080 --rerank")
        return None

def compare_results(ollama_results, llamacpp_results):
    """Compare rankings from both implementations."""
    if llamacpp_results is None:
        return

    print("\n" + "=" * 80)
    print("COMPARISON")
    print("=" * 80)

    print("\nRanking Comparison:")
    print(f"{'Rank':<6} {'Ollama Index':<14} {'llama-server Index':<18} {'Match'}")
    print("-" * 60)

    max_len = max(len(ollama_results), len(llamacpp_results))
    matches = 0

    for i in range(max_len):
        ollama_idx = ollama_results[i]['index'] if i < len(ollama_results) else None
        llama_idx = llamacpp_results[i]['index'] if i < len(llamacpp_results) else None

        match = "✓" if ollama_idx == llama_idx else "✗"
        if ollama_idx == llama_idx:
            matches += 1

        print(f"{i+1:<6} {str(ollama_idx):<14} {str(llama_idx):<18} {match}")

    print(f"\nRanking Agreement: {matches}/{max_len} ({100*matches/max_len:.1f}%)")

    print("\nScore Comparison:")
    print(f"{'Rank':<6} {'Ollama Score':<15} {'llama-server Score':<20} {'Diff'}")
    print("-" * 60)

    for i in range(max_len):
        ollama_score = ollama_results[i]['relevance_score'] if i < len(ollama_results) else None
        llama_score = llamacpp_results[i]['relevance_score'] if i < len(llamacpp_results) else None

        if ollama_score is not None and llama_score is not None:
            diff = abs(ollama_score - llama_score)
            print(f"{i+1:<6} {ollama_score:<15.4f} {llama_score:<20.4f} {diff:.4f}")
        else:
            print(f"{i+1:<6} {str(ollama_score):<15} {str(llama_score):<20} N/A")

def main():
    print("=" * 80)
    print("OLLAMA vs llama-server RERANK COMPARISON")
    print("=" * 80)
    print(f"\nQuery: {QUERY}")
    print(f"Documents: {len(DOCUMENTS)}")
    print("=" * 80)
    print()

    ollama_results = test_ollama()
    llamacpp_results = test_llamacpp()

    compare_results(ollama_results, llamacpp_results)

if __name__ == "__main__":
    main()
