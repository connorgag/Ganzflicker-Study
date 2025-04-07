import os
import re
import json
from pathlib import Path

def scan_image_folders_and_update_config():
    """
    Scans the aphantasia and phantasia image folders and updates the
    config.json file with the available participant IDs and their relative image paths.
    """
    # Define folder paths - adjust these to match your project structure
    base_dir = Path(__file__).parent  # Gets the directory of this script
    images_dir_name = "images"
    aphantasia_folder_name = "aphantasia_images"
    phantasia_folder_name = "phantasia_images"

    aphantasia_dir = base_dir / images_dir_name / aphantasia_folder_name
    phantasia_dir = base_dir / images_dir_name / phantasia_folder_name
    config_file = base_dir / "config.json"

    # Compile regex to extract IDs and model names from filenames
    filename_pattern = re.compile(r'^(\d+)_([^_]+)\.(png|jpeg|jpg|webp)$')

    image_data = {
        "aphantasia_images": {},
        "phantasia_images": {}
    }

    # Scan aphantasia directory
    if aphantasia_dir.exists():
        aphantasia_images = {}
        for filename in os.listdir(aphantasia_dir):
            match = filename_pattern.match(filename)
            if match:
                participant_id = int(match.group(1))
                model_name = match.group(2)
                # Store relative path
                relative_path = f"{images_dir_name}/{aphantasia_folder_name}/{filename}"
                if participant_id not in aphantasia_images:
                    aphantasia_images[participant_id] = {}
                aphantasia_images[participant_id][model_name] = relative_path
        image_data["aphantasia_images"] = aphantasia_images
    else:
        print(f"Warning: Directory not found: {aphantasia_dir}")

    # Scan phantasia directory
    if phantasia_dir.exists():
        phantasia_images = {}
        for filename in os.listdir(phantasia_dir):
            match = filename_pattern.match(filename)
            if match:
                participant_id = int(match.group(1))
                model_name = match.group(2)
                # Store relative path
                relative_path = f"{images_dir_name}/{phantasia_folder_name}/{filename}"
                if participant_id not in phantasia_images:
                    phantasia_images[participant_id] = {}
                phantasia_images[participant_id][model_name] = relative_path
        image_data["phantasia_images"] = phantasia_images
    else:
        print(f"Warning: Directory not found: {phantasia_dir}")

    # Read existing config.json
    config = {}
    if config_file.exists():
        with open(config_file, 'r') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode existing {config_file}. Creating a new one.")

    # Only include the IDs that have all available models images
    # FIXED: Initialize new_image_data as a dictionary with the same structure as image_data
    new_image_data = {
        "aphantasia_images": {},
        "phantasia_images": {}
    }
    
    # Make sure config has available_models before using it
    available_models = config.get('available_models', [])
    
    for image_type in image_data:
        for id in image_data[image_type]:
            all_models_available = True
            for model_type in available_models:
                if model_type not in image_data[image_type][id]:
                    all_models_available = False
                    break
            
            if all_models_available:
                new_image_data[image_type][id] = image_data[image_type][id]

    # Update config with filtered image data
    config["image_paths"] = new_image_data

    # Extract and add available IDs for convenience
    config["aphantasia_ids"] = sorted(list(new_image_data["aphantasia_images"].keys()))
    config["phantasia_ids"] = sorted(list(new_image_data["phantasia_images"].keys()))

    # Write the updated config back to config.json
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    aphantasia_count = sum(len(paths) for paths in new_image_data['aphantasia_images'].values())
    phantasia_count = sum(len(paths) for paths in new_image_data['phantasia_images'].values())
    print(f"Available relative image paths written to {config_file}")
    print(f"Found {aphantasia_count} aphantasia images across {len(new_image_data['aphantasia_images'])} IDs")
    print(f"Found {phantasia_count} phantasia images across {len(new_image_data['phantasia_images'])} IDs")

    return config

if __name__ == "__main__":
    scan_image_folders_and_update_config()