import sys
import csv
import numpy as np 
import matplotlib.pyplot as plt

csvFile = sys.argv[1]
x_points = []
z_points = []
x_origin_points = []
z_origin_points = []
color_points = []
clip_distance = 8.0

def getDatPoints(fname):
    global x_points
    global z_points
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
                x_origin_points.append(float(row[5]))
                z_origin_points.append(float(row[7]))
                line_count += 1
    x_points = np.minimum(x_points, clip_distance)
    z_points = np.minimum(z_points, clip_distance)
    x_points = np.maximum(x_points, -clip_distance)
    z_points = np.maximum(z_points, -clip_distance)

def main(fname):
    getDatPoints(fname)
    fig, ax = plt.subplots(1, 2, figsize=plt.figaspect(0.5))
    ax[0].scatter(x_points, z_points, s = 2 ,c = color_points, cmap = 'rainbow')
    ax[0].set_title('Top down map of gaze points')
    ax[0].set_xlabel('X coordinate')
    ax[0].set_ylabel('Z coordinate')

    norm_color_points = color_points / np.max(color_points)
    cmap = plt.cm.get_cmap('rainbow')
    for i in range(len(x_points)):
        ax[1].plot((x_points[i],x_origin_points[i]),(z_points[i],z_origin_points[i]), c = cmap(norm_color_points[i]))
    ax[1].scatter(x_points, z_points, s = 2 ,c = color_points, cmap = 'rainbow')
    ax[1].set_title('Top down map of gaze vectors')
    ax[1].set_xlabel('X coordinate')
    ax[1].set_ylabel('Z coordinate')
    # Purple shows initial glance and rainbows outwards
    plt.show()

if __name__ == '__main__':
    main(csvFile)
