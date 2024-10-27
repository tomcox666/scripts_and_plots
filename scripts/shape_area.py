import json
import math
import matplotlib.pyplot as plt

def calculate_distance(p1, p2):
    return math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)

def calculate_angle(p1, p2, p3):
    a = calculate_distance(p2, p3)
    b = calculate_distance(p1, p3)
    c = calculate_distance(p1, p2)
    try:
        angle_rad = math.acos((b**2 + c**2 - a**2) / (2 * b * c))
        return math.degrees(angle_rad)
    except ValueError:
        return 0  # Handle cases where the cosine value is outside [-1, 1] due to numerical precision

def calculate_centroid(coordinates):
    x_coords = [point['x'] for point in coordinates]
    y_coords = [point['y'] for point in coordinates]
    centroid_x = sum(x_coords) / len(coordinates)
    centroid_y = sum(y_coords) / len(coordinates)
    return {'x': centroid_x, 'y': centroid_y}

def order_coordinates(coordinates):
    centroid = calculate_centroid(coordinates)
    sorted_points = sorted(coordinates, key=lambda p: math.atan2(p['y'] - centroid['y'], p['x'] - centroid['x']))
    return sorted_points

def calculate_polygon_properties(coordinates):
    ordered_coords = order_coordinates(coordinates)
    side_lengths = []
    angles = []
    num_points = len(ordered_coords)

    for i in range(num_points):
        p1 = ordered_coords[i]
        p2 = ordered_coords[(i + 1) % num_points]
        side_lengths.append(calculate_distance(p1, p2))
        p3 = ordered_coords[(i - 1 + num_points) % num_points]
        angles.append(calculate_angle(p3, p1, p2))

    area = 0.5 * abs(sum(ordered_coords[i]['x'] * (ordered_coords[(i + 1) % num_points]['y'] - ordered_coords[(i - 1) % num_points]['y']) for i in range(num_points)))

    return {"side_lengths": side_lengths, "angles": angles, "area": area}

def process_polygons_from_json(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None

    results = []
    for polygon_data in data['polygons']:
        properties = calculate_polygon_properties(polygon_data['coordinates'])
        results.append({
            "polygon": polygon_data['polygon'],
            "properties": properties
        })
    return results

def plot_polygons(results, filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error loading JSON for plotting.")
        return

    fig, ax = plt.subplots()
    for polygon_data in data['polygons']:
        ordered_coords = order_coordinates(polygon_data['coordinates'])
        x_coords = [point['x'] for point in ordered_coords]
        y_coords = [point['y'] for point in ordered_coords]
        ax.plot(x_coords + [x_coords[0]], y_coords + [y_coords[0]], marker='o')
        ax.fill(x_coords, y_coords, alpha=0.2)

    ax.set_aspect('equal')
    plt.show()

def write_results_to_json(results, output_filepath):
    with open(output_filepath, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    filepath = 'polygons.json'
    output_filepath = 'polygons_properties.json'
    results = process_polygons_from_json(filepath)
    if results:
        write_results_to_json(results, output_filepath)
        print(f"Results written to {output_filepath}")
        plot_polygons(results, filepath)
