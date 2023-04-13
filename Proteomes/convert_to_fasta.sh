#!/bin/bash

input_dir="$1"
output_dir="$2"

if [ ! -d "$input_dir" ]; then
  echo "Input directory does not exist."
  exit 1
fi

if [ ! -d "$output_dir" ]; then
  echo "Output directory does not exist. Creating it now."
  mkdir -p "$output_dir"
fi

for file in "$input_dir"/*.out; do
  base_name=$(basename "$file" .out)
  output_file="$output_dir/$base_name.fasta"

  awk 'BEGIN {ORS=""} /^>/ {print "\n" $0 "\n"} !/^>/ {print}' "$file" > "$output_file"
done

echo "Conversion completed."
