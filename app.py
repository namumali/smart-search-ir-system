"""
Flask Web Application
Main server for the search engine web interface.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os

# Initialize Flask app
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Enable CORS if needed (for development)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

from engine import SearchEngine

# Initialize search engine (loads on startup)
print("Initializing search engine...")
engine = SearchEngine()
print("Search engine ready!")


@app.route('/')
def index():
    """
    Render the homepage with search interface.
    """
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {e}", 500


@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    """
    API endpoint for autocomplete suggestions.
    Accepts JSON: {'prefix': '...'}
    Returns JSON: ['suggestion1', 'suggestion2', ...]
    """
    try:
        data = request.get_json()
        prefix = data.get('prefix', '').strip()
        
        if not prefix:
            return jsonify([])
        
        # Get suggestions from engine
        suggestions = engine.get_suggestions(prefix)
        
        return jsonify(suggestions)
    
    except Exception as e:
        print(f"Error in autocomplete: {e}")
        return jsonify([])


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    API endpoint for search queries.
    Accepts: query parameter (GET) or JSON {'query': '...'} (POST)
    Returns: JSON with search results
    """
    try:
        # Handle both GET and POST requests
        if request.method == 'GET':
            query = request.args.get('query', '').strip()
        else:
            data = request.get_json()
            query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'results': []})
        
        # Perform search
        results = engine.search(query)
        
        # Format results for frontend
        formatted_results = []
        for result in results:
            formatted_results.append({
                'title': result['title'],
                'url': result['url'],
                'snippet': result['snippet'],
                'score': round(result['score'], 4)
            })
        
        return jsonify({'results': formatted_results})
    
    except Exception as e:
        print(f"Error in search: {e}")
        return jsonify({'results': []})


if __name__ == '__main__':
    import sys
    # Try port 5000, if it's busy try 5001
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    print(f"\n{'='*60}")
    print(f"Starting Flask server on http://127.0.0.1:{port}")
    print(f"{'='*60}\n")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=port, threaded=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\nError: Port {port} is already in use.")
            print(f"Try running: python3 app.py {port + 1}")
            print(f"Or kill the process using port {port} first.\n")
        else:
            raise
