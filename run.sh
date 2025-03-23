#!/bin/bash

# If running this gives a permission denied error run this command before ./run.sh : chmod +x run.sh

# Start FastAPI backend
echo "Starting FastAPI backend..."
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

sleep 5

# Start Streamlit frontend
echo "Starting Streamlit frontend..."
cd ../frontend
streamlit run app.py --server.port 8501

# Wait for both processes to finish (if needed)
wait
