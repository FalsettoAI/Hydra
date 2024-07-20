import json
import os
import random
import numpy as np
from itertools import cycle
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

def replace_placeholders(sentence, entity_files):
    slots = []
    splitted = sentence.split()
    offset = 0 #number of inserted words to offset position of future slots

    for idx in range(len(splitted)):
        for placeholder, filepath in entity_files.items():
            if placeholder in splitted[idx]:
                replacement = get_random_line(filepath)
                if placeholder == 'NAME' and random.random() < 0.5: #assign two names on a 50% chance
                    replacement += " " + get_random_line(filepath)

                # get the word indices of the inputted words
                indices = []
                indices.append(idx + offset)

                # add indices for number of words in replacement
                for i in range(len(replacement.split()) - 1):
                    indices.append(indices[0] + i + 1)
                    offset += 1

                sentence = sentence.replace(placeholder, replacement, 1)
                if slots.get(placeholder) is None:
                    slots[placeholder] = [indices]
                else:
                    slots[placeholder].append(indices)
    return sentence, slots

text = "confirm booking details for ten visitor party coming on november twenty ninth"
tokens = tokenizer.tokenize(text)
print(tokens)

trained_bert = bert(input)
sequence_output = trained_bert.last_hidden_state

# process sequence output for memory
slot_memory = np.array([])
sequence_output = sequence_output[:, 1:-1, :].numpy() #remove [CLS] and [SEP]
print(sequence_output)

# process sequence output for slots
for slot, data in slots:

    # see if it starts with ##
    # then it belongs to the previous token
    if token.startswith("##"):
        slot_memory[-1].extend(sequence_output[0][idx])
    else:
        slot_memory.append(np.array([slot_id, sequence_output[0][idx]]))

print(slot_memory)

def write_joint_bert_data(output_file, input_file, num_sentences_per_file):
    # Initialize data dictionary
    data = []

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
    selected_conversations = [next(sentence_cycle) for _ in range(num_sentences_per_file)]
    
    # Find the next index to start appending new data
    next_idx = len(data)
    
    for idx, conversation in enumerate(selected_conversations):
        for sentence_data in conversation.split('|'):
            sentence_data = sentence_data.split(':')
            sentence, slots = replace_placeholders(sentence_data[1], entity_files)
            
            data[str(next_idx + idx)] = {
                "intent": sentence_data[0],
                "text": sentence,
                "slots": slots
            }

    # Write the updated data back to the output file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

def write_mutli_joint_bert_data(output_file, intent_map):
    for key, value in intent_map.items():
        if(len(value) > 1):
            write_joint_bert_data(output_file, key, value[0], value[1])
        else:
            write_joint_bert_data(output_file, key, value[0], None)
 
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


write_mutli_joint_bert_data('../Final_Datasets/JERTmate_data.json', intent_map)