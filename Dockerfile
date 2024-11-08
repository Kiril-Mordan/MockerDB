# Collect latest image from docker registry
FROM kyriosskia/mocker-db-dependancies:latest

# Upgrade to the latest version of mockerdb
RUN pip install --upgrade pip
RUN pip install mocker-db>=0.2.6
RUN pip install package-auto-assembler>=0.5.12

# Copy and select as working directory files from pulled docker image
COPY . /app
COPY .paa.api.config /app
COPY .mockerdb.api.config /app
WORKDIR /app

# Create a persist directory
RUN mkdir -p /app/persist

# Making port 80 available outside of the container
EXPOSE 8080

# Make sure the script is executable
RUN chmod +x /app/entrypoint.sh

# Use the script as the CMD
CMD ["./entrypoint.sh"]
