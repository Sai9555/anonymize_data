import spacy
import os
import multiprocessing as mp
import re
import pandas as pd

nlp = spacy.load("en_core_web_md", disable=['tagger', 'parser', 'textcat'])


def anonymize_persons(text):
    # Process the text using the spacy model.
    doc = nlp(text)
    # Initialize an empty string to store the anonymized text.
    anon_text = ""
    # Initialize a variable i to keep track of the position in the original text.
    i = 0
    # Iterate over each named entity in the text.
    for ent in doc.ents:
        # Check if the named entity is a person.
        if ent.label_ == "PERSON":
            # Get the start and end character positions of the named entity in the original text.
            start = ent.start_char
            end = ent.end_char
            # Replace the named entity with the string "NAME" in the anonymized text.
            anon_text += text[i:start] + "NAME"
            # Update the value of i to the end of the named entity in the original text.
            i = end
            # Add the remaining part of the original text to the anonymized text.
    anon_text += text[i:]
    # Return the anonymized text.
    return anon_text


def anonymize_gpe(text):
    # Load the text into the spaCy pipeline
    doc = nlp(text)
    # Initialize an empty string to store the anonymized text
    anon_text = ""
    # Initialize a pointer to the start of the text
    i = 0
    # Loop through each entity in the document
    for ent in doc.ents:
        # If the entity is classified as a GPE (geopolitical entity)
        if ent.label_ == "GPE":
            # Get the start and end positions of the entity in the text
            start = ent.start_char
            end = ent.end_char
            # Replace the entity with the string "LOCATION"
            anon_text += text[i:start] + "LOCATION"
            # Move the pointer to the end of the entity
            i = end
    # Append any remaining text to the anonymized text
    anon_text += text[i:]
    # Return the anonymized text
    return anon_text


def anonymize_org(text):
    # Load the Spacy English language model
    doc = nlp(text)
    # Initialize an empty string to store the anonymized text
    anon_text = ""
    # Initialize a variable to keep track of the current position in the text
    i = 0
    # Loop over all named entities in the text
    for ent in doc.ents:
        # If the entity is an organization
        if ent.label_ == "ORG":
            # Get the start and end character positions of the entity
            start = ent.start_char
            end = ent.end_char
            # Replace the entity with the string "ORGANIZATION"
            anon_text += text[i:start] + "ORGANIZATION"
            # Update the current position in the text to the end of the entity
            i = end
    # Append any remaining text to the anonymized string
    anon_text += text[i:]
    # Return the anonymized text
    return anon_text


def anonymize_date(text):
    i = 0
    anon_text = ""
    # Find all matches of the regular expression "\d{1,2}[/-]\d{1,2}[/-]\d{2,4}" in the input text
    for match in re.finditer("\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", text):
        # Starting index of the match
        start = match.start()
        # Ending index of the match
        end = match.end()
        # Replace the text between the previous index and the starting index of the match with "DATE"
        anon_text += text[i:start] + "DATE"
        # Update the previous index to the ending index of the match
        i = end
        # Append any remaining text after the last match
    anon_text += text[i:]
    # Return the anonymized text
    return anon_text


def anonymize_file(file_path, output_dir):
    try:
        # Open the file for reading
        with open(file_path, "r") as f:
            # Read the file's text
            text = f.read()
            # Anonymize persons in the text
            anon_text = anonymize_persons(text)
            # Anonymize locations in the text
            anon_text = anonymize_gpe(anon_text)
            # Anonymize organizations in the text
            anon_text = anonymize_org(anon_text)
            # Anonymize dates in the text
            anon_text = anonymize_date(anon_text)

        # Construct the output file path by joining the output directory and the base name of the input file
        output_path = os.path.join(output_dir, os.path.basename(file_path))
        # Open the output file for writing
        with open(output_path, "w") as f:
            # Write the anonymized text to the output file
            f.write(anon_text)
    except FileNotFoundError:
        # If the input file is not found, print an error message
        print(f"File not found: {file_path}")
    except Exception as e:
        # If any other error occurs, print an error message with details about the error
        print(f"Error processing file {file_path}: {e}")


def main():
    # Define input and output directories
    input_dir = "../data/raw"
    output_dir = "../data/processed"
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Get list of files in input directory and read in text
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    data = pd.DataFrame({"file_path": files})
    data["text"] = data["file_path"].apply(lambda x: open(x, "r").read())
    # Process files using multiprocessing
    with mp.Pool(processes=4) as pool:
        pool.starmap(anonymize_file, [(f, output_dir) for f in files])
    # Write output to CSV
    data["output_path"] = data["file_path"].apply(lambda x: os.path.join(output_dir, os.path.basename(x)))
    data[["output_path", "anonymized_text"]].apply(lambda x: x[1], axis=1).to_csv("output.csv", header=False, index=False)


if __name__ != "__main__":
    pass
else:
    main()
