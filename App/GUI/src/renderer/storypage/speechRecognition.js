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

        // this.audioContext.audioWorklet.addModule('audio-processor.js').then(() => {
        //     console.log("Audio processor loaded");
        //     this.source = this.audioContext.createMediaStreamSource(stream);
        //     this.workletNode = new AudioWorkletNode(this.audioContext, 'audio-processor');
        //     console.log("Audio processor node created");
        //     this.workletNode.port.onmessage = (event) => {
        //         if (this.webSocket && this.webSocket.readyState === WebSocket.OPEN) {
        //           const now = performance.now();
        //           if (now - this.lastSendTime > 500) {  // Send data every 300 ms instead
        //             this.webSocket.send(event.data);
        //             this.lastSendTime = now;
        //           }
        //         }
        //       };
              

        //     // Connect everything
        //     this.source.connect(this.workletNode);
        //     this.workletNode.connect(this.audioContext.destination);
        // });
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
