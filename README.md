# Ganzflicker-Study

## Input Data
### Directory Structure

For n participants and m past images:

- participant_data/
  - participant_001/
    - participant_001_claude.jpeg
    - participant_001_dalle.jpeg
    - participant_001_gpt.jpeg
    ...
  - participant_00n/
    - participant_00n_claude.jpeg
    - participant_00n_dalle.jpeg
    - participant_00n_gpt.jpeg
- past_images/
  - description_1/
    - description_1_claude.jpeg
    - description_1_dalle.jpeg
    - description_1_gpt.jpeg
  - description_2/
    - description_2_claude.jpeg
    - description_2_dalle.jpeg
    - description_2_gpt.jpeg
    ...
  - description_m/
    - description_m_claude.jpeg
    - description_m_dalle.jpeg
    - description_m_gpt.jpeg

### Past Descriptions
metadata.json includes a mapping of past description IDs to their description and imagery ability.
```
{
    "current_participant_data": [
        {
            "subject_id": "001",
            "description": "I saw some cool flowers and a face.",
            "results": [
                "random_low_imagery_description": "A glowing orb surrounded by geometric shapes.",
                "random_high_imagery_description": "A swirling vortex of vibrant colors blending into each other with people dancing around it.",
                "user_choices": [
                    "claude": {"choice": "low_imagery_description", "reaction_time": 0.5, "image_choice_location": "left"},
                    "dalle": {"choice": "own_description", "reaction_time": 0.7, "image_choice_location": "middle"},
                    "gpt": {"choice": "high_imagery_description", "reaction_time": 0.6, "image_choice_location": "right"},
                    "final_choice": {"model": "gpt", "reaction_time": 0.6, "description": "own_description"}
                ]
            ]
        },
        {
            "subject_id": "002",
            "description": "I saw some cool flowers and a face."
        }
    ],
    "past_hallucination_mappings": [
        {
            "description_id": "1",
            "description": "A swirling vortex of vibrant colors blending into each other with people dancing around it.",
            "imagery_ability": "high"
        },
        {
            "description_id": "2",
            "description": "A glowing orb surrounded by geometric shapes.",
            "imagery_ability": "low"
        },
        {
            "description_id": "3",
            "description": "A field of stars that seem to pulse and shift in a rhythmic pattern with hands from the sky.",
            "imagery_ability": "high"
        }
    ],
    "available_models": ["claude", "dalle", "gpt"]
}
```
## Steps
This study is produced using Javascript and jsPsych. Results are stored in metadata[current_participant_data][results]. The results for participant one are shown as an example.
```
Randomly choose two descriptions from hallucination_mappings.json, one with a high imagery ability and one with a low imagery ability.

For each available model:
    Display these 3 images side-by-side on the screen in a random order:
      1. Image from first chosen description with current model
      2. Image from second chosen description with current model
      3. Image from participant's description, generated from the current model
    
    User clicks one of the images to move on to the next model.

Display each image chosen by the participant. If there are n models available, there should be n images on the screen. The user then clicks one of these images as their final choice.
```