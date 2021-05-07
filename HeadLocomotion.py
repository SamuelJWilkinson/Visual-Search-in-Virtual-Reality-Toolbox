import sys
import csv
from mpl_toolkits import mplot3d
import numpy as np 
import matplotlib.pyplot as plt

csvFile = sys.argv[1]
x_points = []
y_points = []
z_points = []
color_points = []
heat_points  = []

def headDisplacement():
    x_distance = np.array(x_points) - x_points[0]
    y_distance = np.array(y_points) - y_points[0]
    z_distance = np.array(z_points) - z_points[0]
    return str(np.sum(np.abs(x_distance) + np.abs(y_distance) + np.abs(z_distance)))

def headDisplacementFromCenter():
    x_distance = x_points - np.mean(x_points)
    y_distance = y_points - np.mean(y_points)
    z_distance = z_points - np.mean(z_points)
    return str(np.sum(np.abs(x_distance) + np.abs(y_distance) + np.abs(z_distance)))
 
def verticalDisplacement():
    y_distance = np.array(y_points) - y_points[0]
    return str(np.sum(np.abs(y_distance)))

def verticalDisplacementFromCenter():
    y_distance = y_points - np.mean(y_points)
    return str(np.sum(np.abs(y_distance)))


def getDatPoints(fname):
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
                x_points.append(float(row[5]))
                y_points.append(float(row[6]))
                z_points.append(float(row[7]))
                line_count += 1

def main(fname):
    getDatPoints(fname)

    fig = plt.figure(figsize=plt.figaspect(0.5))

    ax = fig.add_subplot(2, 2, 1, projection='3d')
    ax.plot(x_points[0],z_points[0],0)
    ax.scatter3D(x_points, z_points, y_points, c = color_points, cmap = 'rainbow')
    ax.set_title('Head Movement in World Space \n Head Locomotion Displacement is: ' + headDisplacement())
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Z coordinate')
    ax.set_zlabel('Y coordinate')

    ax = fig.add_subplot(2, 2, 2, projection='3d')
    ax.scatter3D(x_points, z_points, y_points, c = color_points, cmap = 'rainbow')
    ax.set_title('Head Movement within Head Space \n Head Locomotion Displacement from Mean: ' + headDisplacementFromCenter())
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Z coordinate')
    ax.set_zlabel('Y coordinate')

    ax = fig.add_subplot(2, 2, 3)
    ax.plot(0)
    ax.plot(y_points)
    ax.set_title('Vertical Head Locomotion within Head Space \n Vertical Displacement is: ' + verticalDisplacement())
    ax.set_xlabel('Datapoint')
    ax.set_ylabel('Height (m)')

    ax = fig.add_subplot(2, 2, 4)
    ax.plot(y_points)
    average_y = np.mean(y_points)
    ax.plot( (0, len(x_points)) , (average_y, average_y), linestyle = 'dotted')
    ax.set_title('Vertical Head Locomotion within Head Space \n Vertical Displacement from Mean Head Position: ' + verticalDisplacementFromCenter())
    ax.set_xlabel('Datapoint')
    ax.set_ylabel('Height (m)')

    plt.show()

if __name__ == '__main__':
    main(csvFile)
