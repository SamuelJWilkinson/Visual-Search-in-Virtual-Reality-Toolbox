import xml.etree.ElementTree as Xet
import pandas as pd
import sys
import re

cols = ["timestamp", "pos_x", "pos_y", "pos_z", "r1", "r2", "r3", "r4",\
    "l_gaze_dir_x", "l_gaze_dir_y","l_gaze_dir_z", "l_gaze_dir_valid",\
    "l_gaze_origin_x", "l_gaze_origin_y", "l_gaze_origin_z", "l_gaze_origin_valid",\
    "l_pupil", "l_pupil_valid", "l_gaze_world_origin_x", "l_gaze_world_origin_y", "l_gaze_world_origin_z",\
    "l_gaze_world_dir_x", "l_gaze_world_dir_y", "l_gaze_world_dir_z", "l_gaze_world_valid",\
    "r_gaze_dir_x", "r_gaze_dir_y","r_gaze_dir_z", "r_gaze_dir_valid",\
    "r_gaze_origin_x", "r_gaze_origin_y", "r_gaze_origin_z", "r_gaze_origin_valid",\
    "r_pupil", "r_pupil_valid", "r_gaze_world_origin_x", "r_gaze_world_origin_y", "r_gaze_world_origin_z",\
    "r_gaze_world_dir_x", "r_gaze_world_dir_y", "r_gaze_world_dir_z", "r_gaze_world_valid",\
    "cyc_gaze_origin_x", "cyc_gaze_origin_y", "cyc_gaze_origin_z",\
    "cyc_gaze_dir_x", "cyc_gaze_dir_y","cyc_gaze_dir_z", "cyc_gaze_valid",\
    "theta_x", "theta_y"]
rows = []

filename = sys.argv[1]

def parse_vector(vec):
    return [x for x in vec[1:-1].split(', ')]

def parse_valid_value(node):
    return [node.attrib['Value'], node.attrib['Valid']]

def parse_valid_vector(node):
    return [*parse_vector(node.attrib['Value']), node.attrib['Valid']]

def parse_valid_ray(node):
    return [*parse_vector(node.attrib['Origin']), *parse_vector(node.attrib['Direction']), node.attrib['Valid']]

def parse_gazedata(gazedata):
    pose = gazedata.find('Pose')
    left = gazedata.find('Left')
    right = gazedata.find('Right')
    return [
        gazedata.attrib['TimeStamp'],
        *parse_vector(pose.attrib['Position']),
        *parse_vector(pose.attrib['Rotation']),
        *parse_valid_vector(left.find('GazeDirection')),
        *parse_valid_vector(left.find('GazeOrigin')),
        *parse_valid_value(left.find('PupilDiameter')),
        *parse_valid_ray(left.find('GazeRayWorld')),
        *parse_valid_vector(right.find('GazeDirection')),
        *parse_valid_vector(right.find('GazeOrigin')),
        *parse_valid_value(right.find('PupilDiameter')),
        *parse_valid_ray(right.find('GazeRayWorld')),
        *parse_valid_ray(gazedata.find('CombinedGazeRayWorld')),
        "", # What is theta?
        ""
    ]



def main(fname):
    df = pd.DataFrame(columns=cols)
    tree = Xet.parse(fname)
    root = tree.getroot()

    for i, gazedata in enumerate(root):
        df.loc[i] = parse_gazedata(gazedata)
    return df

if __name__ == '__main__':
    df = main(filename)
    df.to_csv('output.csv')
