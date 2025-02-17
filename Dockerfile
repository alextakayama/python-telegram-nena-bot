# Use Python 3.11 on Debian as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the current directory to the container's working directory
COPY . .

# Launches a Spring Boot application using Gradle wrapper
CMD ["python", "src/app.py"]
