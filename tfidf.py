import os
from collections import defaultdict
import numpy as np

# Define the list of terms we're interested in
terms = [
    "socialSignup",
    "facebook",
    "twitter",
    "google",
    "jscrypto",
    ".connected",
    "storage.set",
    "storage.get",
    "storage.sync.get",
    "storage.sync.set",
    "cookies.set",
    "cookies.get",
    "browser.cookies",
    "window.location",
    "window.height",
    "window.width",
    "navigator.userAgent",
    "isChrome",
    "isFirefox",
    "__REACT_DEVTOOLS_GLOBAL_HOOK__",
    "chrome.devtools.network",
    "chrome.storage.sync.get('visitorId')",
    "window.location.href",
    "/recaptcha/api2/",
    "CaptchaMessage",
    "getUserMedia",
    "AudioContext",
    "addEventListener('keyup')",
    "addEventListener('click')",
    "notificationMsg",
    "notification",
    "options",
    "click",
    "settings",
    ".filter",
    "url.search",
    "window.addEventListener(DOMContentLoaded",
    "fetch",
    "math.random",
]


# Function to traverse directories and count term frequencies
def get_term_frequencies(directory):
    term_counts = defaultdict(int)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = (
                            f.read().lower()
                        )  # Read and convert content to lowercase
                        for term in terms:
                            term_counts[term] += content.count(term)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return term_counts


# Function to compare frequencies
def compare_frequencies(freq_a, freq_b):
    more_in_a = sum(freq_a[term] > freq_b[term] for term in terms)
    more_in_b = sum(freq_b[term] > freq_a[term] for term in terms)
    return more_in_a, more_in_b


# Paths to the directories
dir_a = "/home/npantel/vv8-crawler-slim-v5/celery_workers/vv8_worker/vv8_crawler/merged_folder_6_parts"
dir_b = "/home/npantel/vv8-crawler-slim-v5/celery_workers/vv8_worker/vv8_crawler/ALL_EXTENSIONS1k"

# Calculate term frequencies for both directories
frequencies_a = get_term_frequencies(dir_a)
frequencies_b = get_term_frequencies(dir_b)

# Compare the frequencies and print the result
more_in_a, more_in_b = compare_frequencies(frequencies_a, frequencies_b)
print(f"Terms more frequent in Directory A: {more_in_a}")
print(f"Terms more frequent in Directory B: {more_in_b}")


# import os
# import glob
# from collections import defaultdict
# from sklearn.feature_extraction.text import TfidfVectorizer

# # List of JavaScript APIs to track
# javascript_apis = [
#     "socialSignup",
#     "facebook",
#     "twitter",
#     "google",
#     "jscrypto",
#     ".connected",
#     "storage.set",
#     "storage.get",
#     "storage.sync.get",
#     "storage.sync.set",
#     "cookies.set",
#     "cookies.get",
#     "browser.cookies",
#     "window.location",
#     "window.height",
#     "window.width",
#     "navigator.userAgent",
#     "isChrome",
#     "isFirefox",
#     "__REACT_DEVTOOLS_GLOBAL_HOOK__",
#     "chrome.devtools.network",
#     "chrome.storage.sync.get('visitorId')",
#     "window.location.href",
#     "/recaptcha/api2/",
#     "CaptchaMessage",
#     "getUserMedia",
#     "AudioContext",
#     "addEventListener('keyup')",
#     "addEventListener('click')",
#     "notificationMsg",
#     "notification",
#     "options",
#     "click",
#     "settings",
#     ".filter",
#     "url.search",
#     "window.addEventListener(DOMContentLoaded",
#     "fetch",
#     "math.random",
# ]


# # Function to read all .js files in a directory (recursively)
# def read_js_files(directory):
#     all_texts = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith(".js"):
#                 file_path = os.path.join(root, file)
#                 try:
#                     with open(file_path, "r", encoding="utf-8") as file:
#                         all_texts.append(file.read())
#                 except:
#                     continue
#     return all_texts


# # Function to compute TF-IDF
# def compute_tfidf(texts):
#     vectorizer = TfidfVectorizer(vocabulary=javascript_apis, stop_words="english")
#     tfidf_matrix = vectorizer.fit_transform(texts)
#     feature_names = vectorizer.get_feature_names_out()
#     return tfidf_matrix, feature_names


# # Main function to process directories
# def process_directories(dir_a, dir_b):
#     texts_a = read_js_files(dir_a)
#     texts_b = read_js_files(dir_b)

#     # Compute TF-IDF for directory A and B
#     tfidf_a, feature_names = compute_tfidf(texts_a)
#     tfidf_b, _ = compute_tfidf(texts_b)

#     # Get dense representation for comparison
#     dense_a = tfidf_a.todense()
#     dense_b = tfidf_b.todense()

#     # Display TF-IDF results
#     print("TF-IDF for Directory A:")
#     print(dense_a)
#     print("\nTF-IDF for Directory B:")
#     print(dense_b)


# # Specify the paths to your directories
# dir_a = "/home/npantel/vv8-crawler-slim-v5/celery_workers/vv8_worker/vv8_crawler/merged_folder_6_parts"
# dir_b = "/home/npantel/vv8-crawler-slim-v5/celery_workers/vv8_worker/vv8_crawler/ALL_EXTENSIONS1k"

# # Process both directories
# process_directories(dir_a, dir_b)
