const { app, BrowserWindow } = require('electron');
const path = require('path');

require('electron-reload')(__dirname, {
  electron: require(`${__dirname}/../node_modules/electron`)
});

function clearCache() {
  const cachePath = path.join(app.getPath('userData'), 'Local Storage');

  try {
    if (fs.existsSync(cachePath)) {
      console.log(`Cache path found: ${cachePath}`);
      fs.readdirSync(cachePath).forEach((file) => {
        const filePath = path.join(cachePath, file);
        console.log(`Deleting file: ${filePath}`);
        fs.unlinkSync(filePath);
      });
      console.log('Cache cleared successfully');
    } else {
      console.log('Cache path does not exist');
    }
  } catch (error) {
    console.error('Error clearing cache:', error);
  }
}

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    webPreferences: {
      webSecurity: false, //remove this after development to avoid security issues
      nodeIntegration: true, // Enable Node integration
      contextIsolation: false, // Disable context isolation
      enableRemoteModule: false, // turn off remote

    },
    width: 800,
    height: 1280, //resolution of pi display
    //kiosk: true,
    //frame: false,
    //fullscreen: true, //Enable just this to show fullscreen without any other tab components
  });

  // Load the index.html of the app (pointing to your new homepage).
  mainWindow.loadFile('src/renderer/homepage/index.html');
 // mainWindow.setMenu(null); 
  // mainWindow.on('closed', function () {
  //   mainWindow = null;
  // });
}
app.commandLine.appendSwitch('enable-features', 'WebSpeechAPI');
process.env.GOOGLE_API_KEY = 'AIzaSyDEFZTqFNr512nWLs_l37oJEMQ3_qtEXTQ';

app.whenReady().then(() => {
  clearCache();
  createWindow();
});
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
  globalShortcut.register('F12', () => {
    mainWindow.webContents.toggleDevTools();
});
});

app.on('will-quit', () => {
  // Unregister all shortcuts.
  globalShortcut.unregisterAll();
});

