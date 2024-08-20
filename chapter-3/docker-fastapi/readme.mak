# for testing

uvicorn app:app --reload

#docker
docker build -t fastapi-app-haystack:latest .
docker run -p 8000:8000 fastapi-app-haystack:latest

# docker command if DB not in env file
docker run -p 8000:8000 -e DATABASE_URL=postgresql://username:password@host.docker.internal:5432/database_name fastapi-app-haystack:latest

![Image](./screenshot.jpg)