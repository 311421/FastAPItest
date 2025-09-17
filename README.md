Environment setup
-----------------

Create a `.env` file in the project root (same folder as `README.md`) with:

```
DATABASE_URL=
# Optional: use a separate DB for tests; falls back to DATABASE_URL if empty
TEST_DATABASE_URL=
```

Install dependencies and run tests:

```
pip install -r requirements.txt
pytest -q
```

Use uvicorn app.main:app --reload for project startup

