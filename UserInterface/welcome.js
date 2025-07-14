// welcome.js
//alert("This app will run in the background. You can close this window.");
//let task= prompt("This app will run in the background. You can close this window. Do you want to continue? (yes/no)", "yes");
//console.log("User response:", task);
// const{ipcRenderer} = require('electron');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const video = document.querySelector('video');
const fetchButton = document.getElementById('fetch-btn');
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
  const fetchBtn = document.getElementById('fetchBtn');

  fetchBtn.addEventListener('click', () => {
    const token = document.getElementById('token').value.trim();
    const apiUrl = document.getElementById('apiUrl').value.trim();

    if (!token || !apiUrl) {
      alert("Please enter both Access Token and API URL.");
      return;
    }
    alert("Fetching data... Please wait.");

    console.log('Fetch button clicked with:', token, apiUrl);
    window.electronAPI.fetchInstagramComments(token, apiUrl); // Trigger the fetcher
  });

  //  When fetch is successful
  window.electronAPI.onSuccess((data) => {
    console.log('Data received:', data);

    // Display the data in the UI
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
      <strong>Fetched Data:</strong><br/><br/>
      <pre>${JSON.stringify(data, null, 2)}</pre>
    `;

    // Save the data as a JSON file
    // saveDataAsFile(data, 'social_media_data.json');\
    //Using pr.js save function
    window.electronAPI.saveFile(data, 'social_media_data.json');

  });

  // When fetch fails
  window.electronAPI.onError((error) => {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<strong>Error:</strong> ${error}`;
  });
});

// Function to save data as a JSON file
// function saveDataAsFile(data, filename) {
//   const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
//   const url = URL.createObjectURL(blob);

//   // Create a temporary anchor element to trigger the download
//   const a = document.createElement('a');
//   a.href = url;
//   a.download = filename;
//   document.body.appendChild(a);
//   a.click();

//   // Clean up the temporary anchor element
//   document.body.removeChild(a);
//   URL.revokeObjectURL(url);
// }

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

 