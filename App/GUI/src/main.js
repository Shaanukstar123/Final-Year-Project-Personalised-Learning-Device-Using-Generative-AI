const { Console } = require('console');
const { app, BrowserWindow, globalShortcut, ipcMain } = require('electron');
const VirtualKeyboard = require('electron-virtual-keyboard');
const path = require('path');

let isCacheCleared = false;
let mainWindow; // Declare mainWindow globally to use it in the globalShortcut registration

require('electron-reload')(__dirname, {
  electron: require(`${__dirname}/../node_modules/electron`)
});

function createWindow() {
  const clearLocalStorage = `
    localStorage.clear();
    console.log('LocalStorage cleared successfully');
  `;

  mainWindow = new BrowserWindow({
    webPreferences: {
      webSecurity: false, // remove this after development to avoid security issues
      nodeIntegration: true, // Enable Node integration
      contextIsolation: false, // Disable context isolation
      enableRemoteModule: false, // turn off remote
      enableTouchEmulation: true, // Ensure touch events are enabled
    },
    width: 800,
    height: 1280, // resolution of pi display
    // kiosk: true,
    // frame: false,
    // fullscreen: true, // Enable just this to show fullscreen without any other tab components
  });

  // Load the index.html of the app (pointing to your new homepage).
  mainWindow.loadFile('src/renderer/homepage/index.html');

  // Waits for the reload signal from refresh button and reloads the window
  ipcMain.on('reload-window', () => {
    console.log('Reloading window');
    mainWindow.reload();
  });

  // Initialize the virtual keyboard
  const vkb = new VirtualKeyboard(mainWindow.webContents);

  // LOCAL STORAGE:
  mainWindow.webContents.on('did-finish-load', () => {
    if (!isCacheCleared) {
      mainWindow.webContents.executeJavaScript(clearLocalStorage)
        .then(() => {
          isCacheCleared = true;
        })
        .catch(error => console.error('Error clearing LocalStorage:', error));
    } else {
      console.log('LocalStorage not cleared, already cleared this session');
    }
  });

  ipcMain.on('toggle-fullscreen', () => {
    const isFullScreen = mainWindow.isFullScreen();
    mainWindow.setFullScreen(!isFullScreen);
  });

  // mainWindow.setMenu(null);
  // mainWindow.on('closed', function () {
  //   mainWindow = null;
  // });
}

app.commandLine.appendSwitch('enable-features', 'WebSpeechAPI');
process.env.GOOGLE_API_KEY = 'AIzaSyDEFZTqFNr512nWLs_l37oJEMQ3_qtEXTQ';

app.whenReady().then(() => {
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

app.on('will-quit', () => {
  // Unregister all shortcuts.
  globalShortcut.unregisterAll();
});
