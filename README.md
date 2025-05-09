# Ganzflicker-Study

## How to run this

### Installation

1.  **Install Node.js and npm:** Follow the instructions for your operating system on [https://nodejs.org/](https://nodejs.org/) (it's recommended to download the LTS version). Verify installation with `node -v` and `npm -v` in your terminal.

2.  **Navigate to the server directory:**
    ```bash
    cd server
    ```

3.  **Install server dependencies:**
    ```bash
    npm install
    ```
    (or `yarn install` if you use Yarn)

### Running the Server

In the **server** directory, run:

```bash
npm start
```

And click on the link that pops up (should be http://localhost:3000).

## Directions
This study is produced using Javascript and jsPsych. 

### General format
The user goes through a series of screens and must select an image in order to click next to advance to the next screen. Some screens have questions; the user must fill out all questions on the screen to continue. If they try to advance the screen without clicking an image or answering a question, text will appear that reminds them what they need to do in order to advance. There are no back buttons.

The image IDs are the names of the images, which includes information about the participant id and the model (e.g. 234_midjourney_2.jpeg will be stored in the results as 234_midjourney_2, which is a unique name). These image  are used to track the images throughout the study and that are recorded

Whenever there are multiple images on a screen, their order is randomized. They are arranged so that the group of images fill up the entire screen. Where are are 3 images, there is 1 row of 3. When there are 8 images, there are 2 rows of 4. The user does not have to scroll to see all of the images or to find the 'next' button.

Everything is centered both horizontally and vertically on each screen.

### Results storage
The results data is stored in two files:
- image_debrief.json: stores likert scale and other question responses from the user. Each participants data is nested under their participant id.
- image_selection.json: stores information related to the images selected by the user during the study. Each image selection is stored as an individual record with the participant's id as a column.

For each of these files, the columns in each entry should be the same. We do this because it is easier to programmatically parse later. However, this means that some columns are not relevant when saving data from some screens. In this case, we put "na" for the value.

The 'accuracy' field in image_selection indicates whether the participant clicked on an image that was generated using their own description. In other words, if choice = "own", then accuracy is 1, else it is 0.


### How this study works:

By default there are 6 models and 4 images for each model. So for the purposes of this study, there are 24 'models' (claude_1, claude_2, claude_3, claude_4, gpto_1, etc.).

**Before the html is rendered, collect_ids.py is run to collect the participant ids and image paths and puts them in config.json.**


#### Screen 1
This screen is where the user inputs the participant ID. 


#### Screen 2
Welcome screen (e.g. Welcome to the Ganzflicker Study)


#### First Round
24 normal screens with 48 distractors (2 distractors per model)

It first selects 3 people: low distractor (aphantasia), our participant, and a high distractor (phantasia).
Then, for each screen (24 screens, 1 for each model), it displays 3 images: the low distractor image, the high distractor image, and the participant image. These are all taken from the same model (midjourney_3 for instance). The text displayed above the images is "Click on the image that best represents what you "saw" during the ganzflicker experience."


This data is stored in image_selection.json


#### Second Round
At this point, we have 24 images from the 24 screens that the person saw. The participant clicked one image on each of these 24 screens. For this second round, we will have 3 screens. The 24 images that were clicked should be randomly ordered and randomly split up into 3 groups of 8. At this point, it does not matter if the image is from aphantasia, phantasia, or the participant; the images are randomly scrambled and split up into groups for each screen. These should be put on 3 screens with 8 images on each and the user is prompted to select the image that matched their hallucination (using the same prompt as the first round on each screen). The 8 images on each screen are in 2 rows of 4.

The text above the images on each screen is "From the images you chose on previous screens, select the one that is the best visualization of what you "saw" during the Ganzflicker."


This data should be stored in image_selection.json using the same columns as round one. Here is an example:

        "subject_id": "001",
        "trial_type": "second_round_screen_1",
        "model": "na",
        "aphantasia_image": "na",
        "phantasia_image": "na",
        "target": "na",
        "choice": "aphantasia",
        "reaction_time": 199.47,
        "image_choice_location": "row2_col3",
        "accuracy": 0,
        "chosen_model": "stable_2",
        "chosen_image": "1978_stable_2",
        "datetime": "2025-05-07T22:49:06.759Z"

This is the same schema as round one, so many columns will always be na because they are not applicable. We still keep track of whether their choice was an aphantasia image, phantasia image, or their own image. 

There should be three trial_types, one for each screen in this round:
second_round_screen_1
second_round_screen_2
second_round_screen_3

Also, image_choice_location is different for this round because there are 8 images on each screen instead of 3. So we must be more descriptive because there are 2 rows of 4 images. 


#### Third Round
This round consists of 3 screens. The 3 images chosen in round two are randomly ordered and each image is placed on it's own screen. Each screen has one picture and the likert scales and open-ended question below it. The text above the image on each of these screens should read "Below is one of the images you selected as the best visualization of your Ganzflicker experience. Please rate how much this image resembles your hallucinations in terms of the following dimensions:" It is okay for the user to scroll down the pages to see all of the questions.

This data is stored in image_debrief.json in the following format:

    "001": {
      "subject_id": "001",
      "final_image_1": "1978_stable_2",
      "color_1": "3",
      "shape_1": "2",
      "content_1": "2",
      "overall_1": "2",
      "detailed_feedback_1": "This image was really similar to what I saw because I saw really cool images of butterflies and it was better than drugs."

      "final_image_2": "1978_claude_2",
      "color_2": "3",
      "shape_2": "3",
      "content_2": "2",
      "overall_2": "3",
      "detailed_feedback_2": "This image matched the colors really well"

      "final_image_3": "1978_gpto_4",
      "color_3": "10",
      "shape_3": "6",
      "content_3": "5",
      "overall_3": "1",
      "detailed_feedback_3": "This one had such a similar vibe to what I experienced"
    }


#### Fourth Round
This round is the final image selection. The three images from round three are displayed in a random order on the screen and the user chooses from these. The text above the image should read "From the images you chose earlier, please select the image that is the best visualization of what you "saw" during the Ganzflicker."

This data is stored in image_selection.json in the following format:

      {
        "subject_id": "001",
        "trial_type": "fourth_round",
        "model": "na",
        "aphantasia_image": "na",
        "phantasia_image": "na",
        "target": "na",
        "choice": "phantasia",
        "reaction_time": 199.47,
        "image_choice_location": "right",
        "accuracy": 0,
        "chosen_model": "claude_3",
        "chosen_image": "1978_claude_3",
        "datetime": "2025-05-07T22:49:06.759Z"
      }


#### Final Screen
After these rounds, the study is complete and the user will see a screen that says:

  
  "Study Completed
  Thank you for participating in this study!

  Your data has been saved successfully."
  

This changes if the data does not save successfully. If this happens the user is told this and prompted to manually download their data.
