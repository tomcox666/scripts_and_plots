import os
import random
import shutil

def create_dummy_file(file_path, size_mb):
    """Creates a dummy file of a specified size in MB."""
    with open(file_path, 'wb') as f:
        f.write(os.urandom(size_mb * 1024 * 1024))

def generate_test_files(base_dir, num_files=5):
    """Generates a set of dummy video files for testing."""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    file_names = [
        "The Matrix.mp4",
        "The Matrix (1999).mp4",
        "A Beautiful Mind.mkv",
        "A_Beautiful_Mind.mkv",
        "Goodfellas.avi",
        "Goodfellas_HD.avi",
        "The_Godfather.mov",
        "The Godfather (1972).mov",
        "Avatar.mp4",
        "Avatar_2022.mp4"
    ]

    # Create some duplicate files
    duplicates = [
        ("The Matrix (1999)_copy.mp4", "The Matrix.mp4"),  # Duplicate of The Matrix
        ("Goodfellas_Duplicate.avi", "Goodfellas.avi"),   # Duplicate of Goodfellas
        ("Avatar_Duplicate.mp4", "Avatar.mp4")            # Duplicate of Avatar
    ]

    # Create original files with random sizes
    for file_name in file_names:
        size_mb = random.randint(1, 10)  # Random size between 1 MB and 10 MB
        create_dummy_file(os.path.join(base_dir, file_name), size_mb)

    # Create duplicate files with the same content
    for duplicate_name, original_name in duplicates:
        shutil.copyfile(
            os.path.join(base_dir, original_name),
            os.path.join(base_dir, duplicate_name)
        )

    print(f"Test files created in {base_dir}")

# Example usage:
test_folder = "./test_video_folder"
generate_test_files(test_folder)
