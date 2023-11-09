#!/bin/bash

# Get the file name input
read -p "Enter the file name of the trace (Default is trace-big): " file_name

# Set default file name if empty
file_name="${file_name:-trace-big}"

# Get the integer input
read -p "Enter a cache size (Default is 255): " integer_input

# Set default integer if empty
integer_input="${integer_input:-255}"

# Get the user's choice for running belady.py (default is N)
read -p "Do you want to run belady.py? (y/N): " run_belady
run_belady="${run_belady:-n}"

# Get the list of Python scripts in the current folder excluding specific ones
python_scripts=$(ls *.py | grep -vE 'belady.py|trace-scan.py')

# Iterate over the list and run each script with the file name and integer input
for script in $python_scripts
do
  echo ""
  echo  "##################################### $script #####################################"
  echo "Running $script with file name: $file_name and integer: $integer_input"
  python3 "$script" "$file_name" "$integer_input"
done

# Check user's choice and run belady.py if requested
if [ "${run_belady,,}" == "y" ]; then
  echo ""
  echo "##################################### belady.py #####################################"
  echo "Note: Running belady.py may take significant time."
  echo "Running belady.py with file name: $file_name and integer: $integer_input"
  python3 belady.py "$file_name" "$integer_input"
fi
