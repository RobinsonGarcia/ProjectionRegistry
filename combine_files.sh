#!/bin/bash

# Bash script to combine the content of multiple files into a single text file.

# Output file
output_file="combined_files.txt"

# List of input files
files=(
    "projection/__init__.py"
    "projection/registry.py"
    "projection/processor.py"
    "projection/base/__init__.py"
    "projection/base/config.py"
    "projection/base/grid.py"
    "projection/base/interpolation.py"
    "projection/base/strategy.py"
    "projection/base/transform.py"
    "projection/gnomonic/__init__.py"
    "projection/gnomonic/config.py"
    "projection/gnomonic/grid.py"
    "projection/gnomonic/strategy.py"
)

# Get the current working directory
current_dir=$(pwd)

# Create or empty the output file
> "$output_file"

# Loop through each file and append its content to the output file
for file in "${files[@]}"; do
    full_path="$current_dir/$file"
    echo "### $full_path ###" >> "$output_file"
    if [[ -f "$full_path" ]]; then
        cat "$full_path" >> "$output_file"
    else
        echo "Error: $full_path not found." >> "$output_file"
    fi
    echo -e "\n" >> "$output_file"
done

echo "Files combined into $output_file"