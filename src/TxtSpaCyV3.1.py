import re
import spacy
import os
# Load the spaCy model for NER
nlp = spacy.load("en_core_web_md")

def anonymize_text(text):
    # Uses spaCy NER to process the input text 
    doc = nlp(text)
    # Creates an empty list to store the anonymized text
    anonymized_text = []
    # Exclude weeks, days, and months from being anonymized
    weeks = ["week", "weeks", "day", "days", "month","months"]
    # Iterates over each token in the processed text
    for token in doc:
        # Check if the token is a week, day, or month
        if token.text in weeks:
            # If so, add the token's text to the anonymized text variable
            anonymized_text.append(token.text)
        else:
            # Check if the token is a PERSON, ORG, GPE, FAC, DATE, or TIME entity
            if token.ent_type_ in ["PERSON", "ORG", "GPE", "FAC", "DATE", "TIME"] or \
                re.match("\d{3}-\d{2}-\d{4}", token.text) or \
                re.match("\d{3} \d{2} \d{4}", token.text) or \
                re.match("\d{2}/\d{2}/\d{2}", token.text)and \
                not token.ent_type_ == "MED" and \
                not token.ent_type_ == "MEDICINE":
                # If so, add "[ANONYMIZED]" to the anonymized text
                anonymized_text.append("[ANONYMIZED]")
            else:
                # If not, add the token's text to the anonymized text variable
                anonymized_text.append(token.text)
    # Join the list of tokens into a single string
    anonymized_text = " ".join(anonymized_text)
    # Return the anonymized text
    return anonymized_text


# Define the path to the folder containing the files
folder_path = "RAW/"
num = 0
# Check if the folder path exists
if os.path.exists(folder_path):
    # Iterate through the files in the folder
    for file_name in os.listdir(folder_path):
        # Skip files that are not .txt files
        if not file_name.endswith(".txt"):
            continue
        # Open the file for reading
        with open(folder_path + file_name, "r") as file:
            text = file.read()
        # Anonymize the text
        anonymized_text = anonymize_text(text)
        num+=1
        # Write the anonymized text to a new file in the Processed folder
        with open("processed/ANONYMIZED_" + str(num)+".txt", "w") as file:
            file.write(anonymized_text)
else:
    # If the folder path does not exist, raise an error
    raise FileNotFoundError("The folder path '" + folder_path + "' does not exist")
