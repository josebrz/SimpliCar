FROM python:3.9

ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /simplicar

# Set the working directory to /simplicar_apì
WORKDIR /simplicar

# Copy the current directory contents into the container at /simplicar
ADD . /simplicar/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt