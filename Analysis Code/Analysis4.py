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
        
        # Extract columns assuming the order: data1 mean, data1 standard error, data2 mean, data2 standard error
        data1_mean = data.iloc[:, 0]
        data1_se = data.iloc[:, 1]
        data2_mean = data.iloc[:, 2]
        data2_se = data.iloc[:, 3]
        
        # Generate colors for each data point in the file
        colors = cm.rainbow(np.linspace(0, 1, len(data1_mean)))
        
        # Plot each data point with its own color
        for j in range(len(data1_mean)):
            label = f'{i+1} Stimuli Data' if j == 0 and (i == 1 or i == 2) else 'Simple Reflex Data' if j == 0 else None  # Add label only for the first point to avoid duplicates
            plt.errorbar(data1_mean[j], data2_mean[j], xerr=data1_se[j], yerr=data2_se[j], fmt=markers[i], color=colors[j], label=label)
        

    # Add y=x reference line
    lims = [
        np.min([plt.gca().get_xlim(), plt.gca().get_ylim()]),  # min of both axes
        np.max([plt.gca().get_xlim(), plt.gca().get_ylim()]),  # max of both axes
    ]

    plt.plot([0, 500], [0, 500], 'k-', alpha=0.75, zorder=0)  # 'k-' is a solid black line
    plt.xlim(0, 500)
    plt.ylim(0, 500)

    # Add labels and legend
    plt.xlabel('Visual Data (ms)')
    plt.ylabel('Auditory Data (ms)')
    plt.title('Auditory vs Visual Data - 1, 2, 3 Stimuli')
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