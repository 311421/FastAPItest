Environment setup
-----------------

Create a `.env` file in the project root (same folder as `README.md`) with:

```
DATABASE_URL=
TEST_DATABASE_URL=
```

Install dependencies and run tests:

```
pip install -r requirements.txt
pytest -q
```

Use uvicorn app.main:app --reload for project startup

Docker image can be found at: https://hub.docker.com/repositories/tegrasgt

