# Simple RPG Web Game

A minimal RPG-style web game built with FastAPI, HTMX, TailwindCSS and SQLite.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

## Testing

```bash
pytest
```
