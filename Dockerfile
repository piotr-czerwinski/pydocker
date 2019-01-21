# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY *.py /app/
COPY requirements.txt /app
COPY web /app/web

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

ENV SECRET_KEY darude
ENV DATABASE_URL sqlite:////app/db/ap.db
# Run app.py when the container launches
CMD ["python3", "app.py"]
