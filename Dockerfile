FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv sync

# Ensure data is present
RUN uv run scripts/download_iris.py

# Default command
CMD ["uv", "run", "dvc", "repro"]
