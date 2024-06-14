# File to generate useable NER data from dynamic sentences and filler inputs
# All data should be stored in separate .txt files and will get written to a .jsonl file
#
# Some code is specific to reservation NER, however it can easily be changed to any NER

import json
import random
import re
from num2words import num2words

# Define file paths for entity data
entity_files = {
    "TIME": "times.txt",
    "NAME": "names.txt",
    "DATE": 'dates.txt'
}

# Load data from entity files
entity_data = {}
for label, path in entity_files.items():
    with open(path, 'r') as file:
        entity_data[label] = [line.strip() for line in file.readlines()]
        entity_data[label + '_copy'] = entity_data[label].copy()

# Load dynamic sentences from input text file
sentences = []
with open('general_sentences.txt', 'r') as file:
    sentences = [line.strip() for line in file.readlines()]

# Copy sentences
sentences_copy = sentences.copy()

# Generate a random number of people with a logarithmic distribution
def generateTextNumber ():
    return int(2 + (20 - 2) * (random.random() ** 3))

# Generate data and write to output file
with open("general_output.jsonl", 'w') as file:
    data_count = 2000 # Number of sentences to generate
    for i in range(data_count):
        annotations = []
        if(len(sentences_copy) == 0):
            sentences_copy = sentences.copy()

        # Select a random sentence and delete from list
        selected_sentence = random.choice(sentences_copy)
        sentences_copy.remove(selected_sentence)

        # Loop until no more bracketed words are found
        pattern = re.compile(r'\{(.*?)\}')
        match = pattern.search(selected_sentence)
        while(match):    
            # Extract the word inside the brackets
            bracketed_word = match.group(1)
            if(bracketed_word == 'PARTY_SIZE'):
                random_num = num2words(generateTextNumber())
                selected_sentence = selected_sentence.replace(f"{{{bracketed_word}}}", random_num, 1)

                # Add annotations
                index = match.start()
                annotations.append({
                    "startOffset": index,
                    "endOffset": index + len(random_num),
                    "displayName": "PARTY_SIZE"
                })
            else:
                # Replace the bracketed word with random entity
                random_entity = random.choice(entity_data[bracketed_word + '_copy'])
                entity_data[bracketed_word + '_copy'].remove(random_entity)

                #check to replace key_copy
                if(len(entity_data[bracketed_word + '_copy']) == 0):
                    entity_data[bracketed_word + '_copy'] = entity_data[bracketed_word].copy()

                #substitute the bracketed word with random entity
                selected_sentence = selected_sentence.replace(f"{{{bracketed_word}}}", random_entity, 1)

                # Add annotations
                index = match.start()
                annotations.append({
                    "startOffset": index,
                    "endOffset": index + len(random_entity),
                    "displayName": bracketed_word
                })
            match = pattern.search(selected_sentence)
            

        file.write(json.dumps({"textSegmentAnnotations": annotations, "textContent": selected_sentence}) + "\n")
    