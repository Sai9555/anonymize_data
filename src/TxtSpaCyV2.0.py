import spacy
import re

nlp = spacy.load("en_core_web_md")


def anonymize_entities(text):
    doc = nlp(text)
    anonymized = []

    for token in doc:
        if token.ent_type_ == "PERSON":
            anonymized.append("[NAME]")
        elif token.ent_type_ in ["ORG", "GPE", "FAC"]:
            anonymized.append(token.ent_type_)
        elif re.match("\d{4}-\d{2}-\d{2}", token.text):
            anonymized.append("[DATE]")
        elif re.match("\d{2}/\d{2}/\d{4}", token.text):
            anonymized.append("DATE")
        elif re.match("\d{1,2}-\d{1,2}-\d{2,4}", token.text):
            anonymized.append("[DATE]")
        elif re.match("\d{1,2}/\d{1,2}/\d{2,4}", token.text):
            anonymized.append("[DATE]")
        elif re.match("\d{2}:\d{2}", token.text):
            anonymized.append("[TIME]")
        else:
            anonymized.append(token.text)


    return (" ".join(anonymized))


if __name__ == '__main__':
    # Open the input file for reading
    with open("../data/raw/sample_5.txt", "r") as file:
        text = file.read()
    # Anonymize the text
    anonymized = anonymize_entities(text)
    # Write the anonymized text to a new file
    with open("../data/processed/anonymized_sample.txt", "w") as file:
        file.write(anonymized)
