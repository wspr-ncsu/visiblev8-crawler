import os
import re

# The path to the folder containing subfolders
folder_path = "/home/npantel/parsed_logs"

# The keyword to search for
keyword = "Found match for API"

# The keywords to exclude
exclude_keywords = ["setTimeout", "setInterval"]

# Counter for files that contain the keyword at least 5 times without the exclude_keyword in the same line
qualified_files_count = 0

# Process each file in each subfolder
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            # Counter for occurrences in the current file
            keyword_occurrences = 0

            # Read the file line by line
            for line in f:
                # Check if the line contains the keyword and does not contain the excluded keywords
                if re.search(keyword, line) and not any(
                    re.search(exclude_keyword, line)
                    for exclude_keyword in exclude_keywords
                ):
                    # Increment the per-file keyword occurrence counter
                    keyword_occurrences += 1

            # If the keyword occurs at least 5 times in the current file, increment the qualified files counter
            if keyword_occurrences >= 10:
                qualified_files_count += 1

# Display the number of qualified files
print(
    f"Files with '{keyword}' appearing at least 10 times (excluding sentences with '{exclude_keywords}'): {qualified_files_count}"
)
