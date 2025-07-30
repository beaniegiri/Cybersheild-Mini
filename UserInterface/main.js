const { create } = require('domain');
const { app, BrowserWindow, Tray, Menu, ipcMain } = require('electron'); // Import necessary modules
const path = require('path'); // Node.js module for handling file and directory paths
const iconPath = path.join(__dirname, 'logo.png'); // Path to the application tray icon
const { spawn} = require('child_process'); // Required to execute external files
const fs = require('fs'); // Node.js module for file system operations

let mainWindow; // Variable to store the main application window
let tray=null; // Variable to store the tray object
let taskTimer = null; // Variable to track the background task timer


// Function to create the main application window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // Preload script for secure context
      contextIsolation: true, // Enable context isolation for security
      nodeIntegration: false, // Disable Node.js integration in renderer process
      enableRemoteModule: false, // Disable remote module for security
    },
    autoHideMenuBar: true, // Hide the menu bar
    });
  
  
    mainWindow.loadFile('index.html');
    mainWindow.webContents.openDevTools();
  
    mainWindow.on('closed', function () {
      mainWindow = null;
    });
  
  };
  

// Function to create the tray icon
  function createTray(){
    tray=new Tray(iconPath); 
    const contextMenu = Menu.buildFromTemplate([
      {
        label: 'Open Cybershield',
        click: () => {
          if (mainWindow) {
            mainWindow.show(); // Show the main window when the tray icon is clicked
          } else {
            createWindow(); // Create a new window if it doesn't exist
          }
        }
      },
      {
        label: 'Quit',
        click: () => {
          app.quit(); // Quit the application
        }
      }
    ]);
    tray.setToolTip('Cybershield is running in the background');
    tray.setContextMenu(contextMenu); // Set the context menu for the tray icon
    console.log('Tray icon created');
  }
  ipcMain.handle('analyze-text', async (event, text) => {
    const scriptPath = path.join(__dirname, '__init__copy.py'); // Path to the Python script
    return new Promise((resolve, reject) => {
      const process = spawn('python3', [scriptPath, '--text', text]); // Spawn a new Python process to run the script with the provided text
  
      let output = '';
      process.stdout.on('data', (data) => {
        console.log('Python Output:', data.toString()); // Log raw output
        output += data.toString();
      });
  
      process.stderr.on('data', (err) => {
        console.error('Python Error:', err.toString());
      });
  
      process.on('close', (code) => {
        console.log('Python process exited with code:', code);
        console.log('Raw Output:', output); // Log the raw output
        if (code === 0) {
          resolve(output); // Send the raw output to the renderer process
        } else {
          reject('Python script exited with code ' + code);
        }
      });
    });
  });
  // #Task to fetch data from a given API using a Python script
  // This task is triggered by the fetch button in the UI
  
  ipcMain.on('run-fetcher', (event, token, apiUrl) => {
    
    const pyProcess = spawn('python3', ['fetcher.py', token, apiUrl]);
    console.log('We are testing this Fetcher script started with token:', token, 'and API URL:', apiUrl);
  
    let result = '';
    let error = '';
  
    pyProcess.stdout.on('data', (data) => {
      result += data; //adding the data received from the Python script to the result variable
    });
  
    pyProcess.stderr.on('data', (data) => {
      console.error('Python error:', data.toString()); //adding any error data received from the Python script to the error variable
    });
  
    
    pyProcess.on('close', (code) => {
      if (code === 0) {
      
          event.reply('fetcher-success', result); // Send the parsed result back to the renderer process
          console.log('Fetcher script executed successfully:', result);
        }
        
      else {
          event.reply('fetcher-error', error || 'Unknown error occurred');
      // }
    };
  });
  });

  //saving data to a file
  ipcMain.on('save-file', (event, data, filename) => {
    const filePath = path.join(__dirname, filename);
    console.log('Saving to path:', filePath);

  try{
    const fixed = data.replace(/'/g, '"'); // Replace single quotes with double quotes for valid JSON format
    const parsedData = JSON.parse(fixed); // Parse the fixed data to ensure it's valid JSON
   
     // Read existing file (if any)
     let allData = [];
     if (fs.existsSync(filePath)) {
       const fileContents = fs.readFileSync(filePath, 'utf8');
       try {
         allData = JSON.parse(fileContents);
         if (!Array.isArray(allData)) allData = []; // Force array
       } catch (err) {
         console.warn('Existing file is invalid JSON. Starting fresh.');
       }
     }
 
     // Append new parsed data
     if (Array.isArray(parsedData)) {
       allData.push(...parsedData); // If data is an array of objects
     } else if (typeof parsedData === 'object') {
       allData.push(parsedData); // If single object
     } else {
       throw new Error('Parsed data must be an object or array of objects');
     }
 
     // Save back as valid JSON array
     fs.writeFile(filePath, JSON.stringify(allData, null, 2), 'utf8', (err) => {
       if (err) {
         console.error('Error saving file:', err);
         event.reply('save-file-error', 'Failed to save file');
       } else {
         console.log(`File saved successfully at ${filePath}`);
         event.reply('save-file-success', `File saved successfully at ${filePath}`);
       }
        // Call __init__.py 
        const pyProcess = spawn('python3', ['/home/binisa-giri/Downloads/Cybersheild/UserInterface/__init__.py']); // Userelative or absolute path

        pyProcess.stdout.on('data', (data) => {
          console.log('Python output:', data.toString());
        });

        pyProcess.stderr.on('data', (data) => {
          console.error('Python error:', data.toString());
        });

        pyProcess.on('close', (code) => {
          if (code === 0) {
            console.log('__init__.py ran successfully.');
          } else {
            console.error(`__init__.py exited with code ${code}`);
          }
        });
     });
 
   } catch (error) {
     console.error('Error parsing data:', error);
     event.reply('save-file-error', 'Failed to parse data');
   }
 });

  
// ---------- app lifecycle ----------
app.whenReady().then(() => {
  createWindow();
   createTray();

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });

app.on('before-quit', () => {
      tray.destroy(); // Clean up the tray icon before quitting
    });
  });



  