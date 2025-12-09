#!/bin/bash
export DATABASE_URL='postgresql://user:password@localhost:5432/churn_db'
./venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000 --reload

