FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    graphviz \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml uv.lock ./
COPY backend ./backend
COPY frontend ./frontend

# Install Python dependencies
RUN pip install --no-cache-dir pip-tools && \
    pip-compile pyproject.toml --output-file=requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8001

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Set working directory to frontend
WORKDIR /app/frontend

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
