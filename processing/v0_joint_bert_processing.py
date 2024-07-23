import json
import random
import os
import re
from itertools import cycle
import numpy as np
from transformers import AutoTokenizer
from transformers import TFBertModel

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
bert = TFBertModel.from_pretrained(model_name)

entity_files = {
    "DRIN_ADD": "../Filler_Data/drink_addon.txt",
    "TIME": "../Filler_Data/times.txt",
    "NAME": "../Filler_Data/names.txt",
    "DATE": "../Filler_Data/dates.txt",
    "ITEM": "../Filler_Data/food_items.txt",
    "NUMBER": "../Filler_Data/numbers.txt",
    "ADDON": "../Filler_Data/addon.txt",
    "SIZE": "../Filler_Data/size.txt",
    "DRINK": "../Filler_Data/drink_items.txt",
}

def get_random_line(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    return random.choice(lines).strip()

def process_sentence(sentence, entity_files):
    slot_map = []
    slot_memory = []
    splitted = sentence.split() 

    for idx in range(len(splitted)):
        is_slot = False
        print(splitted[idx])
        for placeholder, filepath in entity_files.items():
            if placeholder in splitted[idx]:
                is_slot = True
                processed_slot = splitted[idx].split(',')
                slot_map.append(["B-" + placeholder, processed_slot[1], processed_slot[2]])
                slot_memory.append([placeholder, processed_slot[1], processed_slot[2]])

                replacement = get_random_line(filepath)
                if placeholder == 'NAME' and random.random() < 0.5: # assign two names on a 50% chance
                    replacement += " " + get_random_line(filepath)

                # add indices for number of words in replacement
                for i in range(len(replacement.split()) - 1):
                    slot_map.append(["I-" + placeholder, processed_slot[1], processed_slot[2]])

                sentence = re.sub(r'[A-Z_]+,\d+,\d+', replacement, sentence, count=1)
                break
        
        if not is_slot:
            slot_map.append([0,0,0])

    tokenized_sentence = tokenizer.tokenize(sentence, padding=True, truncation=True, return_tensors="tf")
    sequence_output = bert(tokenizer(sentence, padding=True, truncation=True, return_tensors="tf")['input_ids'].numpy())

    #remove [CLS] and [SEP]
    sequence_output = sequence_output.last_hidden_state
    sequence_output = sequence_output[:, 1:-1, :].numpy()

    offset = 0
    current_slot_position = -1
    for i in range(len(sequence_output[0])):
        if tokenized_sentence[i].startswith("##"):
            offset += 1

        if slot_map[i - offset][0] != 0:
            if slot_map[i - offset][0].startswith("B-") and not tokenized_sentence[i].startswith("##"):
                current_slot_position += 1

            slot_memory[current_slot_position].extend(sequence_output[0][i])

    return sentence, slot_memory, slot_map

def compile_sentences(output_file, input_file, intent, num_sentences_per_file):
    # Initialize data dictionary
    data = {}

    # Read existing data if the output file already exists and is not empty
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, 'r') as file:
            data = json.load(file)

    # Read dynamic sentences from input file
    with open(input_file, 'r') as file:
        sentences = [line.strip() for line in file.readlines()]

    # If num_sentences_per_file is None, set it to the number of sentences in the file
    if num_sentences_per_file is None:
        num_sentences_per_file = len(sentences)
    
    # Shuffle the sentences initially
    random.shuffle(sentences)
    
    # Use a cycle to repeat sentences as needed
    sentence_cycle = cycle(sentences)
    
    # Collect the required number of sentences
    selected_sentences = [next(sentence_cycle) for _ in range(num_sentences_per_file)]
    
    # Find the next index to start appending new data
    next_idx = len(data)
    
    for idx, sentence in enumerate(selected_sentences):
        sentence, slots = process_sentence(sentence, entity_files)
        
        data[str(next_idx + idx)] = {
            "intent": intent,
            "text": sentence,
            "slots": slots
        }
    
    # Write the updated data back to the output file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

print(process_sentence("can i make a reservation for TIME,0,0 DATE,0,0", entity_files))