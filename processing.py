# File to generate useable NER data from dynamic sentences and filler inputs
# All data should be stored in separate .txt files and will get written to a .jsonl file
#
# Some code is specific to reservation NER, however it can easily be changed to any NER

import json
import csv
import random
import re
from num2words import num2words

# Define file paths for entity data
entity_files = {
    #### Reservation ####
    # "TIME": "Filler_Data/times.txt",
    # "FIRST_NAME": "Filler_Data/names.txt",
    # "LAST_NAME": "Filler_Data/names.txt",
    # "DATE": 'Filler_Data/dates.txt',
    # "TIME_CHANGE": "Filler_Data/times.txt",
    # "FIRST_NAME_CHANGE": "Filler_Data/names.txt",
    # "LAST_NAME_CHANGE": "Filler_Data/names.txt",
    # "DATE_CHANGE": 'Filler_Data/dates.txt'
    #### Order ####
    "ITEM": "Filler_Data/food_items.txt",
    "NUM": "Filler_Data/numbers.txt",
    "ADDON": "Filler_Data/addon.txt",
    "SIZE": "Filler_Data/size.txt",
    "DRINK": "Filler_Data/drink_items.txt",
    "D_ADDON": "Filler_Data/drink_addon.txt",
    "D_NUM": "Filler_Data/numbers.txt",
    "D_SIZE": "Filler_Data/drink_size.txt",
    "FIRST_NAME": "Filler_Data/names.txt",
    "LAST_NAME": "Filler_Data/names.txt",
}


# Generate a random number of people with a logarithmic distribution
def generateTextNumber():
    return int(2 + (20 - 2) * (random.random() ** 3))


def write_intent_data(output_file, input_file, num):
    # Load data from entity files
    entity_data = {}
    for label, path in entity_files.items():
        with open(path, "r") as file:
            entity_data[label] = [line.strip() for line in file.readlines()]
            entity_data[label + "_copy"] = entity_data[label].copy()

    # Load dynamic sentences from input text file
    sentences = []
    with open(input_file, "r") as file:
        sentences = [line.strip() for line in file.readlines()]

    # Copy sentences
    sentences_copy = sentences.copy()

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        for i in range(num):
            if len(sentences_copy) == 0:
                sentences_copy = sentences.copy()

            # Select a random sentence and delete from list
            selected_sentence = random.choice(sentences_copy)
            sentences_copy.remove(selected_sentence)

            # Loop until no more bracketed words are found
            pattern = re.compile(r"\{(.*?)\}")
            match = pattern.search(selected_sentence)
            while match:
                # Extract the word inside the brackets
                bracketed_word = match.group(1)
                if (
                    bracketed_word == "PARTY_SIZE"
                    or bracketed_word == "PARTY_SIZE_CHANGE"
                ):
                    random_num = num2words(generateTextNumber())
                    selected_sentence = selected_sentence.replace(
                        f"{{{bracketed_word}}}", random_num, 1
                    )
                else:
                    # Replace the bracketed word with random entity
                    random_entity = random.choice(entity_data[bracketed_word + "_copy"])
                    entity_data[bracketed_word + "_copy"].remove(random_entity)

                    # check to replace key_copy
                    if len(entity_data[bracketed_word + "_copy"]) == 0:
                        entity_data[bracketed_word + "_copy"] = entity_data[
                            bracketed_word
                        ].copy()

                    # substitute the bracketed word with random entity
                    selected_sentence = selected_sentence.replace(
                        f"{{{bracketed_word}}}", random_entity, 1
                    )
                match = pattern.search(selected_sentence)

            writer.writerow((selected_sentence, "reservation"))


def write_ner_data(output_file, input_file, num):
    # Load data from entity files
    entity_data = {}
    for label, path in entity_files.items():
        with open(path, "r") as file:
            entity_data[label] = [line.strip() for line in file.readlines()]
            entity_data[label + "_copy"] = entity_data[label].copy()

    # Load dynamic sentences from input text file
    sentences = []
    with open(input_file, "r") as file:
        sentences = [line.strip() for line in file.readlines()]

    # Copy sentences
    sentences_copy = sentences.copy()

    with open(output_file, "w") as file:
        for i in range(num):
            annotations = []
            if len(sentences_copy) == 0:
                sentences_copy = sentences.copy()

            # Select a random sentence and delete from list
            selected_sentence = random.choice(sentences_copy)
            sentences_copy.remove(selected_sentence)

            # Loop until no more bracketed words are found
            pattern = re.compile(r"\{(.*?)\}")
            match = pattern.search(selected_sentence)
            while match:
                # Extract the word inside the brackets
                bracketed_word = match.group(1)
                if (
                    bracketed_word == "PARTY_SIZE"
                    or bracketed_word == "PARTY_SIZE_CHANGE"
                ):
                    random_num = num2words(generateTextNumber())
                    selected_sentence = selected_sentence.replace(
                        f"{{{bracketed_word}}}", random_num, 1
                    )

                    # Add annotations
                    index = match.start()
                    annotations.append(
                        {
                            "startOffset": index,
                            "endOffset": index + len(random_num),
                            "displayName": bracketed_word,
                        }
                    )
                else:
                    # Replace the bracketed word with random entity
                    random_entity = random.choice(entity_data[bracketed_word + "_copy"])
                    entity_data[bracketed_word + "_copy"].remove(random_entity)

                    # check to replace key_copy
                    if len(entity_data[bracketed_word + "_copy"]) == 0:
                        entity_data[bracketed_word + "_copy"] = entity_data[
                            bracketed_word
                        ].copy()

                    # substitute the bracketed word with random entity
                    selected_sentence = selected_sentence.replace(
                        f"{{{bracketed_word}}}", random_entity, 1
                    )

                    # Add annotations
                    index = match.start()
                    annotations.append(
                        {
                            "startOffset": index,
                            "endOffset": index + len(random_entity),
                            "displayName": bracketed_word,
                        }
                    )
                match = pattern.search(selected_sentence)

            file.write(
                json.dumps(
                    {
                        "textSegmentAnnotations": annotations,
                        "textContent": selected_sentence,
                    }
                )
                + "\n"
            )


#### OUTPUT ####

# write_intent_data('Reservation/Intent/supplemental_reservation.csv', 'Reservation/NER/supplemental_reservation_ner_dynamic_sentences.txt', 100)
# write_ner_data(
#     "Reservation/NER/reservation_ner_data.jsonl",
#     "Reservation/NER/reservation_ner_dynamic_sentences.txt",
#     1000,
# )
# write_ner_data(
#     "Reservation/NER/supplemental_reservation_ner_data.jsonl",
#     "Reservation/NER/supplemental_reservation_ner_dynamic_sentences.txt",
#     50,
# )

write_ner_data(
    "Order/NER/order_res_name.jsonl",
    "Order/Intent/order_name_sentences.txt",
    500,
)
