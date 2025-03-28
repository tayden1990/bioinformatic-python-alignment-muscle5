FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install wget and other necessary tools
RUN apt-get update && apt-get install -y wget && apt-get clean

# Copy application code
COPY . .

# Download MUSCLE5 for Linux
RUN wget https://drive5.com/muscle5/muscle5.1.linux_intel64 -O muscle5 && \
    chmod +x muscle5 && \
    mv muscle5 /usr/local/bin/

# Set environment variable for MUSCLE5 path
ENV MUSCLE5_PATH=/usr/local/bin/muscle5

# Expose port for the Gradio application
EXPOSE 7860

# Set entrypoint
CMD ["python", "app.py"]
