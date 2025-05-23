FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables
ENV PORT=8000
ENV ENVIRONMENT=production
ENV FRONTEND_URL=https://your-vercel-app-url.vercel.app

# Command to run the application
CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
