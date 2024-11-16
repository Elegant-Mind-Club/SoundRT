import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

"""

SAMPLE RUN:

/Users/athenamo/miniconda3/bin/python Regression.py
Please enter the path to your CSV file: ../MeanAppendAudioVisual2R.csv                                 
The file path you entered is:../MeanAppendAudioVisual2R.csv
PLOT TITLE: Audio v.s. Visual 2R
PLOT X LABLE: Audio RT (ms)
PLOT Y LABLE: Visual RT (ms)

"""

def plot_data_with_regression(file_path, plot_title, plot_xlabel, plot_ylabel):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Check if columns exist
    if {'Visual Mean', 'Visual SEM', 'Auditory Mean', 'Auditory SEM'}.issubset(data.columns):
        x = data['Visual Mean']
        y = data['Auditory Mean']
        x_err = data['Visual SEM']
        y_err = data['Auditory SEM']
    else:
        print("The CSV file does not contain the required columns.")
        return

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    # Define the x values for the extended regression line
    x_vals = np.array([0, 500])
    regression_line = slope * x_vals + intercept

    # Plot the scatter plot with error bars and regression line
    plt.figure(figsize=(10, 6))
    plt.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='o', ecolor='gray', capsize=3, alpha=0.6, label='Data points')
    plt.plot(x_vals, regression_line, color='green', label='Regression line (Intercept)')

    plt.xlim(0, 500) # Set the x limit 
    plt.ylim(0, 500) # Set the y limit 
    plt.xticks(np.arange(0, 501, 50)) # Set the class intervals for x 
    plt.yticks(np.arange(0, 501, 50)) # Set the class intervals for y

    # Labels, title, and legend
    plt.xlabel(str(plot_xlabel))
    plt.ylabel(str(plot_ylabel))
    plt.title(str(plot_title))
    plt.legend()

    #test change

    # Show plot
    plt.show()

# Ask for file input from the user
file_path = input("Please enter the path to your CSV file: ") #enter ../ before file name (e.g. ../MeanAppendAudioVisual2R.csv)
print("The file path you entered is:" + str (file_path))
plot_title = input("PLOT TITLE: ")
plot_xlabel = input("PLOT X LABLE: ")
plot_ylabel = input("PLOT Y LABLE: ")
plot_data_with_regression(file_path, plot_title, plot_xlabel, plot_ylabel)
