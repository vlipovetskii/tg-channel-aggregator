# Use Python image
# FROM python:3.12
FROM python:3.12.9-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
# --- What is pip's `--no-cache-dir` good for? https://stackoverflow.com/questions/45594707/what-is-pips-no-cache-dir-good-for
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY *.py .

# Create logs directory
RUN mkdir -p logs

# Create session directory
RUN mkdir -p session

# Start script
CMD ["python", "tg_channel_aggregator.py"]
