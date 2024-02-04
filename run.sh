#!/bin/bash

# Set the name of your virtual environment
VENV_NAME="venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_NAME" ]; then
    echo $VENV_NAME
    echo "Creating virtual environment..."
    python3 -m venv $VENV_NAME
fi

# Activate the virtual environment
source $VENV_NAME/bin/activate
echo "Virtual environment started"


# Set the path to your requirements.txt file
requirements_file="requirements.txt"

# Check if the requirements file exists
if [ ! -f "$requirements_file" ]; then
    echo "Error: requirements file not found at $requirements_file"
    exit 1
fi

# Read package names from requirements file into an array
readarray -t packages < "$requirements_file"

# Check and install missing packages
missing_packages=()
for package in "${packages[@]}"; do
    package=$(echo "$package" | tr -d '\r\n')  # Remove newline characters
    if ! pip show "$package" >/dev/null 2>&1; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -eq 0 ]; then
    echo "All packages are already installed."
else
    echo "Installing missing packages: ${missing_packages[@]}"
    pip install "${missing_packages[@]}"
fi

echo "starting application"
python3 run.py