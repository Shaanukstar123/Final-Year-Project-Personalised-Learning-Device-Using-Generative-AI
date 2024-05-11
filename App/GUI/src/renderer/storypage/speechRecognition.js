export class Microphone {
    constructor(stream) {
        this.audioContext = new AudioContext();
        this.stream = stream;

        // Add the module to the Audio Context
        this.audioContext.audioWorklet.addModule('audio-processor.js').then(() => {
            this.source = this.audioContext.createMediaStreamSource(stream);
            this.workletNode = new AudioWorkletNode(this.audioContext, 'audio-processor');

            this.workletNode.port.onmessage = (event) => {
                // Handle the audio data received from the processor
                console.log(event.data);  // Or send this data through WebSocket
            };

            // Connect everything
            this.source.connect(this.workletNode);
            this.workletNode.connect(this.audioContext.destination);
        });
    }

    stop() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
        if (this.audioContext) {
            this.audioContext.close();
        }
    }
}
