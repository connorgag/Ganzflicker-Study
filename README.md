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

