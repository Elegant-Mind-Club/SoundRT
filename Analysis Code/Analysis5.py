import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
import re
from collections import defaultdict
import matplotlib.cm as cm

def parse_participant_files(file_paths):
    """
    Groups the input file paths by participant name.
    """
    participant_files = defaultdict(list)
    for path in file_paths:
        basename = os.path.basename(path)
        match = re.match(r"(\w+)_MeanAppendTouchSound.*\.csv", basename)
        if match:
            participant = match.group(1)
            participant_files[participant].append(path)
    return participant_files

def main(file_paths):
    participant_files = parse_participant_files(file_paths)

    plt.figure(figsize=(9, 9))
    markers = ['o', '^', 's']
    cmap = cm.get_cmap('tab10')  # Up to 10 unique participant colors

    for i, (participant, paths) in enumerate(sorted(participant_files.items())):
        color_base = cmap(i % 10)  # Wrap around if more than 10 participants
        paths_sorted = sorted(paths, key=lambda x: ['SR', '2R', '3R'].index(re.search(r'(SR|2R|3R)', x).group(1)))

        for j, file in enumerate(paths_sorted):  # Ensure SR, 2R, 3R order
            df = pd.read_csv(file).replace({r'\[|\]': ''}, regex=True).astype(float)

            for k in range(2):  # Row 0 = same hand (dark), Row 1 = diff hand (light)
                x = df.iloc[k, 0]
                xerr = df.iloc[k, 1]
                y = df.iloc[k, 2]
                yerr = df.iloc[k, 3]

                alpha = 1.0 if k == 0 else 0.4
                color = color_base[:3] + (alpha,)
                label = f"Participant #{i+1} - {j+1} Stimulus" if k == 0 else None

                plt.errorbar(
                    x, y, xerr=xerr, yerr=yerr,
                    fmt=markers[j], color=color,
                    label=label, capsize=5
                )

    # Reference line
    plt.plot([0, 1000], [0, 1000], 'k-', alpha=0.75, zorder=0)
    plt.xlim(0, 1000)
    plt.ylim(0, 1000)
    plt.xlabel('Touch Data (ms)')
    plt.ylabel('Sound Data (ms)')
    plt.title('Touch vs Sound Data - All Participants (Same Hand vs Different Hand)')
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot multi-participant data from CSVs.')
    parser.add_argument('files', metavar='F', type=str, nargs='+', help='List of CSV files (multiple participants)')
    args = parser.parse_args()
    main(args.files)
