# Use an official Python runtime as base image
FROM python:3.10-slim


# Set work directory
WORKDIR /app
# Copy requirements first (for caching)
COPY requirements.txt .
COPY data.txt .
# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

EXPOSE 5050

# Set the command to run the Flask app
CMD ["python", "app.py", "--host=0.0.0.0", "--port=5050"]