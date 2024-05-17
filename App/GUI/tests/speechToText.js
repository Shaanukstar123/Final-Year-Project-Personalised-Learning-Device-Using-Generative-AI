const vosk = require('vosk');
const { Readable } = require('stream');
const { spawn } = require('child_process');

// Load the model from the path where you've downloaded it
const modelPath = 'path/to/your/model';
vosk.setLogLevel(-1); // Turn off log output
const model = new vosk.Model(modelPath);

// Function to recognize from microphone
function recognizeFromMicrophone() {
    // Start recording from the microphone
    const process = spawn('arecord', ['-f', 'cd', '-t', 'wav', '-D', 'default']);

    const recognizer = new vosk.Recognizer({model: model, sampleRate: 16000});
    recognizer.setWords(true);

    const stream = new Readable().wrap(process.stdout);
    stream.on('data', (data) => {
        if (recognizer.acceptWaveform(data)) {
            console.log(recognizer.result());
        } else {
            console.log(recognizer.partialResult());
        }
    });

    stream.on('end', () => {
        console.log(recognizer.finalResult());
        recognizer.free();
    });

    process.on('exit', (code, signal) => {
        console.log('Process exited:', { code, signal });
        recognizer.free();
    });
}

// Call this function to start recognition
recognizeFromMicrophone();
