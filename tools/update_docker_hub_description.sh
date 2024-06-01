#!/bin/bash

# Usage: ./script.sh <username> <password> <repository_name>

# Check if all parameters are provided
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <username> <password> <repository_name>"
  exit 1
fi

USERNAME=$1
PASSWORD=$2
REPOSITORY=$3

# Read the README.md content
description=$(<README.md)

# Escape newlines and double quotes for JSON
description=$(echo "$description" | sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/\\n/g' -e 's/"/\\"/g')

# Get the JWT token
token=$(curl -s -H "Content-Type: application/json" -X POST -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" https://hub.docker.com/v2/users/login/ | jq -r .token)

# Update the Docker Hub repository description
curl -s -X PATCH https://hub.docker.com/v2/repositories/$USERNAME/$REPOSITORY/ \
    -H "Content-Type: application/json" \
    -H "Authorization: JWT $token" \
    -d "{\"full_description\": \"$description\"}"
