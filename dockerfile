# Use the official Python image as the base image
FROM python:3.8.13-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required dependencies
RUN pip install --upgrade pip &&  pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade --no-cache-dir -r requirements.txt


# Copy the application code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask app
CMD ["python", "CRUD-app/app.py"]
