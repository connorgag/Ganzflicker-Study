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
    const participantData = req.body;

    if (!participantData.subject_id || !participantData.results) {
        return res.status(400).send('Participant ID and results are required.');
    }

    const results = await readResults();
    const existingParticipantIndex = results.current_participant_data.findIndex(p => p.subject_id === participantData.subject_id);

    if (existingParticipantIndex !== -1) {
        // Update existing participant's data
        results.current_participant_data[existingParticipantIndex] = participantData;
    } else {
        // Add new participant's data
        results.current_participant_data.push(participantData);
    }

    await writeResults(results);
    res.status(200).send('Participant data saved successfully.');
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});