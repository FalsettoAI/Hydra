import csv


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


# Example usage
input_file = "order.csv"
output_file = "main_order.csv"
reformat_csv(input_file, output_file)
