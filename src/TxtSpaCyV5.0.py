import dateutil
import spacy
import os
import multiprocessing as mp
import re
import pandas as pd
import dateutil.parser as dparser
import csv

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
    for match in re.finditer("\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", text):
        start = match.start()
        end = match.end()
        date_str = text[start:end]
        # check if the date is not relative using dateutil.parser
        try:
            date = dparser.parse(date_str, fuzzy=True)
        except ValueError:
            date = None
        if date is not None and not dateutil.parser._isrelativedelta(date):  # exclude relative dates
            # get the unit of measurement (days, weeks, months, years)
            unit = next((w.lower() for w in text[:start].split()[-4:] if w in ["days", "weeks", "months", "years"]),
                        None)
            # anonymize the date with the unit of measurement
            anon_text += text[i:start] + f"{unit} DATE" if unit else "DATE"
        else:
            anon_text += text[i:end]
        i = end
    anon_text += text[i:]
    return anon_text


def anonymize_file(file_path, output_dir):
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(file_path)

        # Extract the text column from the DataFrame
        text_column = df['text']

        # Anonymize persons, locations, organizations, and dates in the text
        anonymized_texts = []
        for text in text_column:
            anon_text = anonymize_persons(text)
            anon_text = anonymize_gpe(anon_text)
            anon_text = anonymize_org(anon_text)
            anon_text = anonymize_date(anon_text)
            anonymized_texts.append(anon_text)

        # Create a new DataFrame with the anonymized text
        anonymized_df = pd.DataFrame({'anonymized_text': anonymized_texts})

        # Construct the output file path by joining the output directory and the base name of the input file
        output_path = os.path.join(output_dir, os.path.basename(file_path))
        output_path = output_path.replace(".csv", "_anonymized.csv")

        # Write the anonymized DataFrame to a new CSV file
        anonymized_df.to_csv(output_path, index=False)

    except FileNotFoundError:
        # If the input file is not found, print an error message
        print(f"File not found: {file_path}")
    except Exception as e:
        # If any other error occurs, print an error message with details about the error
        print(f"Error processing file {file_path}: {e}")


def main():
    input_file = "../src/output.csv"  # Path to the output.csv file
    output_dir = "../data/processed"  # Directory to store the anonymized files
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the output.csv file
    data = pd.read_csv(input_file)

    # Check if the "index" column exists in the DataFrame
    if "index" not in data.columns:
        print("Error: 'index' column not found in the CSV file.")
        return

    # Create a multiprocessing pool with 4 processes
    pool = mp.Pool(processes=4)

    # Map the anonymize_file function to each index in parallel
    pool.starmap(anonymize_file, [(index, output_dir) for index in data["index"]])

    # Close the pool and wait for the processes to finish
    pool.close()
    pool.join()

    print("Anonymization complete. Anonymized files saved in the 'processed' directory.")


if __name__ == "__main__":
    main()