# Selecting Python version
FROM python:3.11-slim as builder

# Setting environment variables to non-interactive, this makes sure
# that apt-get does not wait for user input during execution
ENV DEBIAN_FRONTEND=noninteractive

# Installing Linux libraries and default g++ (which should support C++11)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libxml2 \
    libpq-dev \
    libblas3 \
    liblapack3 \
    liblapack-dev \
    gfortran \
    libatlas-base-dev

# Ensure that Python packages installed with --user flag are in PATH
ENV PATH="/root/.local/bin:${PATH}"

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copying requirements for python packages and installing them
WORKDIR /app
COPY env_spec/requirements.txt /app/env_spec/requirements.txt
RUN pip install --user -r env_spec/requirements.txt

# Upgrade to the latest version of mockerdb
RUN pip install --upgrade pip
RUN pip install mocker-db

# Copy and select as working directory files from pulled docker image
COPY . /app
WORKDIR /app

# Making port 80 available outside of the container
EXPOSE 8000

# Command to run the Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]