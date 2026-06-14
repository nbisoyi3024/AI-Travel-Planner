# Use a small Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (faster rebuilds if code changes but deps don't)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files
COPY . .

# Cloud Run sets PORT env variable — Streamlit must listen on it
ENV PORT=8080

# Run Streamlit on the port Cloud Run expects
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0