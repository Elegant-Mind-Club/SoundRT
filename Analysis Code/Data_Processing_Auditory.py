import pandas as pd
import argparse
import re

def process_data(df, output_file_path):
    
    df.columns = df.columns.str.strip()
    
    # Step 1: Remove any trials that are False in the 'Correct' column
    df = df[df['Correct'] == 1]

    # Step 2: Generate a new column 'TimeDifference' by doing ReactionTime - ObjShowTime
    df['TimeDifference'] = df['ReactionTime'] - df['ObjShowTime']

    """# Step 3: Subtract 50 ms from all trials
    df['TimeDifference'] -= 50"""

    # Step 4: Remove outliers using the 1.5*IQR method
    Q1 = df['TimeDifference'].quantile(0.25)
    Q3 = df['TimeDifference'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df['TimeDifference'] >= lower_bound) & (df['TimeDifference'] <= upper_bound)]
    del df['TimeDifference']
    df.to_csv(output_file_path, index=False)
    df2 = pd.read_csv(output_file_path)
    df2.to_csv(output_file_path, index=False)
    print(f"Processing complete. The new file is saved as '{output_file_path}'.")

def process_csv(input_file_path, output_file_path):
    # Step 1: Read the CSV file, skipping the first line initially
    data = pd.read_csv(input_file_path, skiprows=1)
    
    # Step 2: Read the first line to get the two variables
    with open(input_file_path, 'r') as file:
        first_line = file.readline().strip()
        first_line = re.sub(r'[^\d.,-]', '', first_line)
    # Extract variables from the first line
    variables = list(map(float, first_line.split(',')))
    # Remove any empty strings and convert to float
    try:
        variables = [float(num) for num in variables if num]
    except ValueError as e:
        print(f"Error converting line to floats: {e}")
    # Extract variables from the first line
    first_number, second_number = variables
    first_number = first_number + 25200
    

    # Step 3: Perform the calculations
    data.iloc[:, 0] = data.iloc[:, 0] / 1000 
    data.iloc[:, 1] = data.iloc[:, 1] / 1000  

    data.iloc[:, 0] = data.iloc[:, 0] + (first_number*1000)  # Add to the first column
    data.iloc[:, 0] = data.iloc[:, 0] - (second_number/1000)

    data.iloc[:, 1] = data.iloc[:, 1] + (first_number*1000)
    data.iloc[:, 1] = data.iloc[:, 1] - (second_number/1000) # Subtract from the second column

    process_data(data, output_file_path)


def main():
    parser = argparse.ArgumentParser(description='Scatter plot of means with SEM error bars and y=x reference line.')
    parser.add_argument('file_pairs', nargs='+', type=str, help='Pairs of CSV files separated by a comma, e.g., "visual1.csv,auditory1.csv visual2.csv,auditory2.csv"')
    args = parser.parse_args()
    for pair in args.file_pairs:
        try:
            input_file, output_file = pair.split(',')
        except ValueError:
            print(f"Error: File pair '{pair}' is not in the correct format. Ensure it is in 'file1,file2' format.")
            continue
        process_csv(input_file, output_file)

if __name__ == '__main__':
    main()
