import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import matplotlib.cm as cm

def main(files):
    """
    Main function to plot data from CSV files with error bars.
    
    Parameters:
    - files: list of str, paths to CSV files
    """
    # Different markers for each file
    markers = ['o', '^', 's']

    # Ensure there are enough markers for the number of files
    if len(files) > len(markers):
        raise ValueError("Not enough markers for the number of files.")

    # Initialize a plot figure
    plt.figure(figsize=(9, 9))

    # Loop through each file
    for i, file in enumerate(files):
        # Read the CSV file into a DataFrame
        data = pd.read_csv(file)

        data = data.replace({r'\[': '', r'\]': ''}, regex=True)
        
        # Extract columns assuming the order: data1 mean, data1 standard error, data2 mean, data2 standard error
        data1_mean = data.iloc[:, 0].astype(float)
        data1_se = data.iloc[:, 1].astype(float)
        data2_mean = data.iloc[:, 2].astype(float)
        data2_se = data.iloc[:, 3].astype(float)

        
        # Generate colors for each data point in the file
        colors = cm.rainbow(np.linspace(0, 1, len(data1_mean)))
        
        # Plot each data point with its own color
        for j in range(len(data1_mean)):
            label = f'{i+1} Stimuli Data' if j == 0 and (i == 1 or i == 2) else 'Simple Reflex Data' if j == 0 else None  # Add label only for the first point to avoid duplicates
            plt.errorbar(data2_mean[j], data1_mean[j], xerr=data2_se[j], yerr=data1_se[j], fmt=markers[i], color=colors[j], label=label, capsize=5)


    # Add y=x reference line
    lims = [
        np.min([plt.gca().get_xlim(), plt.gca().get_ylim()]),  # min of both axes
        np.max([plt.gca().get_xlim(), plt.gca().get_ylim()]),  # max of both axes
    ]

    plt.plot([0, 700], [0, 700], 'k-', alpha=0.75, zorder=0)  # 'k-' is a solid black line
    plt.xlim(0, 700)
    plt.ylim(0, 700)

    # Add labels and legend
    plt.xlabel('Sound Data (ms)') # CHANGE THIS LABEL IF NECESSARY
    plt.ylabel('Vision Data (ms)') # CHANGE THIS LABEL IF NECESSARY
    plt.title('Sound vs Vision Data - 1, 2, 3 Stimuli, N = 10') # CHANGE THIS LABEL IF NECCESSARY
    plt.legend()
    plt.grid(False)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Plot data from CSV files with error bars.')
    
    # Define the argument to accept multiple CSV files
    parser.add_argument('files', metavar='F', type=str, nargs='+', help='CSV files to be processed')

    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Call the main function with the list of file paths
    main(args.files)