#!/bin/bash

# Specify the package name
package_name="mocker-db"

# Specify the .yml file path
yml_file="env_spec/lsts_versions.yaml"

# Get the current version of the package using pip show
version=$(pip show $package_name | grep 'Version:' | awk '{print $2}')
if [ -z "$version" ]; then
    echo "Version not found for package $package_name"
    exit 1
fi

# Check if we're on macOS and adjust the sed command accordingly
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS system, use sed with '' for in-place editing without backup
    sed -i '' "s/\($package_name: *\).*/\1$version/" "$yml_file"
else
    # Assume Linux system, use sed with -i for in-place editing without backup
    sed -i "s/\($package_name: *\).*/\1$version/" "$yml_file"
fi

# Confirmation message
echo "$package_name version updated to $version in $yml_file"