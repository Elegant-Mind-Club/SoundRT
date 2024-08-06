import argparse
import csv

# FOR EASE: JUST PASS THROUGH COMMAND LINE 'python3 {code file path} {source file path} {destination file path}
def append_csv(source_file, destination_file):
    # Read the contents of the source file
    with open(source_file, 'r', newline='') as src:
        reader = csv.reader(src)
        rows = list(reader)  # Store all rows from the source file

    # Append the contents to the destination file
    with open(destination_file, 'a', newline='') as dest:
        writer = csv.writer(dest)
        writer.writerows(rows)  # Write all rows to the destination file

    print(f"Contents of {source_file} have been appended to {destination_file}")

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Append one CSV file to another.")
    parser.add_argument('source', type=str, help="Source CSV file")
    parser.add_argument('destination', type=str, help="Destination CSV file")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the append function
    append_csv(args.source, args.destination)

if __name__ == "__main__":
    main()