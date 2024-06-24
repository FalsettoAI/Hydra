import re
import random


# Read data from text files
def read_file(file_name):
    with open(file_name, "r") as file:
        return [line.strip() for line in file.readlines()]


# Replace placeholders with actual values
def replace_placeholders(sentence, dynamic_items):
    placeholders = re.findall(r"{(.*?)}", sentence)
    new_sentence = sentence
    for placeholder in placeholders:
        if placeholder in dynamic_items:
            replacement = random.choice(dynamic_items[placeholder])
            new_sentence = new_sentence.replace(f"{{{placeholder}}}", replacement, 1)
    return new_sentence


# Generate sentences with dynamic replacements
def generate_sentences(sentences, dynamic_items, max_sentences):
    total_base_sentences = len(sentences)
    generated_sentences = set()  # Use a set to avoid duplicates

    while len(generated_sentences) < max_sentences:
        for sentence in sentences:
            if len(generated_sentences) >= max_sentences:
                break
            new_sentence = replace_placeholders(sentence, dynamic_items)
            generated_sentences.add(new_sentence)

    return list(generated_sentences)[:max_sentences]


# Main function
def main():
    sentences = read_file("Order/Intent/order_sentences.txt")

    dynamic_parts = {
        "item": "Filler_Data/food_items.txt",
        "num": "Filler_Data/numbers.txt",
        "addon": "Filler_Data/addon.txt",
        "size": "Filler_Data/size.txt",
        "drink": "Filler_Data/drink_items.txt",
        "d_addon": "Filler_Data/drink_addon.txt",
        "d_num": "Filler_Data/numbers.txt",
        "d_size": "Filler_Data/drink_size.txt",
        "name": "Filler_Data/names.txt",
        "last_name": "Filler_Data/names.txt",
    }

    dynamic_items = {key: read_file(file) for key, file in dynamic_parts.items()}

    max_sentences = 40000
    generated_sentences = generate_sentences(sentences, dynamic_items, max_sentences)

    # Write generated sentences to a new file
    with open("order_new_sentences.txt", "w") as file:
        for sentence in generated_sentences:
            file.write(sentence + "\n")


if __name__ == "__main__":
    main()
