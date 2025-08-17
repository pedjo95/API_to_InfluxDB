# Use a minimal official Python image to keep the final image size small.
# The `3.11-slim` tag is based on Debian and is a great choice for production.
FROM python:3.11-slim

# Set the working directory inside the container.
# All subsequent commands will be executed from this directory.
WORKDIR /app

# Copy the requirements file into the working directory.
# This step is cached by Docker, so it only re-runs if requirements.txt changes.
COPY requirements.txt .

# Install the dependencies from the requirements.txt file.
# The --no-cache-dir flag reduces the size of the final image.
# We also run a single `RUN` command to combine these steps into one layer,
# which is a best practice for Dockerfile optimization.
RUN pip install --no-cache-dir \
    prometheus-client \
    requests

# Copy the rest of the application code into the container.
COPY . .

# Define the command to run when the container starts.
# This assumes you have a main Python script named 'main.py'
# If your application has a different entry point, you can change this.
CMD ["python", "main.py"]
