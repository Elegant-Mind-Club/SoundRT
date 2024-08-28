import pandas as pd
import argparse

def process_csv(input_file_path, output_file_path):
    # Step 1: Read the CSV file, skipping the first line initially
    data = pd.read_csv(input_file_path, skiprows=1)
    data = data[data['Correct'] == 1]
    
    # Step 2: Read the first line to get the two variables
    with open(input_file_path, 'r') as file:
        first_line = file.readline().strip()
    variables = list(map(float, first_line.split(',')))

    # Extract variables from the first line
    first_number, second_number = variables
    first_number = first_number + 25200
    

    # Step 3: Perform the calculations
    data.iloc[:, 1] = data.iloc[:, 1] / 1000000  # COLUMN 1: SECONDS
    data.iloc[:, 2] = data.iloc[:, 2] / 1000    # COLUMN 2: MILLISECONDS

    data.iloc[:, 1] = data.iloc[:, 1] + first_number  # Add to the first column
    data.iloc[:, 1] = data.iloc[:, 1] - (second_number/1000000)

    data.iloc[:, 2] = data.iloc[:, 2] + (first_number*1000)
    data.iloc[:, 2] = data.iloc[:, 2] - (second_number/1000) # Subtract from the second column

    data.iloc[:, 1] = data.iloc[:, 1]
    data.iloc[:, 2] = data.iloc[:, 2] - 50


    # Step 4: Save the processed data to the output file path
    data.to_csv(output_file_path, index=False)

    print(f"Processing complete. The new file is saved as '{output_file_path}'.")

def main():
    parser = argparse.ArgumentParser(description='Process a CSV file with specific calculations.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file')
    parser.add_argument('output_file', type=str, help='Path to the output CSV file where the results will be saved')

    args = parser.parse_args()

    process_csv(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
