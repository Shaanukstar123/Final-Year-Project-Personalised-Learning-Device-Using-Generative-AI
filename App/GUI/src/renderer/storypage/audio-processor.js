class AudioProcessor extends AudioWorkletProcessor {
  constructor() {
      super();
      this.sampleRate = 16000; // Make sure this matches the context sample rate
      this.frameSize = 512; // Number of samples per frame
      this.buffer = new Int16Array(this.frameSize);
      this.index = 0;
  }

  process(inputs) {
      const input = inputs[0][0]; // Assuming mono input
      if (input) {
          for (let i = 0; i < input.length; i++) {
              // Convert float32 audio data to int16
              this.buffer[this.index++] = Math.max(-1, Math.min(1, input[i])) * 32767;
              if (this.index >= this.buffer.length) {
                  // Send the buffer via port
                  this.port.postMessage(this.buffer.buffer);
                  this.index = 0; // Reset the index
              }
          }
      }
      return true;
  }
}

registerProcessor('audio-processor', AudioProcessor);
