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
        for placeholder, filepath in entity_files.items():
            if placeholder in splitted[idx]:
                processed_slot = splitted[idx].split(',')
                slot_map.append(["B-" + placeholder, processed_slot[1], processed_slot[2]])

                replacement = get_random_line(filepath)
                if placeholder == 'NAME' and random.random() < 0.5: # assign two names on a 50% chance
                    replacement += " " + get_random_line(filepath)

                # add indices for number of words in replacement
                for i in range(len(replacement.split()) - 1):
                    slot_map.append(["I-" + placeholder, processed_slot[1], processed_slot[2]])

                sentence = re.sub(r'[A-Z_]+,\d+,\d+', replacement, replacement)
            else:
                slot_map.append([0,0,0])

    tokenized_sentence = tokenizer.tokenize(sentence, padding=True, truncation=True, return_tensors="tf")
    sequence_output = bert(tokenizer(sentence, padding=True, truncation=True, return_tensors="tf"))

    #remove [CLS] and [SEP]
    sequence_output = sequence_output.last_hidden_state[:, 1:-1, :]

    offset = 0
    current_slot_position = -1
    for i in range(len(sequence_output)):
        if tokenized_sentence[i].startswith("##"):
            offset += 1

        if slot_map[i - offset][0] is not 0:
            if slot_map[i - offset][0].startswith("B-"):
                current_slot_position += 1
                slot_memory[current_slot_position].extend(sequence_output[i])
            elif slot_map[i - offset][0].startswith("I-"):
                slot_memory[current_slot_position].extend(sequence_output[i])

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

def write_mutli_joint_bert_data(output_file, intent_map):
    for key, value in intent_map.items():
        if(len(value) > 1):
            compile_sentences(output_file, key, value[0], value[1])
        else:
            compile_sentences(output_file, key, value[0], None)
 
intent_map = {
    "../Add_Info/prompted_date.txt": ["add_info", 600],
    "../Add_Info/prompted_name.txt": ["add_info", 600],
    "../Add_Info/single_prompted_name.txt": ["add_info", 800],
    "../Add_Info/prompted_time.txt": ["add_info", 600],
    "../Add_Info/prompted_number.txt": ["add_info", 600],
    "../Add_Info/single_prompted_inputs.txt": ["add_info", 500],
    "../Change_Name/change_name.txt": ["change_info", 400],
    "../Confirm_Deny/confirm.txt": ["confirm"],
    "../Confirm_Deny/deny.txt": ["deny"],
    "../Greeting_Farewell/greeting.txt": ["greeting"],
    "../Greeting_Farewell/farewell.txt": ["farewell"],
    "../Inquiry/faq_policies.txt": ["faq_policies"],
    "../Inquiry/menu_inquiry.txt": ["menu_inquiry"],
    "../Order/checkout.txt": ["checkout"],
    "../Order/clear_cart.txt": ["clear_cart"],
    "../Order/delete_items.txt": ["delete_item", 10000],
    "../Order/make_order.txt": ["make_order", 10000],
    "../Order/replace_items.txt": ["replace_item", 10000],
    "../Order/view_order.txt": ["view_order"],
    "../Out_of_Scope/out_of_scope.txt": ["out_of_scope"],
    "../Reservation/add_res.txt": ["add_res", 10000],
    "../Reservation/delete_res.txt": ["delete_res", 10000],
    "../Reservation/edit_res.txt": ["edit_res", 10000],
    "../Reservation/view_res.txt": ["view_res", 10000],
}

print(process_sentence("I want to make an order for NAME,0,0", entity_files))
#write_mutli_joint_bert_data('../Final_Datasets/JERTmate_data.json', intent_map)