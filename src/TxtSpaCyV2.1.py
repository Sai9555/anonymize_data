import spacy
import re
# Load the spaCy model for NER
nlp = spacy.load("en_core_web_md")
# Define a function to anonymize personal information
def anonymize_text(text):
    # Uses spaCy NER to process the input text 
    doc = nlp(text)
    # Creates an empty list to store the anonymized text
    anonymized_text = []
    # Exclude weeks, days, and months from being anonymized
    weeks = ["months", "days", "weeks", "week", "day", "month"]
    # Iterates over each token in the processed textsample
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


fileName = input(" Input the files name here: ")
# Open the input file for reading
with open( fileName+".txt", "r") as file:
    text = file.read()

# Anonymize the text
anonymized_text = anonymize_text(text)
# Write the anonymized text to a new file
with open("anonymized_"+fileName+".txt", "w") as file:
    file.write(anonymized_text)
