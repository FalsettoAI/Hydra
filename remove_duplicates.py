def remove_duplicate_sentences(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
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
    with open(file_path, 'w') as file:
        for sentence in cleaned_sentences:
            file.write(sentence + '\n')

# Example usage:
file_path = 'delete_res.txt'
remove_duplicate_sentences(file_path)