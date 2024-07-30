import csv

source_file = '' # INSERT MOTHER FILE FROM GITHUB
destination_file = '' # INSERT FILE FROM GITHUB

with open(source_file, 'r', newline='') as src:
    reader = csv.reader(src)
    rows = list(reader)  # Store all rows from the source file

# Append the contents to the destination file
with open(destination_file, 'a', newline='') as dest:
    writer = csv.writer(dest)
    writer.writerows(rows)

