const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 550,
    height: 600,
    resizeable: false,
    maximizeable: false,
    frame: false,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"), // <- add this!
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  // Load Flask app in the Electron window
  mainWindow.loadURL('http://localhost:5000'); // Flask default port
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', () => {
  // Start the Flask app as a child process
  const flaskProcess = spawn('python', ['app.py'], {
    cwd: __dirname, // Directory of Flask app
  });

  flaskProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  flaskProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  flaskProcess.on('close', (code) => {
    console.log(`Flask app exited with code ${code}`);
  });

  // After Flask starts, create the Electron window
  setTimeout(createWindow, 2000); // Adjust delay if necessary
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }

const { ipcMain } = require('electron');

ipcMain.on("close-window", (event) => {
  const win = BrowserWindow.getFocusedWindow();
  if (win) win.close();
});

ipcMain.on("minimize-window", (event) => {
  const win = BrowserWindow.getFocusedWindow();
  if (win) win.minimize();
});

});
