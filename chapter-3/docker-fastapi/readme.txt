uvicorn app:app --reload
docker build -t fastapi-app-haystack:latest .
docker run -p 8000:8000 fastapi-app-haystack:latest