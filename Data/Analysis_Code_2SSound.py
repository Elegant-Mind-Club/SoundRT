import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm

# Reading the file as a CSV
data = pd.read_csv('/Users/taneeshkondapally/Downloads/Taneesh.2SrtData.2024-07-23.csv')

# Remove all trials that have boolean value False for the ‘Correct’ category.
filtered_data = data[data['Correct'] == True].copy()
 
# Calculate the data points: ReactionTime - ObjShowTime
filtered_data['TimeDifference'] = filtered_data['ReactionTime'] - filtered_data['ObjShowTime']

# Convert from seconds to milliseconds
filtered_data['TimeDifference'] *= 1000  # Convert to ms

# Remove 50 ms from all trials
filtered_data['TimeDifference'] -= 50  # Subtract 50 ms

# Separate the data into two groups based on StimType
group_v = filtered_data[filtered_data['StimType'] == 'V'].copy()
mean_v = group_v['TimeDifference'].mean()
std_v = group_v['TimeDifference'].std()
group_b = filtered_data[filtered_data['StimType'] == 'B'].copy()
mean_b = group_b['TimeDifference'].mean()
std_b = group_b['TimeDifference'].std()

# Histogram data for redCircle
hist_V, bin_edges_V = np.histogram(group_v['TimeDifference'], bins=range(int(group_v['TimeDifference'].min()), 
                  int(group_v['TimeDifference'].max()) + 25, 25), density=True)

bin_centers_red = (bin_edges_V[:-1] + bin_edges_V[1:]) / 2

# Plot the histogram and Gaussian distribution for redCircle
sns.histplot(group_v['TimeDifference'], bins=bin_edges_V, kde=False, color='#FF8080', stat='density')
plt.axvline(mean_v, color='#800000', linestyle='solid', linewidth=1, label=f'Mean: {mean_v:.2f} ms')
plt.axvline(mean_v + std_v, color='#FF0000', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_v:.2f} ms')
plt.axvline(mean_v - std_v, color='#FF0000', linestyle='dashed', linewidth=1)

# Plot Gaussian distribution for redCircle
x_fit_v = np.linspace(mean_v - 4*std_v, mean_v + 4*std_v, 1000)
y_fit_v = norm.pdf(x_fit_v, mean_v, std_v)
plt.plot(x_fit_v, y_fit_v, color='#FF0000', linewidth=2, label=f'Gaussian: μ = {mean_v:.2f} ms, σ = {std_v:.2f} ms')

plt.title('Histogram for Red Stimulus Reaction Time with Gaussian Distribution')
plt.xlabel('Reaction Time (ms)')
plt.ylabel('Frequency Density')
plt.legend()
plt.grid(False)
plt.xlim(0, 600)

# Histogram data for bCircle
hist_b, bin_edges_b = np.histogram(group_b['TimeDifference'], bins=range(int(group_b['TimeDifference'].min()), 
                  int(group_b['TimeDifference'].max()) + 25, 25), density=True)

bin_centers_b = (bin_edges_b[:-1] + bin_edges_b[1:]) / 2

# Plot the histogram and the fitted Gaussian for bCircle
sns.histplot(group_b['TimeDifference'], bins=bin_edges_b, kde=False, color='#80FF80', stat='density')
plt.axvline(mean_b, color='#008000', linestyle='solid', linewidth=1, label=f'Mean: {mean_b:.2f} ms')
plt.axvline(mean_b + std_b, color='#00FF00', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_b:.2f} ms')
plt.axvline(mean_b - std_b, color='#00FF00', linestyle='dashed', linewidth=1)

# Plot Gaussian distribution for bCircle
x_fit_b = np.linspace(mean_b - 4*std_b, mean_b + 4*std_b, 1000)
y_fit_b = norm.pdf(x_fit_b, mean_b, std_b)
plt.plot(x_fit_b, y_fit_b, color='#00FF00', linewidth=2, label=f'Gaussian: μ = {mean_b:.2f} ms, σ = {std_b:.2f} ms')

plt.title('Histogram for Auditory 2 Stimuli Reaction Time')
plt.xlabel('Reaction Time (ms)')
plt.ylabel('Frequency Density')
plt.legend(prop={'size': 5})
plt.grid(False)
plt.xlim(0, 600)

plt.tight_layout()
plt.show()
