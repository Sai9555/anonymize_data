import os
import csv


def convert_txt_to_csv(folder_path):
    # Create a folder for the CSV files
    csv_folder = os.path.join(folder_path, 'csv_files')
    os.makedirs(csv_folder, exist_ok=True)

    # Iterate over the text files in the "raw" folder
    raw_folder = os.path.join(folder_path, 'raw')
    for file_name in os.listdir(raw_folder):
        if file_name.endswith('.txt'):
            txt_file = os.path.join(raw_folder, file_name)
            csv_file = os.path.join(csv_folder, f"{os.path.splitext(file_name)[0]}.csv")

            # Convert text file to CSV
            with open(txt_file, 'r') as txt_file, open(csv_file, 'w', newline='') as csv_file:
                reader = csv.reader(txt_file, delimiter='\t')
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerows(reader)

    print('Conversion completed successfully!')


# Example usage
folder_path = "../data"  # Replace with the path to your folder
convert_txt_to_csv(folder_path)
