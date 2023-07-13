# Use an official Python runtime as the base image
FROM python:3.9

# Install Redis server
RUN apt-get update && apt-get install -y redis-server

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . .

# Expose the ports for Django and Redis
EXPOSE 8000
EXPOSE 6379

# Specify the command to run Django project
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Run Redis server
CMD redis-server --daemonize yes && python manage.py runserver 0.0.0.0:8000