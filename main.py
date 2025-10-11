import requests
import json

# --- Configuration ---
# The URL of your running llama.cpp server
SERVER_URL = "http://localhost:8080/rerank"

# The query you want to find relevant documents for
query = "What is the capital of France?"

# A list of documents to be reranked
documents = [
    "The Eiffel Tower is a famous landmark in Paris.",
    "Paris is known for its art, fashion, and culture.",
    "Berlin is the capital of Germany.",
    "The currency of France is the Euro.",
    "The city of Paris serves as the capital of France."
]

# --- Prepare the Request ---
# Structure the data in the format required by the /rerank endpoint
payload = {
    "query": query,
    "documents": documents
}

headers = {
    "Content-Type": "application/json"
}

# --- Send the Request and Get the Response ---
try:
    print("Sending request to the reranker...")
    response = requests.post(SERVER_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    results = response.json()['results']

    # --- Process and Display the Results ---
    print("\n--- Reranked Results (from most to least relevant) ---\n")

    # Sort the results by relevance score in descending order
    sorted_results = sorted(results, key=lambda x: x['relevance_score'], reverse=True)
    
    for result in sorted_results:
        # The 'index' corresponds to the original position in your documents list
        doc_index = result['index']
        score = result['relevance_score']
        original_document = documents[doc_index]

        print(f"Score: {score:.4f}")
        print(f"Document: \"{original_document}\"\n")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
