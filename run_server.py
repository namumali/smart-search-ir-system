#!/usr/bin/env python3
"""
Simple script to run the Flask server with better error handling.
"""

import os
import sys

# Check if Flask is installed
try:
    from flask import Flask
except ImportError:
    print("Error: Flask is not installed.")
    print("Please install it using: pip3 install Flask")
    sys.exit(1)

# Check if required directories exist
if not os.path.exists('templates'):
    print("Error: 'templates' directory not found!")
    sys.exit(1)

if not os.path.exists('static'):
    print("Error: 'static' directory not found!")
    sys.exit(1)

# Import and run the app
try:
    from app import app
    
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    print("\n" + "="*60)
    print(f"Smart Search Engine - Web Interface")
    print("="*60)
    print(f"\nServer starting on: http://127.0.0.1:{port}")
    print(f"Press Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=port, threaded=True)
    
except OSError as e:
    if "Address already in use" in str(e):
        print(f"\n❌ Error: Port {port} is already in use.")
        print(f"💡 Solution: Try running with a different port:")
        print(f"   python3 run_server.py {port + 1}\n")
    else:
        print(f"\n❌ Error: {e}\n")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error starting server: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)
