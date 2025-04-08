const express = require('express');
const fs = require('fs').promises;
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path'); // Import the 'path' module

const app = express();
const port = 3000;
const RESULTS_FILE = '../results.json';

app.use(cors());
app.use(bodyParser.json());

// Serve static files from the parent directory
app.use(express.static(path.join(__dirname, '..')));

// Function to read the results file
async function readResults() {
    try {
        const data = await fs.readFile(RESULTS_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('Error reading results.json:', error);
        return { "current_participant_data": [] }; // Return default if file not found or errors
    }
}

// Function to write to the results file
async function writeResults(data) {
    try {
        await fs.writeFile(RESULTS_FILE, JSON.stringify(data, null, 2), 'utf8');
        console.log('results.json updated successfully.');
    } catch (error) {
        console.error('Error writing to results.json:', error);
    }
}

app.post('/save-participant-data', async (req, res) => {
    const { subject_id, trials } = req.body;

    if (!subject_id || !Array.isArray(trials)) {
        return res.status(400).send('Subject ID and trials are required.');
    }

    const results = await readResults();

    // Initialize if not already an object
    if (typeof results.current_participant_data !== 'object' || Array.isArray(results.current_participant_data)) {
        results.current_participant_data = {};
    }

    // Save or overwrite trials under the subject ID
    results.current_participant_data[subject_id] = trials;

    await writeResults(results);
    res.status(200).send('Participant data saved successfully.');
});


app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});