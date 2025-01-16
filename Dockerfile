FROM ubuntu:20.04
MAINTAINER scientistsoni23@gmail.com

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY .. .

# Expose the port that the app will run on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Command to run the Flask app
CMD ["flask", "run"]
