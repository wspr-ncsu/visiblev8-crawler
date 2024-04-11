#!/bin/bash

# The path to the folder containing subfolders
folder_path="/home/npantel/parsed_logs"

# The keyword to search for
keyword="Found match for API"

# The keyword to exclude
exclude_keyword1="setTimeout"
exclude_keyword1="setInterval"

# Counter for files that contain the keyword at least 5 times without the exclude_keyword in the same line
qualified_files_count=0

# Process each file in each subfolder
for file in "$folder_path"/*/*; do
  # Counter for occurrences in the current file
  keyword_occurrences=0
  
  # Read the file line by line
  while IFS= read -r line; do
    # Check if the line contains the keyword and does not contain the excluded keyword
    if echo "$line" | grep -q "$keyword" && ! echo "$line" | grep -qE "$exclude_keyword1|$exclude_keyword2"; then
      # Increment the per-file keyword occurrence counter
      ((keyword_occurrences++))
    fi
  done < "$file"
  
  # If the keyword occurs at least 5 times in the current file, increment the qualified files counter
  if [ "$keyword_occurrences" -ge 5 ]; then
    ((qualified_files_count++))
  fi
done

# Display the number of qualified files
echo "Files with '$keyword' appearing at least 5 times (excluding sentences with '$exclude_keyword1'): $qualified_files_count"
