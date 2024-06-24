import csv


def combine_csv_files(file_list, output_file, encoding="ISO-8859-1"):
    header_written = False

    with open(output_file, "w", newline="", encoding=encoding) as outfile:
        csv_writer = csv.writer(outfile)

        for file in file_list:
            with open(
                file, "r", newline="", encoding=encoding, errors="replace"
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


# List of CSV files to merge
file_list = [
    "Order/Intent/order.csv",
    "Out_of_Scope/out-of-scope.csv",
    "Reservation/Intent/reservation.csv",
    "Reservation/Intent/supplemental_reservation.csv",
    "confirm.csv",
    "deny.csv",
    "greeting_sentences.csv",
    "farwell_sentences.csv",
    "inquiry_data.csv",
]  # replace with your file names

# Output file name
output_file = "main_model.csv"

# Merge the CSV files
combine_csv_files(file_list, output_file)
