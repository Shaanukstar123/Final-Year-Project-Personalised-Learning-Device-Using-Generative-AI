export class Microphone {
    constructor(stream, webSocket) {
        this.audioContext = new AudioContext();
        this.stream = stream;
        this.webSocket = webSocket;
        this.lastSendTime = performance.now();

        this.audioContext.audioWorklet.addModule('audio-processor.js').then(() => {
            this.source = this.audioContext.createMediaStreamSource(stream);
            let node = new AudioWorkletNode(this.audioContext, 'audio-processor');
            node.port.onmessage = (event) => {
                // Handle the Int16Array buffer here
                if (webSocket.readyState === WebSocket.OPEN) {
                    const now = performance.now();
                    if (now - this.lastSendTime > 300) { 
                    webSocket.send(new Uint8Array(event.data));
                    this.lastSendTime = now;
                    }
                }
            };
            this.source.connect(node);
            node.connect(this.audioContext.destination); // This connection is not always necessary
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
