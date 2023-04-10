import spacy
import os
import multiprocessing as mp
import re

nlp = spacy.load("en_core_web_md",disable = [ 'tagger', 'parser', 'textcat'])



def anonymize_persons(doc):
    anon_text = ""
    i = 0
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start = ent.start_char
            end = ent.end_char
            anon_text += doc.text[i:start] + "NAME"
            i = end
    anon_text += doc.text[i:]
    return anon_text

def anonymize_gpe(doc):
    anon_text = ""
    i = 0
    for ent in doc.ents:
        if ent.label_ == "GPE":
            start = ent.start_char
            end = ent.end_char
            anon_text += doc.text[i:start] + "LOCATION"
            i = end
    anon_text += doc.text[i:]
    return anon_text

def anonymize_org(doc):
    anon_text = ""
    i = 0
    for ent in doc.ents:
        if ent.label_ == "ORG":
            start = ent.start_char
            end = ent.end_char
            anon_text += doc.text[i:start] + "ORGANIZATION"
            i = end
    anon_text += doc.text[i:]
    return anon_text

def anonymize_date(text):
    i = 0
    anon_text = ""
    for match in re.finditer("\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", text):
        start = match.start()
        end = match.end()
        anon_text += text[i:start] + "DATE"
        i = end
    anon_text += text[i:]
    return anon_text

def anonymize_file(file_path):
    with open(file_path, "r") as f:
        text = f.read()
        doc = nlp(text)
        anon_text = anonymize_persons(doc)
        anon_text = anonymize_date(anon_text)
        with open(os.path.join("../data/processed", os.path.basename(file_path)), "w") as fw:
            fw.write(anon_text)

def main():
    input_dir = "../data/raw"
    output_dir = "../data/processed"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    print(files)
    pool = mp.Pool(processes=4)
    pool.map(anonymize_file, files)

if __name__ == "__main__":
    main()
