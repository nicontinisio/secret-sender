FROM python:3.11-slim

# Create non-root user
RUN adduser --disabled-password --gecos "" secretuser
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY --chown=secretuser:secretuser app/ ./app
USER secretuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]