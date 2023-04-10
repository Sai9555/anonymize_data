#import the spaCy library
import spacy

# Load the spaCy model for NER(this is the sm version so faster but less accurate)
nlp = spacy.load("en_core_web_sm")
# Define a function to anonymize personal information
def anonymize_text(text): 
     # Use spaCy NER to process the input text
    doc = nlp(text) 
    # Create an empty list to store the anonymized text
    anonymized_text = [] 
    # Iterate over each token in the processed text
    for token in doc:  
        # Check if the token is a ORG entity
        if token.ent_type_ == "ORG": 
            # If so, add "[ANONYMIZED]" to the anonymized text
            anonymized_text.append("[ANONYMIZED ORG]")  
            # Check if the token is a TIME entity
        elif token.ent_type_ == "TIME":
            # If so, add "[ANONYMIZED]" to the anonymized text
            anonymized_text.append("[ANONYMIZED TIME]") 
            # Check if the token is a Person entity(not working find out why)
        elif token.ent_type_ == "PERSON": 
            # If so, add "[ANONYMIZED]" to the anonymized text
            anonymized_text.append("[ANONYMIZED NAME]") 
        else:
            # Add the token's text to the anonymized text if it isn't
            anonymized_text.append(token.text) 
            # Join the list of tokens into a single string
    anonymized_text = " ".join(anonymized_text) 
    # Print the anonymized text
    print(anonymized_text)  
###############################################################################
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