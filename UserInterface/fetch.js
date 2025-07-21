const fetchBtn = document.getElementById('fetch-btn');
const usernameInput = document.getElementById('username');
const tweetOutput = document.getElementById('tweet-output');

window.addEventListener('DOMContentLoaded', () => {
  console.log('DOM fully loaded and parsed');

  window.electronAPI.onSuccess((data) => {
    console.log('Data received:', data);
    tweetOutput.innerHTML = `<strong>Fetched Data:</strong><br/><pre>${JSON.stringify(data, null, 2)}</pre>`;
    window.electronAPI.saveFile(data, 'social_media_data.json');
  });

  window.electronAPI.onError((error) => {
    console.error('Error fetching data:', error);
    tweetOutput.innerHTML = `<strong>Error:</strong> ${error}`;
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
});
