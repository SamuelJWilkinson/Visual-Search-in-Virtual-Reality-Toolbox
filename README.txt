// README  For Visual Attention in Virtual Reality Toolbox//

------------Visual Search Package Instructions---------------

1. Ensure that you have the TobiiPro.SDK.Unity.Windows_1.7.1.1081 Unity Package installed, provided by Tobii.
this contains all of the assets, scripts and instructions needed to setup your eye tracker and allow it to 
gather eye data througout experiments.

2. Import the custom package: VisualSearchPackage into your Unity Project.

3. Drag the SearchController prefab into your Scene ensuring that the ObjectSelection.cs script is attached as
a component to this prefab.

4. Assign a size to the Targets field in the Object Selection component.

5. Assign the assets you want to use as targets to the elements field of Targets.

6. Drag the SearchCavas prefab to be a child of the Main Camera in the Scene.

7. Ensure that the Object Selection component is correctly linked to the SearchCanvas' Target Text and the Search
Canvas prefab and Hiding UI is unchecked.

8. In the Unity Project file create a file where you want your data to be saved.

9. Within the inspector of the [VRSaveData] GameObject, ensure that save data is unchecked and you have the folder
set to the name of the folder you just created.

You are now ready to run a visual search experiment as soon as you hit the play button. Press 'ESC' key to show and
hide the UI presenting subjects with the next search task. Once the experiment has concluded XML files will be
generated for each trial.


-----------Convert XML files to CSV Files--------------

1. Run the program XMLtoCSV.py with the argument of the file that you want to convert.

python XMLtoCSV.py vr_save_data_blah.xml


-----------Post Analysis Tools----------------

1. Import the Post Analysis package into your scene.

2. Drag the Post Analysis Prefab into your scene.

3. Drag the CameraController.cs script onto the Post Analysis parent GameObject and assing the two cameras to their
relavant fields within this component.

4. Drag the WorldPos.cs onto the Camera_gaze_pos GameObjects and assign an asset to the Target field. This asset
will be placed at the gaze point of the subject so any can be used but we have included a pink cube asset for testing.

5. Ensure that the CSV data file you want to process is within the Assets folder of your Project.

6. Add in any colliders that you want to that represent semantic fields or points of interest. Eg: a box collider
representing the ceiling...

7. Press the play button and then hit space bar. You will now replay the subjects trial from both the perspective 
of the subject's head and their gaze.

8. Once the data has been run through output.csv will be created that contains data about world points and semantics.

------------Data Visualisation Tools--------------

1. Run the data visualisation program you want to see with the argument of the csv file you want to visualize the
data from.

python 3Dmap.py output.csv
python DonutMap.py output.csv
python Semantic-Analysis.py output.csv
python HeadLocomotion.py output.csv