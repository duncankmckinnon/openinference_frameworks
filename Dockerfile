# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/* && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.cargo/bin/uv /usr/local/bin/uv

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies using uv
RUN uv pip install --system --no-cache -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make ports available to the world outside this container
EXPOSE 8000 8080

# The actual command will be specified in docker-compose.yml
CMD ["echo", "Please use docker-compose to run the services"] 