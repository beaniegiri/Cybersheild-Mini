// welcome.js
//alert("This app will run in the background. You can close this window.");
//let task= prompt("This app will run in the background. You can close this window. Do you want to continue? (yes/no)", "yes");
//console.log("User response:", task);
// const{ipcRenderer} = require('electron');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const video = document.querySelector('video');
const fetchBtn = document.getElementById('fetch-btn');
const usernameInput = document.getElementById('username');
const tweetOutput = document.getElementById('tweet-output');



let isTaskRunning = true; // Track task state

document.getElementById('analyzeBtn').addEventListener('click', analyzeText);
document.getElementById('clearBtn').addEventListener('click', clearText);


function analyzeText() {
    const text = document.getElementById('inputText').value;
    if (!text.trim()) {
        alert('Please enter some text to analyze');
        return;
    }
    
    // In a real app, need to send this to your backend for analysis
    // This is just a placeholder for the UI
    document.getElementById('results').innerHTML = `
        <strong>Analysis Complete:</strong><br/><br/>
        <strong>Sentiment:</strong> Positive<br/>
        <strong>Toxicity Score:</strong> 12%<br/>
        <strong>Abusive Language Detected:</strong> No<br/>
        <strong>Key Phrases:</strong> "great experience", "highly recommend"<br/><br/>
        <em>Note: This is a demo. Real analysis would use DistilBERT or similar model.</em>
    `;
}

function clearText() {
    document.getElementById('inputText').value = '';
    document.getElementById('results').innerHTML = 
        'No analysis results yet<br/>Enter text and click analyze to begin';
}

window.addEventListener('DOMContentLoaded', () => {
  console.log('DOM fully loaded and parsed');

    window.electronAPI.onSuccess((data) => {
      console.log('Data received:', data);
      tweetOutput.innerHTML = `<strong>Fetched Data:</strong><br/><pre>${JSON.stringify(data, null, 2)}</pre>`;
      
      //save the data
      window.electronAPI.saveFile(data, 'social_media_data.json');
    });

    window.electronAPI.onError((error) => { 
      console.error('Error fetching data:', error);
      tweetOutput.innerHTML = `<strong>Error:</strong> ${error}`;
    });
  });
  fetchBtn.addEventListener('click', () => {
    const token = document.getElementById('token').value.trim();
    const apiUrl = document.getElementById('apiUrl').value.trim();

    if (!token || !apiUrl) {
      alert("Please enter both Access Token and API URL.");
      return;
    }

    alert("Fetching data... Please wait.");
    console.log('Fetch button clicked with:', token, apiUrl);

    window.electronAPI.fetchInstagramComments(token, apiUrl);
  });



// Your existing analyzeText() and clearText() functions
document.getElementById('analyzeBtn').addEventListener('click', analyzeText);
document.getElementById('clearBtn').addEventListener('click', clearText);

function analyzeText() {
  const text = document.getElementById('inputText').value;
  if (!text.trim()) {
    alert('Please enter some text to analyze');
    return;
  }

  document.getElementById('results').innerHTML = `
      <strong>Analysis Complete:</strong><br/><br/>
      <strong>Sentiment:</strong> Positive<br/>
      <strong>Toxicity Score:</strong> 12%<br/>
      <strong>Abusive Language Detected:</strong> No<br/>
      <strong>Key Phrases:</strong> "great experience", "highly recommend"<br/><br/>
      <em>Note: This is a demo. Real analysis would use DistilBERT or similar model.</em>
  `;
}

function clearText() {
  document.getElementById('inputText').value = '';
  document.getElementById('results').innerHTML =
    'No analysis results yet<br/>Enter text and click analyze to begin';
}

 