import open3d as o3d
import numpy as np
import pyransac3d as pyrsc
import time, os

# Print in a dark blue color
print("\033[34m" + "Welcome to the point selection tool!" + "\033[0m")
print("\033[34m" + "This tool will help you select a point in the top plane of a point cloud." + "\033[0m")
print("\033[34m" + "Please make sure that the point cloud is in the same directory as this script." + "\033[0m")
print("\033[34m" + "Enter the name of the .ply file: " + "\033[0m")
file_name = input()

# Import point cloud
print("Importing the point cloud...")
original_pcd = o3d.io.read_point_cloud(file_name + ".ply")
if(len(original_pcd.points) == 0):
    print("\033[31m" + "No points found in the point cloud." + "\033[0m")
    print("\033[34m" + "Make sure that the point cloud is in the same directory as this script, and that the file name is correct." + "\033[0m")
    exit()


# Cleaning the point cloud
print("Cleaning the point cloud: ")
# print in a dark blue color
print("\033[34m" + "  - Removing outliers" + "\033[0m")
cleaned_pcd, ind = original_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
cleaned_pcd, ind = cleaned_pcd.remove_radius_outlier(nb_points=10, radius=0.01)
print("\033[34m" + "  - Voxel downsampling" + "\033[0m")
cleaned_pcd = cleaned_pcd.voxel_down_sample(voxel_size=0.005)

def find_plane(pcd):
  # Create a plane object
  plane = pyrsc.Plane()

  # Convert the points to a numpy array
  pcd_array = np.asarray(pcd.points)

  # Fit plane to point cloud
  best_eq, best_inliers = plane.fit(pcd_array, thresh=0.005)
  return best_inliers

point_found = False
index = 0

original_pcd = cleaned_pcd

while not point_found:
  outlier_cloud = cleaned_pcd
  # print in blue color
  print("\033[94m" + f"Number of points remaining in the pointcloud: {len(outlier_cloud.points)}" + "\033[0m")
  index += 1
  # Find the top plane
  print("Finding a plane...")
  best_inliers = find_plane(outlier_cloud)
  # Export the inliers to a new point cloud
  inlier_cloud = cleaned_pcd.select_by_index(best_inliers)
  inlier_cloud.paint_uniform_color([0, 0, 1])
  # Visualize the found plane (blue) and the remaining points (red)
  print("Close the visualization window to continue")
  visualization_pcd = original_pcd.select_by_index(best_inliers, invert=True)
  visualization_pcd.paint_uniform_color([1, 0, 0])

  o3d.visualization.draw_geometries([inlier_cloud, visualization_pcd])

  print("\033[92m" + f"Number of points in found plane: {len(inlier_cloud.points)}" + "\033[0m")

  # Ask user if the top plane is now a different color
  print("\033[95m" + "Is the top plane now blue? (y/n), enter STOP to stop: " + "\033[0m", end="")

  answer = input()
  try: 
    if answer == "y":
        point_found = True
        print("\033[92m" + "Great!" + "\033[0m")

        # Find the centroid of the found plane
        centroid = np.mean(inlier_cloud.points, axis=0)
        
        # Print in a darkgreen color
        print("\033[32m" + f"Centroid of the top plane: {centroid}" + "\033[0m")
        print("\033[32m" + f"top_plane_point_x = {centroid[0]}" + "\033[0m")
        print("\033[32m" +  f"top_plane_point_y = {centroid[1]}" + "\033[0m")
        print("\033[32m" + f"top_plane_point_z = {centroid[2]}" + "\033[0m")
        print("You can copy the values above to your code.")
        
        # Export the coordinates to a file
        # Create a new file or append to the existing one
        file_mode = 'a' if os.path.exists('coordinates.txt') else 'w'

        with open('coordinates.txt', file_mode) as f:
            f.write('----------------------------------------\n')
            f.write(f'fileName = {file_name}\n')
            f.write(f'top_plane_point_x = {centroid[0]}\n')
            f.write(f'top_plane_point_y = {centroid[1]}\n')
            f.write(f'top_plane_point_z = {centroid[2]}\n')
            f.write('----------------------------------------\n')


        # Wait 2 seconds
        time.sleep(2)
        print("You should now see a visualisation of the found point in the top plane (grey sphere).")

        # Visualize the centroid
        found_point = o3d.geometry.TriangleMesh.create_sphere(radius=0.01)
        found_point.translate(centroid)
        found_point.paint_uniform_color([0.5, 0.5, 0.5])
        o3d.visualization.draw_geometries([found_point, original_pcd])

    elif answer == "STOP":
        print("Stopping.")
        point_found = True
        exit()

    elif answer == "n":
        print("\033[91m" + "Let's try again." + "\033[0m")
        # outlier_cloud = outlier_cloud.select_by_index(best_inliers, invert=True)
        # outlier_cloud.paint_uniform_color([1, 0, 0])
        cleaned_pcd = cleaned_pcd.select_by_index(best_inliers, invert=True)  
        # Repeat the process
    else:
        # Throw an error
        Exception("Please enter y, n or STOP")
  except Exception as e:
    # print in a red color
    print("\033[91m" + "Error: "  + e + "\033[0m", end="")
