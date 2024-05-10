// Define the Microphone class to encapsulate all related operations
class Microphone {
  constructor() {
      this.stream = null;
      this.audioContext = null;
      this.audioWorkletNode = null;
      this.source = null;
      this.audioBufferQueue = new Int16Array(0);
  }

  async requestPermission() {
      this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  }

  async startRecording(onAudioCallback) {
      if (!this.stream) await this.requestPermission();
      this.audioContext = new AudioContext({
          sampleRate: 16000,
          latencyHint: 'balanced'
      });
      this.source = this.audioContext.createMediaStreamSource(this.stream);

      await this.audioContext.audioWorklet.addModule('audio-processor.js');
      this.audioWorkletNode = new AudioWorkletNode(this.audioContext, 'audio-processor');

      this.source.connect(this.audioWorkletNode);
      this.audioWorkletNode.connect(this.audioContext.destination);
      this.audioWorkletNode.port.onmessage = (event) => {
          const currentBuffer = new Int16Array(event.data.audio_data);
          this.audioBufferQueue = this.mergeBuffers(this.audioBufferQueue, currentBuffer);

          const bufferDuration = (this.audioBufferQueue.length / this.audioContext.sampleRate) * 1000;

          if (bufferDuration >= 100) {
              const totalSamples = Math.floor(this.audioContext.sampleRate * 0.1);
              const finalBuffer = new Uint8Array(this.audioBufferQueue.subarray(0, totalSamples).buffer);
              this.audioBufferQueue = this.audioBufferQueue.subarray(totalSamples);
              if (onAudioCallback) onAudioCallback(finalBuffer);
          }
      };
  }

  stopRecording() {
      if (this.stream) {
          this.stream.getTracks().forEach(track => track.stop());
      }
      if (this.audioContext) {
          this.audioContext.close();
      }
      this.audioBufferQueue = new Int16Array(0);
  }

  mergeBuffers(lhs, rhs) {
      const mergedBuffer = new Int16Array(lhs.length + rhs.length);
      mergedBuffer.set(lhs, 0);
      mergedBuffer.set(rhs, lhs.length);
      return mergedBuffer;
  }
}

// Export the Microphone class
export { Microphone };
