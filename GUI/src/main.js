const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    webPreferences: {
      webSecurity: false, //remove this after development to avoid security issues
    },
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // or remove if not using
      nodeIntegration: true
    }
  });

  // Load the index.html of the app (pointing to your new homepage).
  mainWindow.loadFile('src/renderer/homepage/index.html');
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
