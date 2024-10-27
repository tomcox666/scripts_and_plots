import numpy as np
import open3d as o3d

# Load and inspect the .ply file
ply_data = o3d.io.read_point_cloud("inputs/bearder_guy.ply")
points = np.asarray(ply_data.points)

# Print first few points to inspect structure
print(points.dtype)
print(points[:5])