import random
import re


def remove_duplicate_sentences(file_path):
    # Read the content of the file
    with open(file_path, "r") as file:
        sentences = file.readlines()

    # Use a set to keep track of unique sentences
    unique_sentences = set()
    cleaned_sentences = []

    for sentence in sentences:
        # Strip any leading/trailing whitespace characters
        clean_sentence = sentence.strip()
        if clean_sentence not in unique_sentences:
            unique_sentences.add(clean_sentence)
            cleaned_sentences.append(clean_sentence)

    # Write the cleaned content back to the file
    with open(file_path, "w") as file:
        for sentence in cleaned_sentences:
            file.write(sentence + "\n")


def remove_lines_with_string(file_path, string_to_remove):
    # Read all lines from the file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Filter out lines that contain the string to remove
    lines_to_keep = [line for line in lines if string_to_remove not in line]

    # Write the remaining lines back to the file
    with open(file_path, "w") as file:
        file.writelines(lines_to_keep)


# inputs a given string immediately after a specific string with a random chance
def add_string_after_string(filename, search_string, append_string):
    # Read all lines from the file
    with open(filename, "r") as file:
        lines = file.readlines()

    # Modify the lines in memory
    for i in range(len(lines)):
        line = lines[i]
        if search_string in line:
            if random.random() < 0.5:
                lines[i] = line.replace(search_string, search_string + append_string, 1)

    # Write the modified lines back to the same file
    with open(filename, "w") as file:
        file.writelines(lines)


def extract_dynamic_variables(file_path):
    """
    Extracts dynamic variables enclosed in curly braces {} from a text file.

    :param file_path: Path to the text file.
    :return: List of unique dynamic variables.
    """
    dynamic_variables = set()

    # Regular expression pattern to match dynamic variables
    pattern = re.compile(r"\{(.*?)\}")

    with open(file_path, "r") as file:
        for line in file:
            matches = pattern.findall(line)
            dynamic_variables.update(matches)

    return list(dynamic_variables)


# Example usage:
# dynamic_variables = extract_dynamic_variables('path/to/your/file.txt')
# print(dynamic_variables)


# remove_duplicate_sentences('Reservation/reservation_ner_dynamic_sentences.txt')
# remove_duplicate_sentences("goodbye.txt")
# remove_lines_with_string('Reservation/Intent/reservation_and_order_intent_dynamic_sentences.txt', 'res')
# add_string_after_string('Reservation/reservation_ner_dynamic_sentences.txt', "{FIRST_NAME}", " {LAST_NAME}")

print(extract_dynamic_variables("Order/make_order_dynamic.txt"))
