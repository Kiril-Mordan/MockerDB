#!/bin/bash

# Specify the package name
package_name="mocker-db"

# Specify the .yml file path
yml_file="env_spec/lsts_versions.yaml"

# Get the current version of the package using pip show
package_version=$(pip show $package_name | grep 'Version:' | awk '{print $2}')
if [ -z "$package_version" ]; then
    echo "Version not found for package $package_name"
    exit 1
fi

# Extract the current api_version and increment the iterator
current_api_version=$(grep '^api_version:' "$yml_file" | awk '{print $2}')
if [[ -z "$current_api_version" ]]; then
    echo "api_version not found in $yml_file"
    exit 1
fi

# Increment the iterator in the version
new_iterator=$((${current_api_version##*.} + 1))
new_api_version="${package_version}.${new_iterator}"

# Update the api_version in the YAML file
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS system, use sed with '' for in-place editing without creating a backup
    sed -i '' "s/api_version: [^ ]*/api_version: $new_api_version/" "$yml_file"
else
    # Assume Linux system, use sed with -i for in-place editing without backup
    sed -i "s/api_version: [^ ]*/api_version: $new_api_version/" "$yml_file"
fi

# Confirmation message
echo "api_version updated to $new_api_version in $yml_file"