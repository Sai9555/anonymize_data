import os

import dateutil
import pandas as pd
import multiprocessing as mp
import re
import dateutil.parser as dparser
import spacy


nlp = spacy.load("en_core_web_md", disable=['tagger', 'parser', 'textcat'])


def anonymize_persons(text):
    """
    Anonymize named entities of type 'PERSON' in the text.
    Replace the named entities with the string 'NAME'.
    """
    if type(text) is not str:
        return ""
    doc = nlp(text)
    anonymized_text = ""
    start_index = 0
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            anonymized_text += text[start_index:ent.start_char] + "NAME"
            start_index = ent.end_char
    anonymized_text += text[start_index:]
    return anonymized_text


def anonymize_locations(text):
    """
    Anonymize named entities of type 'GPE' (Geopolitical Entity) in the text.
    Replace the named entities with the string 'LOCATION'.
    """
    doc = nlp(text)
    anonymized_text = ""
    start_index = 0
    for ent in doc.ents:
        if ent.label_ == "GPE":
            anonymized_text += text[start_index:ent.start_char] + "LOCATION"
            start_index = ent.end_char
    anonymized_text += text[start_index:]
    return anonymized_text


def anonymize_organizations(text):
    """
    Anonymize named entities of type 'ORG' (Organization) in the text.
    Replace the named entities with the string 'ORGANIZATION'.
    """
    doc = nlp(text)
    anonymized_text = ""
    start_index = 0
    for ent in doc.ents:
        if ent.label_ == "ORG":
            anonymized_text += text[start_index:ent.start_char] + "ORGANIZATION"
            start_index = ent.end_char
    anonymized_text += text[start_index:]
    return anonymized_text


def anonymize_dates(text):
    """
    Anonymize dates in the text.
    Replace the dates with the string 'DATE'.
    """
    anonymized_text = ""
    start_index = 0
    doc = nlp(text)
    anonymized_text = ""
    start_index = 0
    for ent in doc.ents:
        if ent.label_ == "DATE":
            anonymized_text += text[start_index:ent.start_char] + "DATE"
            start_index = ent.end_char
    anonymized_text += text[start_index:]
    return anonymized_text


def anonymize_text(text):
    """
    Anonymize text by applying various anonymization functions.
    """
    anonymized_text = anonymize_persons(text)
    anonymized_text = anonymize_locations(anonymized_text)
    anonymized_text = anonymize_organizations(anonymized_text)
    anonymized_text = anonymize_dates(anonymized_text)
    return anonymized_text


def anonymize_file(data_frame, output_file):
    """
    Anonymize a single file by reading the CSV, applying anonymization, and saving the anonymized CSV.
    """
    try:
        data_frame['anonymized_text'] = data_frame['text'].apply(anonymize_text)
        data_frame.to_csv(output_file, index=False)
    except Exception as e:
        raise e


def validate_csv_file(file_path, required_columns):
    """
    Validate the existence of the CSV file and check that it contains the required columns.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    if len(df) == 0:
        raise ValueError("CSV file is empty.")

    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"CSV file is missing the following columns: {', '.join(missing_columns)}")


def main():
    input_file = "../src/output.csv"  # Path to the output.csv file
    output_file = "anonymized_output.csv"  # Filename for the anonymized output file
    try:

        validate_csv_file(input_file, ['text'])
        df = pd.read_csv(input_file)
        anonymize_df=pd.DataFrame()
        anonymize_df['anonymize_text'] = df['text'].apply(anonymize_text)
        anonymize_df.to_csv(output_file)

    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
