# FINAL CODE FOR DATA EXTRACTION

import PyPDF2
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import json

# function to extract name from resume


def extract_name(resume_text):
    # tokenize text
    tokens = nltk.word_tokenize(resume_text)

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if not t.lower() in stop_words]

    # extract entities
    tagged_tokens = pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged_tokens)

    # extract names
    names = []
    for entity in entities:
        if isinstance(entity, nltk.tree.Tree) and entity.label() == 'PERSON':
            name = ' '.join([leaf[0] for leaf in entity.leaves()])
            names.append(name)

    # return the first name
    if len(names) > 0:
        return names[0]
    else:
        return None

# function to extract email from resume


def extract_email(resume_text):
    # use regular expression to extract email
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, resume_text)
    if match:
        return match.group()
    else:
        return None

# function to extract phone number from resume


def extract_phone(resume_text):
    # use regular expression to extract phone number
    pattern = r'\+91\d{10}|\d{10}'
    match = re.search(pattern, resume_text)
    if match:
        return match.group()
    else:
        return None


def extract_skills(resume_text):
    # tokenize text
    tokens = nltk.word_tokenize(resume_text)

    # remove stopwords and lowercase
    stop_words = set(stopwords.words('english'))
    tokens = [t.lower() for t in tokens if not t.lower() in stop_words]

    # perform POS tagging
    tagged_tokens = nltk.pos_tag(tokens)

    # extract noun phrases that are likely to represent skills
    chunked_tokens = nltk.ne_chunk(tagged_tokens)
    skills = set([chunk.leaves()[0][0].lower() for chunk in chunked_tokens if hasattr(
        chunk, 'label') and chunk.label() == 'NP' and 'skill' in chunk.leaves()[0][0].lower()])

    return list(set(skills))


def extract_education(resume_text):
    # define a list of education keywords
    education_keywords = ['University', 'B.E', 'BTECH', 'B.A', 'B.COM' 'Bachelor',
                          'Master', 'PhD', 'Engineering', 'Computer Science', 'Mathematics', 'Statistics']

    # tokenize text
    tokens = nltk.word_tokenize(resume_text)

    # remove stopwords and lowercase
    stop_words = set(stopwords.words('english'))
    tokens = [t.lower() for t in tokens if not t.lower() in stop_words]

    # perform POS tagging
    tagged_tokens = nltk


def extract_address(resume_text):
    # use regular expression to extract address
    pattern = r'\d{1,3}\s\w+\s\w+.\s?\w+\s?\w+?\s?\d{0,3}\s?\w+\s?\w+\s?\w+'
    match = re.search(pattern, resume_text)
    if match:
        return match.group()
    else:
        return None


# example usage

# open resume file
with open('resume.pdf', 'rb') as pdf_file:
    # Read the PDF content using PyPDF2
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # Extract text from each page of the PDF file
    resume_text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        resume_text += page.extract_text()

# extract information from resume
name = extract_name(resume_text)
email = extract_email(resume_text)
phone = extract_phone(resume_text)
skills = extract_skills(resume_text)
education = extract_education(resume_text)
address = extract_address(resume_text)

# create a dictionary to store the output
output = {
    'Name': name,
    'Email': email,
    'Phone': phone,
    'Skills': skills,
    'Education': education,
    'Address': address
}

# save the output to a JSON file
with open('output.json', 'w') as f:
    json.dump(output, f)
