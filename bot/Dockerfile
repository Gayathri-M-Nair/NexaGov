FROM python:3.10-slim

# Set memory-efficient environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONMALLOC=malloc
ENV OMP_NUM_THREADS=2
ENV MALLOC_TRIM_THRESHOLD_=100000

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 4002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
  CMD curl -f http://localhost:4002/ || exit 1

# Run with memory limits
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4002", "--workers", "1"]
