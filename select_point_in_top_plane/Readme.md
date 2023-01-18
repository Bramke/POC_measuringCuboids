# Select a point in the top plane of a cuboid - TOOL
This script is a tool that helps you select the top plane of a point cloud. It reads a point cloud from a .ply file, applies filtering and resampling. It tries to find a plane in the given pointcloud. The script will then show a visualisation with the found plane in blue color, and the remaining pointcloud in red. The user will be asked if the top plane is colored in blue. If not, the script will try to find another plane. The script will continue to iterate until the correct plane is found. When the top plane is found the script will return the centroid (point in the center of the found plane) of the plane.

## Requirements
The script requires the following libraries:
```
Python3
Open3D
pyransac3d
time
```

## Usage
- Make sure that the point cloud is in the same directory as the script.
- Run the script by typing python select_point_in_top_plane.py in the command line.
- Enter the name of the .ply file when prompted, not including the .ply extension.
- Follow the instructions in the command line until the script is finished.
- The script will return the x, y and z coordinate of the centroid of the top plane, this data will also be saved in the coordinates.txt file.
- You can now use the x, y and z coordinate centroid of the top plane in the measuring_cuboid algorithm.

## Customization
You can customize the script by changing the parameters of the plane fitting function and the cleaning process to adapt it to different types of point clouds or use cases.

## Example
You can try pointcloud1.ply as an example, this file is included in the repository.