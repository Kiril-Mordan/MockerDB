#!/bin/bash

# Specify the .yml file path
yml_file="env_spec/lsts_versions.yaml"

# Read the api_version from the YAML file
api_version=$(grep '^api_version:' "$yml_file" | awk '{print $2}')
if [[ -z "$api_version" ]]; then
    echo "api_version not found in $yml_file"
    exit 1
fi


git config --local user.email "action@github.com"
git config --local user.name "GitHub Action"
git pull origin HEAD:main

# Add updated versions file
git add env_spec/lsts_versions.yaml
git commit -m "Update configuration to $api_version"

# Create a new tag with the api_version
git tag -a "$api_version" -m "API version $api_version"
# Push changes and tags to remote
git push && git push --tags

# Confirmation message
echo "Repository tagged with api_version $api_version"
