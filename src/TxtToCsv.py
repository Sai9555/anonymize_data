import os
import pandas as pd

# Step 1: Read your raw text files sequentially

# Step 2: Declare a variable raw_docs = []
raw_docs = []

# Step 3: Iterate over all raw files in the directory
raw_directory = '../data/raw'  # Replace '../data/raw' with the actual directory path

for filename in os.listdir(raw_directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(raw_directory, filename)
        with open(file_path, 'r') as f:
            doc_text = f.read()
            raw_docs.append(doc_text)

# Step 4: Create a pandas DataFrame from raw_doc list
df = pd.DataFrame()
df['text'] = raw_docs
df.dropna(inplace=True)
print(df)
# Step 5: Save df as CSV
output_csv = 'output.csv'  # Replace 'output.csv' with your desired file name and path
df.to_csv(output_csv, index=False)

print("CSV file saved successfully!")
