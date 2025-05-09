import os
import re
import json
from pathlib import Path

def scan_image_folders_and_update_config():
    """
    Scans the aphantasia and phantasia image folders and the participant_data folder,
    and updates the config.json file with the available participant IDs and their relative image paths.
    Updated to handle the filename format: {id}_{model name}_{1, 2, 3, or 4}.{image type}
    """
    # Define folder paths - adjust these to match your project structure
    base_dir = Path(__file__).parent  # Gets the directory of this script
    images_dir_name = "images"
    participant_data_folder_name = "participant_data"
    aphantasia_folder_name = "aphantasia_images"
    phantasia_folder_name = "phantasia_images"

    aphantasia_dir = base_dir / images_dir_name / aphantasia_folder_name
    phantasia_dir = base_dir / images_dir_name / phantasia_folder_name
    participant_data_dir = base_dir / participant_data_folder_name
    config_file = base_dir / "config.json"
    
    # Define available models directly in the code
    available_models = [
        "claude_1", "claude_2", "claude_3", "claude_4",
        "dalle_1", "dalle_2", "dalle_3", "dalle_4",
        "gemini_1", "gemini_2", "gemini_3", "gemini_4",
        "gpto_1", "gpto_2", "gpto_3", "gpto_4",
        "stable_1", "stable_2", "stable_3", "stable_4",
        "midjourney_1", "midjourney_2", "midjourney_3", "midjourney_4"
    ]

    # Compile regex to extract IDs, model names, and numbers from filenames
    # New pattern: {id}_{model name}_{1, 2, 3, or 4}.{image type}
    filename_pattern = re.compile(r'^(\d+)_([^_]+)_([1-4])\.(png|jpeg|jpg|webp)$')

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
                model_base = match.group(2)
                number = match.group(3)
                # Combine model name and number to create the full model name
                model_name = f"{model_base}_{number}"
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
                model_base = match.group(2)
                number = match.group(3)
                # Combine model name and number to create the full model name
                model_name = f"{model_base}_{number}"
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

    # Scan participant_data folder for participant IDs
    participant_ids = []
    if participant_data_dir.exists():
        for folder in os.listdir(participant_data_dir):
            if folder.startswith("participant_"):
                participant_id = folder[12:]  # Extract the ID after "participant_"
                participant_ids.append(participant_id)
    else:
        print(f"Warning: Directory not found: {participant_data_dir}")

    # Only include the IDs that have all available models images
    new_image_data = {
        "aphantasia_images": {},
        "phantasia_images": {}
    }
    
    # Always use the available_models defined in this script
    config['available_models'] = available_models
    
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
    
    # Add participant IDs from participant_data folder - keep as strings
    config["participant_ids"] = sorted(participant_ids)

    # Write the updated config back to config.json
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    aphantasia_count = sum(len(paths) for paths in new_image_data['aphantasia_images'].values())
    phantasia_count = sum(len(paths) for paths in new_image_data['phantasia_images'].values())
    print(f"Available relative image paths written to {config_file}")
    print(f"Found {aphantasia_count} aphantasia images across {len(new_image_data['aphantasia_images'])} IDs")
    print(f"Found {phantasia_count} phantasia images across {len(new_image_data['phantasia_images'])} IDs")
    print(f"Added {len(participant_ids)} participant IDs from participant_data folder: {', '.join(participant_ids)}")

    return config

if __name__ == "__main__":
    scan_image_folders_and_update_config()