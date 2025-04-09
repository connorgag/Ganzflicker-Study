const express = require('express');
const fs = require('fs').promises;
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');

const app = express();
const port = 3000;

// Updated file paths to save in the "results" folder
const RESULTS_FILE = path.join(__dirname, '../results/image_selection.json');
const LIKERT_RESPONSES_FILE = path.join(__dirname, '../results/likert_responses.json');

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
    const { subject_id, trials } = req.body;

    if (!subject_id || !Array.isArray(trials)) {
        return res.status(400).send('Subject ID and trials are required.');
    }

    await ensureResultsFolder(); // Ensure the "results" folder exists

    const results = await readResults(RESULTS_FILE);

    // Initialize if not already an object
    if (typeof results.current_participant_data !== 'object' || Array.isArray(results.current_participant_data)) {
        results.current_participant_data = {};
    }

    // Save or overwrite trials under the subject ID
    results.current_participant_data[subject_id] = trials;

    await writeResults(RESULTS_FILE, results);
    res.status(200).send('Participant data saved successfully.');
});

app.post('/save-likert-data', async (req, res) => {
    const likertData = req.body;

    if (!likertData || !likertData.current_participant_data) {
        return res.status(400).send('Invalid data format.');
    }

    await ensureResultsFolder(); // Ensure the "results" folder exists

    const existingData = await readResults(LIKERT_RESPONSES_FILE);

    // Merge the new data with existing data
    existingData.current_participant_data = {
        ...existingData.current_participant_data,
        ...likertData.current_participant_data
    };

    await writeResults(LIKERT_RESPONSES_FILE, existingData);
    res.status(200).send('Likert data saved successfully.');
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});