const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const spawn = require('child_process').spawn;

dotenv.config();

const app = express();
app.use(bodyParser.json());

mongoose.connect(process.env.ATLAS_URI || "", { useNewUrlParser: true, useUnifiedTopology: true });

const visitSchema = new mongoose.Schema({
    event: String,
    windowId: Number,
    tabId: Number,
    url: String,
    category: String,
    duration: Number,
    timestamp: Date
});

const Visit = mongoose.model('Visit', visitSchema);

function categorizeUrl(url, callback) {
    const process = spawn('python3', ['./categorize_url.py', url]);
    process.stdout.on('data', (data) => {
        callback(data.toString().trim());
    });
}

app.post('/track', (req, res) => {
    const { event, windowId, tabId, url, duration, timestamp } = req.body;
    categorizeUrl(url, (category) => {
        const newVisit = new Visit({
            event: event,
            windowId: windowId,
            tabId: tabId,
            url: url,
            category: category,
            duration: duration,
            timestamp: timestamp
        });
        newVisit.save()
            .then(() => res.json({ message: 'Success' }))
            .catch(err => res.status(400).json({ error: err }));
    });
});

app.get('/getStatistics', (req, res) => {
    Visit.aggregate([
        { $group: { _id: "$category", totalDuration: { $sum: "$duration" } } }
    ])
    .then(results => {
        const stats = {};
        results.forEach(result => {
            stats[result._id] = result.totalDuration;
        });
        res.json(stats);
    })
    .catch(err => res.status(400).json({ error: err }));
});

app.listen(process.env.PORT || '', () => console.log(`Server running on port ${process.env.PORT || ''}`));