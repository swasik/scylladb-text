#!/usr/bin/env python3
# Requires: pip install flask requests

from flask import Flask, request, jsonify
import argparse
import requests
import sys

app = Flask(__name__)

@app.route('/api/v1/text-search/<index>/search', methods=['POST'])
def text_search(index):
    data = request.get_json()

    # Validate request body
    if not data or 'text' not in data or 'limit' not in data:
        return jsonify({"error": "Missing 'text' or 'limit' in request body"}), 400

    text = data['text']
    try:
        limit = int(data['limit'])
    except ValueError:
        return jsonify({"error": "'limit' must be an integer"}), 400

    # Dummy implementation: generate dummy vector strings
    results = [f"amnon_{i}" for i in range(limit)]

    return jsonify(results), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Flask server or send a POST query')
    parser.add_argument('--query', nargs=3, metavar=('INDEX', 'TEXT', 'LIMIT'),
                        help='Send a POST query instead of running the server')
    parser.add_argument('--port', type=int, default=6080, help='Port to run the server or send the query to')
    args = parser.parse_args()

    if args.query:
        index, text, limit = args.query
        try:
            limit = int(limit)
        except ValueError:
            print("Limit must be an integer", file=sys.stderr)
            sys.exit(1)

        url = f"http://localhost:{args.port}/api/v1/text-search/{index}/search"
        response = requests.post(url, json={"text": text, "limit": limit})
        print(response.status_code, response.json())
    else:
        app.run(debug=True, port=args.port)
