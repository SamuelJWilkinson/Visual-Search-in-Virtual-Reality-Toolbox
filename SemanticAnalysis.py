import sys
import csv
from mpl_toolkits import mplot3d
from scipy.stats import mode
import numpy as np 
import matplotlib.pyplot as plt

csvFile = sys.argv[1]
color_points = []
rotation_points = []
semantic_info = []
rotations = []
x_points = []
z_points = []
x_heads = []
z_heads = []

def get_semantic_info(fname):
    total_lines = sum(1 for line in open(fname)) - 1
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # These are the header names
                line_count += 1
            elif line_count < total_lines:
                color_points.append(line_count)
                # Add these valus to an array
                x_points.append(float(row[2]))
                z_points.append(float(row[4]))
                x_heads.append(float(row[5]))
                z_heads.append(float(row[7]))
                semantic_info.append((row[8]))
                line_count += 1

def create_pie():
    semantic_ratio =  np.unique(semantic_info, return_counts = True)
    return semantic_ratio

def calculate_rotations(frame_skip):
    rotation_count = 0
    # For each frame
    for i in range(len(x_points) - frame_skip):
        # Look at the next 'frame_skip' frames
        next_looks = []
        g1 = [x_points[i], z_points[i]]
        for each in range(frame_skip):
            g2 = [x_points[i + each], z_points[i + each]]
            p = [x_heads[i], z_heads[i]]

            value = ((g1[0] - p[0]) * (g2[1] - p[1])) - ((g1[1] - p[1]) * (g2[0] - p[0]))

            if value > 0:
                next_looks.append('Clockwise')
            elif value < 0:
                next_looks.append('Anticlockwise')
        a = mode(next_looks)
        rotations.append(a[0][0])
        rotation_count += 1
        rotation_points.append(rotation_count)
    rotation_ratio = np.unique(rotations, return_counts= True)
    return rotation_ratio


def main(fname):
    get_semantic_info(fname)
    semantic_ratio = create_pie()
    fig = plt.figure(figsize=plt.figaspect(0.5))

    labels = []
    for i in range(len(semantic_ratio[1])):
        labels.append(semantic_ratio[0][i] + ', ' + str(semantic_ratio[1][i]))

    # Pie chart of semantic distribution
    ax = fig.add_subplot(2, 3, 1)
    ax.pie(semantic_ratio[1], labels = labels)
    ax.set_title('Semantic Information Distribution')

    # Bar chart of semantic distribution
    ax = fig.add_subplot(2, 3, 2)
    ax.bar(labels, semantic_ratio[1])
    ax.set_title('Semantic Information Distribution')
    ax.set_ylabel('Datapoint')

    # Time chart to show semantic distribution
    ax = fig.add_subplot(2, 3, 3)
    ax.scatter(color_points, semantic_info, c = color_points, cmap = 'jet')
    ax.set_title('Semantic Information over Trial Period')
    ax.set_xlabel('Datapoint')

    rotation_ratio = calculate_rotations(100)
    rot_labels = []
    for i in range(len(rotation_ratio[1])):
        rot_labels.append(rotation_ratio[0][i] + ', ' + str(rotation_ratio[1][i]))
    
    ax = fig.add_subplot(2, 3, 4)
    ax.pie(rotation_ratio[1], labels = rot_labels)
    ax.set_title('Gaze Rotation Distribution')

    ax = fig.add_subplot(2, 3, 5)
    ax.bar(rot_labels, rotation_ratio[1])
    ax.set_title('Gaze Rotation Distribution')
    ax.set_ylabel('Datapoint')

    ax = fig.add_subplot(2, 3, 6)
    ax.scatter(rotation_points, rotations, c = rotation_points, cmap = 'jet')
    ax.set_title('Gaze Rotation over Trial Period')
    ax.set_xlabel('Datapoint')

    plt.show()

if __name__ == '__main__':
    main(csvFile)