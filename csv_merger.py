import os
import csv


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


# Replace 'input_folder' with the path to the folder containing your CSV files
input_folder_path = "Order/Intent"

# Replace 'output.csv' with the path to your output CSV file
output_file_path = "order.csv"

combine_csv_files(input_folder_path, output_file_path)
