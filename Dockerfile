# Use Python 3.6.3 as a base image
From python:3.6-slim-buster
# Prevent Docker from outputting to stdout
ENV PYTHONBUFFERED 1
# Make a directory called "code" which will contain the source code. This will be used as a volume in our docker-compose.yml file
RUN mkdir /code
# Add the contents of the hello_earth directory to the code directory
ADD . /code
# Set the working directory for the container. I.e. all commands will be based out of this directory
WORKDIR /code
# Install all dependencies required for this project. the trusted-host flag is useful if you are behind a corporate proxy.
RUN pip install --trusted-host pypy.org --trusted-host files.pythonhosted.org -r requirements.txt