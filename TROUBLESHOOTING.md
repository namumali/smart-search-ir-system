# Troubleshooting Guide

## HTTP 403 Error on localhost:5000

If you're getting a "403 Forbidden" error when accessing `http://localhost:5000`, try these solutions:

### Solution 1: Check if the server is running

Make sure you've started the Flask server:

```bash
python3 app.py
```

Or use the helper script:

```bash
python3 run_server.py
```

### Solution 2: Port 5000 is already in use

If port 5000 is busy, use a different port:

```bash
python3 app.py 5001
```

Then access: `http://localhost:5001`

### Solution 3: Kill the process using port 5000

On macOS/Linux:

```bash
# Find the process
lsof -ti:5000

# Kill it (replace PID with the number from above)
kill -9 PID

# Or kill all Python processes (use with caution)
pkill -f "python.*app.py"
```

On Windows:

```bash
# Find the process
netstat -ano | findstr :5000

# Kill it (replace PID with the number from above)
taskkill /PID PID /F
```

### Solution 4: Use 127.0.0.1 instead of localhost

Try accessing:
```
http://127.0.0.1:5000
```

### Solution 5: Check Flask installation

Make sure Flask is installed:

```bash
pip3 install Flask
```

Verify installation:

```bash
python3 -c "import flask; print(flask.__version__)"
```

### Solution 6: Check directory structure

Make sure these directories exist:
- `templates/` (with `index.html`)
- `static/` (with `style.css` and `script.js`)
- `data/` (with document files)

### Solution 7: Check file permissions

Make sure the files are readable:

```bash
chmod -R 755 templates static data
```

### Solution 8: Clear browser cache

Sometimes browsers cache error pages. Try:
- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Or use incognito/private browsing mode

### Solution 9: Check firewall/antivirus

Some security software blocks localhost connections. Temporarily disable to test.

### Solution 10: Verify the server started correctly

When you run `python3 app.py`, you should see:

```
Initializing search engine...
Loading X documents...
Successfully indexed X documents.
...
============================================================
Starting Flask server on http://127.0.0.1:5000
============================================================

 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

If you see errors, fix them before trying to access the URL.

## Common Error Messages

### "Address already in use"
- Port is busy, use Solution 2 or 3

### "Template not found"
- Make sure `templates/index.html` exists
- Check you're running from the project root directory

### "Module not found"
- Make sure you're in the project directory
- Install Flask: `pip3 install Flask`

### "Permission denied"
- Check file permissions (Solution 7)
- On macOS, you might need to grant Terminal full disk access

## Still having issues?

1. Check the terminal output when running the server - it will show error messages
2. Make sure you're accessing the correct URL (check the port number in terminal)
3. Try a different browser
4. Check if Python 3 is being used: `python3 --version`
