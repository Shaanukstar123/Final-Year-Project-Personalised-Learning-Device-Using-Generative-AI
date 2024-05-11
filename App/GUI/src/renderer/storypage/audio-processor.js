const MAX_16BIT_INT = 32767;
class AudioProcessor extends AudioWorkletProcessor {
  process(inputs) {
    const input = inputs[0];
    const output = inputs[0]; // if you wish to loop back audio to output
    if (!input) return true;
    const inputChannel = input[0];

    if (inputChannel) {
      // Convert Float32Array to Int16Array
      const int16Array = new Int16Array(inputChannel.length);
      for (let i = 0; i < inputChannel.length; i++) {
        int16Array[i] = Math.min(1, inputChannel[i]) * 32767;
      }
      // Post the buffer to the main thread
      this.port.postMessage(int16Array.buffer);
    }
    return true;
  }
}
registerProcessor('audio-processor', AudioProcessor);