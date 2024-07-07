import json
import random
import os

entity_files = {
    #### Reservation ####
    "TIME": "../Filler_Data/times.txt",
    "NAME": "../Filler_Data/names.txt",
    "DATE": "../Filler_Data/dates.txt",
    "ITEM": "../Filler_Data/food_items.txt",
    "NUM": "../Filler_Data/numbers.txt",
    "ADDON": "../Filler_Data/addon.txt",
    "SIZE": "../Filler_Data/size.txt",
    "DRINK": "../Filler_Data/drink_items.txt",
    "D_ADDON": "../Filler_Data/drink_addon.txt",
    "D_NUM": "../Filler_Data/numbers.txt",
    "D_SIZE": "../Filler_Data/drink_size.txt",
}

def get_random_line(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    return random.choice(lines).strip()

def replace_placeholders(sentence, entity_files):
    positions = {}
    for placeholder, filepath in entity_files.items():
        while placeholder in sentence:
            replacement = get_random_line(filepath)
            start = sentence.index(placeholder)
            end = start + len(replacement)
            sentence = sentence.replace(placeholder, replacement, 1)
            positions[placeholder] = [start, end]
    return sentence, positions

def write_joint_bert_data(output_file, input_file, num):
    # Read existing data if the output file already exists
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            data = json.load(file)
    else:
        data = {}
    
    # Read dynamic sentences from input file
    with open(input_file, 'r') as file:
        sentences = [line.strip() for line in file.readlines()]
    
    # Find the next index to start appending new data
    next_idx = len(data)
    
    for idx, sentence in enumerate(sentences):
        sentence, positions = replace_placeholders(sentence, entity_files)
        
        slots = {placeholder: sentence[start:end] for placeholder, (start, end) in positions.items()}
        
        data[str(next_idx + idx)] = {
            "intent": intent,
            "text": sentence,
            "slots": slots,
            "positions": positions
        }
    
    # Write the updated data back to the output file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage:
input_file = '../dynamic_sentences.txt'  # Your input file with dynamic sentences
output_file = 'processed_data.json'  # The output JSON file
intent = 'AddToPlaylist'  # The intent for the sentences

write_joint_bert_data(input_file, output_file, intent)