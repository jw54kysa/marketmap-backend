# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose HTTPS port
EXPOSE 8000

# Start the app (default command if not overridden)
# "--ssl-keyfile=key.pem", "--ssl-certfile=cert.pem"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 
