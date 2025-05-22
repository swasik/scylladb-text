#!/usr/bin/env python3
# Requires: pip install flask requests

from flask import Flask, request, jsonify
import argparse
import requests
import sys
import os

app = Flask(__name__)

# Global flags
USE_OPENSEARCH = False
OPENSEARCH_HOST = ""

@app.route('/api/v1/text-search/<index>/search', methods=['POST'])
def text_search(index):
    index = index.lower()
    data = request.get_json()

    # Validate request body
    if not data or 'text' not in data or 'limit' not in data:
        return jsonify({"error": "Missing 'text' or 'limit' in request body"}), 400

    text = data['text']
    try:
        limit = int(data['limit'])
    except ValueError:
        return jsonify({"error": "'limit' must be an integer"}), 400

    if USE_OPENSEARCH:
        # Send query to OpenSearch
        query = {
            "query": {
                "match": {
                    "content": text
                }
            },
            "size": limit
        }
        try:
            url = f"{OPENSEARCH_HOST}/{index}/_search"
            response = requests.get(url, json=query)
            response.raise_for_status()
            hits = response.json().get("hits", {}).get("hits", [])
            results = [hit.get("_id", "") for hit in hits]
        except requests.RequestException as e:
            return jsonify({"error": f"OpenSearch query failed: {e}"}), 500
    else:
        # Dummy implementation: generate dummy vector strings
        results = [f"vector_for_{text}_{i}" for i in range(limit)]

    return jsonify(results), 200

@app.route('/api/v1/text-search/<index>/add', methods=['POST'])
def add_document(index):
    if not USE_OPENSEARCH:
        return jsonify({"error": "OpenSearch is not enabled"}), 400

    data = request.get_json()
    if not data or 'id' not in data or 'text' not in data:
        return jsonify({"error": "Missing 'id' or 'text' in request body"}), 400

    doc_id = data['id']
    text = data['text']

    try:
        url = f"{OPENSEARCH_HOST}/{index}/_doc/{doc_id}"
        response = requests.put(url, json={"content": text})
        response.raise_for_status()
        return jsonify({"result": "Document added", "id": doc_id}), 200
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to add document: {e}"}), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Flask server or send a POST query')
    parser.add_argument('--query', help='Send a POST query instead of running the server')
    parser.add_argument('--port', type=int, default=6080, help='Port to run the server or send the query to')
    parser.add_argument('--limit', type=int, default=1, help='Limit the number of results when using query')
    parser.add_argument('--index', default="opensearch", help='Index to search or create')
    parser.add_argument('--host', default="localhost", help='host to connect to')
    parser.add_argument('--opensearch', action='store_true', help='Use OpenSearch backend')
    parser.add_argument('--create-index', action='store_true', help='Create the OpenSearch index and exit')
    args = parser.parse_args()

    USE_OPENSEARCH = args.opensearch
    OPENSEARCH_HOST = f"http://{args.host}:9200"

    if args.create_index:
        url = f"{OPENSEARCH_HOST}/{args.index}"
        try:
            response = requests.put(url, json={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "content": {"type": "text"}
                    }
                }
            })
            response.raise_for_status()
            print(f"Index '{args.index}' created successfully.")
        except requests.RequestException as e:
            print(f"Failed to create index: {e}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    if args.query:
        text = args.query
        url = f"http://{args.host}:{args.port}/api/v1/text-search/{args.index}/search"
        print(url)
        response = requests.post(url, json={"text": text, "limit": args.limit})
        print(response)
        print(response.status_code, response.json())
    else:
        app.run(debug=True, port=args.port)