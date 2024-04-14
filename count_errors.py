# Define the path to the file and the keywords
file_path = "logs_mal.out"
keywords = [
    "Failed to connect to the bus",
    "Error: Failed to launch the browser process!",
    "Failed to call method:",
    "Exception: Crawler failed",
    "Exiting GPU process due to errors during initialization",
    "xcb_connect() failed, error 1",
]

# Initialize a dictionary to count each keyword
keyword_counts = {keyword: 0 for keyword in keywords}

# Open and read the file
try:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

        # Count each keyword in the file
        for keyword in keywords:
            keyword_counts[keyword] = content.count(keyword)

    # Print the counts
    for keyword, count in keyword_counts.items():
        print(f"'{keyword}': {count}")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")
