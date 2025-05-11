import os
import re
import json
from pathlib import Path

def scan_image_folders_and_update_config():
    """
    Scans the aphantasia, phantasia, and participant_data image folders,
    and updates the config.json file with the available participant IDs and their relative image paths.
    Participant images are expected to be named participant_{id}_{model_name}.{ext}.
    Aphantasia/Phantasia images are expected as {id}_{model_base}_{number}.{ext}.
    Participant IDs are stored as strings.
    """
    base_dir = Path(__file__).resolve().parent # Use resolve() for more robust path
    images_dir_name = "images"
    participant_data_folder_name = "participant_data"
    aphantasia_folder_name = "aphantasia_images"
    phantasia_folder_name = "phantasia_images"

    aphantasia_dir = base_dir / images_dir_name / aphantasia_folder_name
    phantasia_dir = base_dir / images_dir_name / phantasia_folder_name
    participant_data_dir = base_dir / participant_data_folder_name
    config_file = base_dir / "config.json"

    # Define available models directly in the code
    # These are the "full" model names like "claude_1", "midjourney_4"
    available_models = [
        "claude_1", "claude_2", "claude_3", "claude_4",
        "dalle_1", "dalle_2", "dalle_3", "dalle_4",
        "gemini_1", "gemini_2", "gemini_3", "gemini_4",
        "gpto_1", "gpto_2", "gpto_3", "gpto_4",
        "stable_1", "stable_2", "stable_3", "stable_4",
        "midjourney_1", "midjourney_2", "midjourney_3", "midjourney_4"
    ]

    # Pattern for aphantasia/phantasia: {id}_{model_base}_{number}.{image_type}
    # Extracts: 1=id, 2=model_base (e.g., "claude"), 3=number (e.g., "1"), 4=extension
    aph_phan_filename_pattern = re.compile(r'^(\d+)_([a-zA-Z0-9]+)_([1-4])\.(png|jpeg|jpg|webp)$', re.IGNORECASE)

    # Initialize data structure
    image_paths_data = {
        "aphantasia_images": {},
        "phantasia_images": {},
        "participant_images": {} # Stores paths for each participant's models
    }

    # Scan aphantasia directory
    if aphantasia_dir.exists() and aphantasia_dir.is_dir():
        for filename in os.listdir(aphantasia_dir):
            match = aph_phan_filename_pattern.match(filename)
            if match:
                # Use string for participant_id_key to be consistent with participant_ids from folders
                participant_id_key = match.group(1) 
                model_base = match.group(2).lower() # Normalize model base name
                number = match.group(3)
                model_name = f"{model_base}_{number}" # Construct full model name
                
                # Ensure this constructed model_name is in our official available_models list
                if model_name not in available_models:
                    print(f"Warning (Aphantasia): Parsed model_name '{model_name}' from '{filename}' is not in available_models. Skipping.")
                    continue

                relative_path = f"{images_dir_name}/{aphantasia_folder_name}/{filename}"
                if participant_id_key not in image_paths_data["aphantasia_images"]:
                    image_paths_data["aphantasia_images"][participant_id_key] = {}
                image_paths_data["aphantasia_images"][participant_id_key][model_name] = relative_path
    else:
        print(f"Warning: Aphantasia directory not found or is not a directory: {aphantasia_dir}")

    # Scan phantasia directory
    if phantasia_dir.exists() and phantasia_dir.is_dir():
        for filename in os.listdir(phantasia_dir):
            match = aph_phan_filename_pattern.match(filename)
            if match:
                participant_id_key = match.group(1)
                model_base = match.group(2).lower()
                number = match.group(3)
                model_name = f"{model_base}_{number}"

                if model_name not in available_models:
                    print(f"Warning (Phantasia): Parsed model_name '{model_name}' from '{filename}' is not in available_models. Skipping.")
                    continue
                
                relative_path = f"{images_dir_name}/{phantasia_folder_name}/{filename}"
                if participant_id_key not in image_paths_data["phantasia_images"]:
                    image_paths_data["phantasia_images"][participant_id_key] = {}
                image_paths_data["phantasia_images"][participant_id_key][model_name] = relative_path
    else:
        print(f"Warning: Phantasia directory not found or is not a directory: {phantasia_dir}")

    # Scan participant_data directory for participant images
    # This will collect all participant IDs for whom a folder exists.
    # The JS part will later check if a *specific* participant has all their required images.
    raw_participant_ids_from_folders = []
    if participant_data_dir.exists() and participant_data_dir.is_dir():
        for folder_name in os.listdir(participant_data_dir):
            if folder_name.startswith("participant_"):
                participant_id_str = folder_name[12:] # Extract the ID (string)
                if not participant_id_str: # Skip if ID is empty
                    print(f"Warning: Found participant folder '{folder_name}' with no ID. Skipping.")
                    continue
                
                raw_participant_ids_from_folders.append(participant_id_str)
                
                participant_specific_folder_path = participant_data_dir / folder_name
                current_participant_model_paths = {}
                if participant_specific_folder_path.is_dir():
                    # For each available model, try to find a matching image file for this participant
                    for model_name_needed in available_models:
                        found_model_for_participant = False
                        # Expected filename: participant_{id_str}_{model_name_needed}.{ext}
                        # Example: participant_001_claude_1.png
                        expected_filename_prefix = f"participant_{participant_id_str}_{model_name_needed}."
                        
                        for item_in_folder in os.listdir(participant_specific_folder_path):
                            if item_in_folder.lower().startswith(expected_filename_prefix.lower()):
                                # Check extension
                                if item_in_folder.lower().endswith((".png", ".jpeg", ".jpg", ".webp")):
                                    relative_path = f"{participant_data_folder_name}/{folder_name}/{item_in_folder}"
                                    current_participant_model_paths[model_name_needed] = relative_path
                                    found_model_for_participant = True
                                    break # Found for this model_name_needed, move to next model_name_needed
                        
                        if not found_model_for_participant:
                            # If a specific model image is not found, we still create an entry for the participant,
                            # but this model_name_needed will be missing from their dict.
                            # The JS will handle the "missing image" error for the specific participant.
                            pass 
                
                if current_participant_model_paths: # Only add if we found at least one image or to register the participant
                     image_paths_data["participant_images"][participant_id_str] = current_participant_model_paths
                elif participant_id_str not in image_paths_data["participant_images"]: # Ensure participant is listed even if no images found yet
                     image_paths_data["participant_images"][participant_id_str] = {}


    else:
        print(f"Warning: Participant data directory not found or is not a directory: {participant_data_dir}")

    # Read existing config.json or create a new one
    config = {}
    if config_file.exists():
        with open(config_file, 'r') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode existing {config_file}. Creating a new one.")

    config['available_models'] = available_models # Always use the list from this script

    # Filter aphantasia/phantasia IDs: only include those with all available models
    filtered_aphantasia_images = {}
    for p_id_str, models_dict in image_paths_data["aphantasia_images"].items():
        if all(model_key in models_dict for model_key in available_models):
            filtered_aphantasia_images[p_id_str] = models_dict
        else:
            print(f"Info (Aphantasia): ID {p_id_str} does not have all {len(available_models)} model images. Excluding from aphantasia_ids.")
    
    filtered_phantasia_images = {}
    for p_id_str, models_dict in image_paths_data["phantasia_images"].items():
        if all(model_key in models_dict for model_key in available_models):
            filtered_phantasia_images[p_id_str] = models_dict
        else:
            print(f"Info (Phantasia): ID {p_id_str} does not have all {len(available_models)} model images. Excluding from phantasia_ids.")

    config["image_paths"] = {
        "aphantasia_images": filtered_aphantasia_images,
        "phantasia_images": filtered_phantasia_images,
        "participant_images": image_paths_data["participant_images"] # Store all found participant images/folders
    }

    # These IDs are for selection pools in the experiment
    config["aphantasia_ids"] = sorted(list(filtered_aphantasia_images.keys()))
    config["phantasia_ids"] = sorted(list(filtered_phantasia_images.keys()))
    
    # participant_ids lists all unique IDs for whom a participant_XYZ folder was found.
    # The JS will check if the *selected* participant from this list has all *their* necessary images.
    config["participant_ids"] = sorted(list(set(raw_participant_ids_from_folders)))


    # Write the updated config back to config.json
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    aphantasia_img_count = sum(len(paths_dict) for paths_dict in filtered_aphantasia_images.values())
    phantasia_img_count = sum(len(paths_dict) for paths_dict in filtered_phantasia_images.values())
    
    # Count total participant images collected.
    total_participant_images_collected = 0
    for p_id_str in image_paths_data["participant_images"]:
        total_participant_images_collected += len(image_paths_data["participant_images"][p_id_str])

    print(f"\n--- Configuration Summary ---")
    print(f"Config file updated: {config_file}")
    print(f"Total available_models defined: {len(available_models)}")
    
    print(f"\nAphantasia Images:")
    print(f"  - IDs with complete model sets: {len(config['aphantasia_ids'])}")
    print(f"  - Total images for these complete sets: {aphantasia_img_count}")
    
    print(f"\nPhantasia Images:")
    print(f"  - IDs with complete model sets: {len(config['phantasia_ids'])}")
    print(f"  - Total images for these complete sets: {phantasia_img_count}")

    print(f"\nParticipant Images & IDs:")
    print(f"  - Participant ID folders found: {len(config['participant_ids'])} ({', '.join(config['participant_ids']) if config['participant_ids'] else 'None'})")
    print(f"  - Total participant-specific images collected across all models and IDs: {total_participant_images_collected}")
    print(f"  (Note: Completeness for a *selected* participant's images is checked during the study.)")
    print(f"--- End of Summary ---\n")

    return config

if __name__ == "__main__":
    scan_image_folders_and_update_config()
