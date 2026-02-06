# Quick Start Guide

## Step-by-Step Instructions

### 1. Make sure you're in the project directory

```bash
cd "/Users/namratamali/Documents/CityU Seattle/CityU Courses/CS622 Discrete Mathematics/Projects/Project"
```

### 2. Install Flask (if not already installed)

```bash
pip3 install Flask
```

### 3. Generate data files (if not already done)

```bash
python3 data_gen.py
```

### 4. Start the Flask server

**Option A: Using the helper script (recommended)**
```bash
python3 run_server.py
```

**Option B: Using app.py directly**
```bash
python3 app.py
```

**Option C: If port 5000 is busy, use a different port**
```bash
python3 app.py 5001
```

### 5. Open your browser

Once you see this message in the terminal:
```
============================================================
Starting Flask server on http://127.0.0.1:5000
============================================================

 * Running on http://127.0.0.1:5000
```

Open one of these URLs in your browser:
- `http://127.0.0.1:5000`
- `http://localhost:5000`

**Important:** The server must be running in the terminal. Keep that terminal window open!

### 6. If you get a 403 error

1. **Check the terminal** - Is the server actually running? You should see "Running on http://..."
2. **Try a different port** - Run `python3 app.py 5001` and use `http://localhost:5001`
3. **Kill any existing processes** on port 5000:
   ```bash
   lsof -ti:5000 | xargs kill -9
   ```
4. **Use 127.0.0.1 instead of localhost**: `http://127.0.0.1:5000`

### 7. Stop the server

Press `Ctrl+C` in the terminal where the server is running.

## Expected Output

When you start the server, you should see:

```
Initializing search engine...
Loading 15 documents...
Successfully indexed 15 documents.
Generating document citations...
Generated citations between documents.
Calculating PageRank authority scores...
Authority scores calculated.
Search engine ready!

============================================================
Starting Flask server on http://127.0.0.1:5000
============================================================

 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

If you see errors instead, check the TROUBLESHOOTING.md file.
