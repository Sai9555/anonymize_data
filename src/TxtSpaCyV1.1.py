import spacy

# Load the spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Define a function to anonymize personal information
def anonymize_text(text):
    # Uses spaCy NER to process the input text 
    doc = nlp(text)
    # Creates an empty list to store the anonymized text
    anonymized_text = []
    # Iterates over each token in the processed text
    for token in doc:
        # Check if the token is a PERSON PLACE TIME... entity
        if token.ent_type_ in ["PERSON", "ORG", "GPE", "FAC", "DATE", "TIME"]:
            # If so, add "[ANONYMIZED]" to the anonymized text
            anonymized_text.append("[ANONYMIZED]") 
        else:
            # If not, dd the token's text to the anonymized text variable
            anonymized_text.append(token.text)
            # Join the list of tokens into a single string
    anonymized_text = " ".join(anonymized_text)
    # Print the anonymized text
    print(anonymized_text)


# Variable for participation and reuse of code
cont = input("Would you like to Anonymize text? (Y/N) ")
# If N, then stop running code.
while(cont != "N"):
    # If Y, then run the code below
  if (cont == "Y"):
    # Get input text from user
    text = input("Enter text: ")
    # Anonymize the text
    anonymize_text(text) 
  else:
    # Reasks if there is more text to be added
    print("Please enter 'Y' or 'N'")
  cont = input("More Text? (Y/N) ")

