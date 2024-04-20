# Use the official Python image as base
FROM python:3.10-slim

# Install Flask
RUN pip install Flask ...

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000
EXPOSE 5000

# Run the Flask application
#CMD ["python", "app.py"]