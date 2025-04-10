const express = require('express');
const fs = require('fs').promises;
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');

const app = express();
const port = 3000;

// Updated file paths to save in the "results" folder
const RESULTS_FILE = path.join(__dirname, '../results/image_selection.json');
const IMAGE_DEBRIEF_FILE = path.join(__dirname, '../results/image_debrief.json');

app.use(cors());
app.use(bodyParser.json());

// Serve static files from the parent directory
app.use(express.static(path.join(__dirname, '..')));

// Function to ensure the "results" folder exists
async function ensureResultsFolder() {
    const resultsDir = path.join(__dirname, '../results');
    try {
        await fs.mkdir(resultsDir, { recursive: true });
        console.log(`Ensured "results" folder exists at ${resultsDir}`);
    } catch (error) {
        console.error(`Error ensuring "results" folder exists:`, error);
    }
}

// Function to read the results file
async function readResults(filePath) {
    try {
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.warn(`Error reading ${filePath} (it is probably just empty, so don't worry about this):`, error);
        return { "current_participant_data": {} }; // Return default if file not found or errors
    }
}

// Function to write to the results file
async function writeResults(filePath, data) {
    try {
        await fs.writeFile(filePath, JSON.stringify(data, null, 2), 'utf8');
        console.log(`${filePath} updated successfully.`);
    } catch (error) {
        console.error(`Error writing to ${filePath}:`, error);
    }
}

app.post('/save-participant-data', async (req, res) => {
    try {
        const { current_participant_data } = req.body;

        // Validate the request body
        if (!current_participant_data || typeof current_participant_data !== 'object') {
            console.error('Invalid request body: current_participant_data is missing or invalid.');
            return res.status(400).send('Invalid request body: current_participant_data is required.');
        }

        await ensureResultsFolder(); // Ensure the "results" folder exists

        const results = await readResults(RESULTS_FILE);

        // Merge the new data with existing data
        results.current_participant_data = {
            ...results.current_participant_data,
            ...current_participant_data
        };

        await writeResults(RESULTS_FILE, results);
        console.log('Participant data saved successfully.');
        res.status(200).send('Participant data saved successfully.');
    } catch (error) {
        console.error('Error in /save-participant-data:', error);
        res.status(500).send('Internal Server Error.');
    }
});

app.post('/save-likert-data', async (req, res) => {
    const likertData = req.body;

    if (!likertData || !likertData.current_participant_data) {
        return res.status(400).send('Invalid data format.');
    }

    await ensureResultsFolder(); // Ensure the "results" folder exists

    const existingData = await readResults(IMAGE_DEBRIEF_FILE); // Updated file path

    // Merge the new data with existing data
    existingData.current_participant_data = {
        ...existingData.current_participant_data,
        ...likertData.current_participant_data
    };

    await writeResults(IMAGE_DEBRIEF_FILE, existingData); // Updated file path
    res.status(200).send('Image debrief data saved successfully.');
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});