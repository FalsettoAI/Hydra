import random
import re
import json
import csv
import os


'''
Helper Functions to manipulate/pre-process data

RULES:
- Add whatever functions you create to this file so others can use them as well. Make sure that when you add a function you provide a fairly detailed summary of the function so that others can understand what it does clearly and concisely(ask chat gpt, prompt below). 
- Try to make the function as customizable as possible, meaning putting many things into parameters so they can be easily changed without understanding the code.
- If you added a new file, clean the file of any function calls so it doesn't mess with anyone's data accidentally, and push back to github.

Chat GPT prompt for generating a proper summary of a function:

'''

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

remove_lines_with_string('Reservation/view_res.txt', 'blueprint')

# inputs a given string immediately after a specific string with a random chance
def add_string_after_string(filename, search_string, append_string, random_chance):
    # Read all lines from the file
    with open(filename, "r") as file:
        lines = file.readlines()

    # Modify the lines in memory
    for i in range(len(lines)):
        line = lines[i]
        if search_string in line:
            if random.random() < random_chance:
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


def transform_dynamic_variables(input_file_path, output_file_path):
    """
    Transforms dynamic variable names in a text file to all caps and changes {name} to {FIRST_NAME}.

    :param input_file_path: Path to the input text file.
    :param output_file_path: Path to the output text file where the transformed content will be saved.
    """
    # Regular expression pattern to match dynamic variables
    pattern = re.compile(r"\{(.*?)\}")

    with open(input_file_path, "r") as infile, open(output_file_path, "w") as outfile:
        for line in infile:
            # Function to transform the match
            def transform(match):
                variable = match.group(1)
                if variable == "name":
                    return "{FIRST_NAME}"
                else:
                    return "{" + variable.upper() + "}"

            # Use re.sub with the transform function to replace variables
            transformed_line = pattern.sub(transform, line)
            outfile.write(transformed_line)


def modify_jsonl_file(input_file_path, output_file_path):
    with open(input_file_path, "r") as input_file, open(
        output_file_path, "w"
    ) as output_file:
        for line in input_file:
            data = json.loads(line)

            if "textSegmentAnnotations" in data:
                for annotation in data["textSegmentAnnotations"]:
                    if annotation["displayName"] in ["FIRST_NAME", "LAST_NAME"]:
                        annotation["displayName"] = "NAME"

            output_file.write(json.dumps(data) + "\n")


def write_csv_from_txt(input_file, output_file, type):
    with open(input_file, "r") as file:
        sentences = file.readlines()

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        for sentence in sentences:
            writer.writerow([sentence.strip(), type])

def combine_csv_files(input_folder, output_file, encoding="ISO-8859-1"):
    header_written = False

    with open(output_file, "w", newline="", encoding=encoding) as outfile:
        csv_writer = csv.writer(outfile)

        for filename in os.listdir(input_folder):
            if filename.endswith(".csv"):
                with open(
                    os.path.join(input_folder, filename),
                    "r",
                    newline="",
                    encoding=encoding,
                    errors="replace",
                ) as infile:
                    csv_reader = csv.reader(infile)
                    if not header_written:
                        # Write the header only once
                        csv_writer.writerow(next(csv_reader))
                        header_written = True
                    else:
                        # Skip the header in subsequent files
                        next(csv_reader, None)
                    # Write the rows
                    csv_writer.writerows(csv_reader)

def reformat_csv(input_file, output_file):
    with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        for row in rows:
            if len(row) < 2:
                # Skip rows with insufficient data
                continue
            sentence = row[0]
            intents = row[1:]
            # Create the new intents list with the fixed values
            new_intents = ["order"]
            writer.writerow([sentence] + new_intents)
