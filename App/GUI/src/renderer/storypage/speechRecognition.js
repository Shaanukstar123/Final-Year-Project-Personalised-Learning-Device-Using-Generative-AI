export class Microphone {
    constructor(stream, webSocket) {
        this.audioContext = new AudioContext();
        this.stream = stream;
        this.webSocket = webSocket;

        this.audioContext.audioWorklet.addModule('audio-processor.js').then(() => {
            console.log("Audio processor loaded");
            this.source = this.audioContext.createMediaStreamSource(stream);
            this.workletNode = new AudioWorkletNode(this.audioContext, 'audio-processor');
            console.log("Audio processor node created");
            this.workletNode.port.onmessage = (event) => {
                console.log("Received audio data:", event.data);
                // Assuming the event.data is the raw audio buffer
                const audioBuffer = event.data;
                const buffer = audioBuffer.buffer;  // Get the ArrayBuffer from the audio buffer
                if (this.webSocket && this.webSocket.readyState === WebSocket.OPEN) {
                    //console.log("Sending audio data:", buffer.byteLength);
                    this.webSocket.send(event.data);
                }
                else {
                    console.error("WebSocket is not open");
                }
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
        if (this.webSocket) {
            this.webSocket.close();
        }
    }
}
