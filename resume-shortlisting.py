import PyPDF2
import os
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("ResumeProcessing").getOrCreate()

# Define data scientist resume expectations
data_scientist_keywords = [
    "machine learning",
    "artificial intelligence",
    "data science",
    "algorithms",
    "natural language processing",
    "speech recognition",
    "computer vision",
    "deep learning",
    "big data",
    "data analytics",
    "business intelligence",
    "data mining",
]

# Create functions to mimic KMP algorithm
def calculate_lps_array(pattern):
    lps = [0] * len(pattern)
    i = 0
    j = 1

    while j < len(pattern):
        if pattern[i] == pattern[j]:
            lps[j] = i + 1
            i += 1
            j += 1
        else:
            if i == 0:
                lps[j] = 0
                j += 1
            else:
                i = lps[i - 1]

    return lps

def search_keyword(pattern, text):
    lps = calculate_lps_array(pattern)
    i = 0
    j = 0
    occurrences = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == len(pattern):
                occurrences += 1
                j = lps[j - 1]
        else:
            if j == 0:
                i += 1
            else:
                j = lps[j - 1]

    return occurrences

# Extract text from each PDF file and calculate its score based on data scientist keywords
def process_resume_with_kmp(file_path):
    with open(file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        file_text = ""

        for page in pdf_reader.pages:
            file_text += page.extract_text().lower()

    keyword_scores = []
    for keyword in data_scientist_keywords:
        occurrences = search_keyword(keyword, file_text)
        keyword_scores.append(occurrences)

    resume_score = sum(keyword_scores) / len(data_scientist_keywords)
    return file_path, resume_score

# Hadoop input and output paths
input_path = "hdfs://localhost:9820/dataset2/"
output_path = "hdfs://localhost:9820/shortlisted2/"

# Process resumes in parallel using Spark
resume_scores_rdd = spark.sparkContext.wholeTextFiles(input_path).map(
    lambda x: process_resume_with_kmp(x[1])
)

# Collect results to the driver
resume_scores = dict(resume_scores_rdd.collect())

# Sort resumes by score in descending order
sorted_scores = sorted(resume_scores.items(), key=lambda item: item[1], reverse=True)

# Display top 5 resumes with highest scores
print("Top 5 Resumes based on Keyword Matching Score:")
top_5_resumes = []
for index, (file_path, score) in enumerate(sorted_scores[:5]):
    print(f"Resume #{index + 1}:")
    print(f"File Path: {file_path}")
    print(f"Score: {score}")
    top_5_resumes.append(file_path)

# Move shortlisted files to the specified Hadoop output directory
for file_path in top_5_resumes:
    file_name = os.path.basename(file_path)
    destination_path = f"{output_path}/{file_name}"
    spark.sparkContext.runJob([], lambda _: os.system(f"hadoop distcp {file_path} {destination_path}"))

# Stop the SparkSession
spark.stop()
