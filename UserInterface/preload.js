const { contextBridge, ipcRenderer } = require('electron');

//creates a bridge between the main process and renderer process
// This allows the renderer process to safely interact with the main process without exposing the entire Node.js API
// It provides a secure way to call functions in the main process and receive responses
contextBridge.exposeInMainWorld('electronAPI', {
  // Trigger the fetcher Python script
  fetchInstagramComments: (token, apiUrl) => {
    console.log('Sending fetcher request to main with token and API URL');
    ipcRenderer.send('run-fetcher', token, apiUrl); //sends a message to the main process to run the fetcher script
  },

  // Listen for success response from main process
  onSuccess: (callback) => {
    ipcRenderer.on('fetcher-success', (event, data) => { //listen for the 'fetcher-success' event from the main process
      console.log('Fetcher success coming from here :', data);

      callback(data);
    });
  },

  // Listen for error response from main process
  onError: (callback) => {
    ipcRenderer.on('fetcher-error', (event, error) => {
      console.error('Fetcher error:', error);
      callback(error);
    });
  },

  //might delete it later
  saveFile: (data, filename) => {
    ipcRenderer.send('save-file', data, filename);
  }
}),

contextBridge.exposeInMainWorld('api', {
    analyzeText: (text) => ipcRenderer.invoke('analyze-text', text),
})
