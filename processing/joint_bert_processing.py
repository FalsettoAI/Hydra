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

def write_joint_bert_data(output_file, input_file, intent):
    # Initialize data dictionary
    data = {}
    
    # Read existing data if the output file already exists and is not empty
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, 'r') as file:
            data = json.load(file)
    
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

def write_mutli_joint_bert_data(output_file, intent_map):
    for key, value in intent_map.items():
        write_joint_bert_data(output_file, key, value)

intent_map = {
    "../Add_Info/prompted_date.txt": "add_info",
    "../Add_Info/prompted_name.txt": "add_info",
    "../Add_Info/prompted_time.txt": "add_info",
    "../Add_Info/prompted_number.txt": "add_info",
    "../Change_Name/change_name.txt": "add_info",
    "../Confirm_Deny/confirm.txt": "confirm",
    "../Confirm_Deny/deny.txt": "deny",
    "../Greeting_Farewell/greeting.txt": "greeting",
    "../Greeting_Farewell/farewell.txt": "farewell",
    "../Inquiry/faq_policies.txt": "faq_policies",
    "../Inquiry/menu_inquiry.txt": "menu_inquiry",
    "../Order/checkout.txt": "checkout",
    "../Order/clear_cart.txt": "clear_cart",
    "../Order/delete_items.txt": "delete_item",
    "../Order/make_order.txt": "make_order",
    "../Order/replace_items.txt": "replace_item",
    "../Order/view_order.txt": "view_order",
    "../Out_of_Scope/out_of_scope.txt": "out_of_scope",
    "../Reservation/add_res.txt": "add_res",
    "../Reservation/delete_res.txt": "delete_res",
    "../Reservation/edit_res.txt": "edit_res",
    "../Reservation/view_res.txt": "view_res",
}


write_mutli_joint_bert_data('../Final_Datasets/JERTmate_data.json', intent_map)
#write_joint_bert_data('../Final-Datasets/JERTmate_data.json', '../Add-Info/prompted_date.txt', 'confirm')