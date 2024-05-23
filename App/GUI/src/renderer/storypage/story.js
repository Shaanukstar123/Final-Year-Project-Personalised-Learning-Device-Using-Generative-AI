//import assemblyai library:
const assemblyai = require('assemblyai');
const pages = [];
let currentPageIndex = 0;
let incompleteWord = '';
let accumulatedStory = '';
let ws = null;  // WebSocket instance
const buttonEl = document.getElementById("speak");
const messageEl = document.getElementById("textarea");
const titleEl = document.getElementById("titlearea");
messageEl.style.display = "none";
let isRecording = false;
let rt;
let microphone = null;

document.addEventListener('DOMContentLoaded', () => {
    const storyContainer = document.getElementById('story-container');
    storyContainer.style.fontFamily = 'Comic Sans MS';
    const params = new URLSearchParams(window.location.search);
    const topicId = params.get('topicId');
    const buttonEl = document.getElementById("speak"); // ID corrected for the speak button
    const messageEl = document.getElementById("textarea"); // ID corrected for the message display area
    let isRecording = false;
    buttonEl.addEventListener("click", () => run());

    if (topicId) {
        axios.get(`http://localhost:5000/fetch_story/${topicId}`)
            .then(response => {
                const storyContent = response.data.story; // Adjust according to your response structure
                const storyContainer = document.getElementById('story-container');
                displayContentWithAnimation(storyContainer, storyContent); // Update displayContentWithAnimation to handle the received data
            })
            .catch(error => {
                console.error('Error fetching story:', error);
            });
    }
    
    const homeButton = document.getElementById('homeButton');
    if (homeButton) {
        homeButton.addEventListener('click', function() {
            window.location.href = '../homepage/index.html'; // Adjust the path as needed
        });
    }

    const nextPageButton = document.getElementById('next-page-button');
    if (nextPageButton) {
        nextPageButton.addEventListener('click', fetchNextPage);
    }
    initialiseSwipeDetection(storyContainer);
});

// Existing functions from story.js here...

function updateImage(storyContent) {
    // Check if the story content contains a "DALL-E prompt:"
    const promptRegex = /dall-e prompt:/i; // 'i' flag for case-insensitive matching
    const promptMatch = storyContent.match(promptRegex);

    if (promptMatch) {
        // Extract the content after the prompt for image generation
        const promptIndex = promptMatch.index + promptMatch[0].length;
        const imageDescription = storyContent.substring(promptIndex).trim();

        // Only proceed with the API call if there's a valid description
        if (imageDescription.length > 0) {
            axios.post('http://localhost:5000/get_image', { text: imageDescription })
                .then(response => {
                    const { image_url } = response.data;
                    pages[currentPageIndex].imageUrl = image_url; // Update current page with the new image URL
                    displayImage(document.getElementById('story-container'), image_url);
                })
                .catch(error => console.error('Error fetching image:', error));
        }
    }
}


let cumulativeDelay = 0;
const wordDisplayInterval = 100; // Interval between words appearing, in milliseconds

function displayContentWithAnimation(container, content) {
    // Clear the container first
    container.innerHTML = '';

    const words = content.split(/\s+/);
    cumulativeDelay = 0;  // Reset the delay for word animation

    words.forEach(word => {
        if (word.length > 0) {
            const span = document.createElement('span');
            span.textContent = word + ' ';
            span.style.opacity = 0; // Start invisible
            span.style.transition = 'opacity 1s ease-in-out';
            container.appendChild(span);

            setTimeout(() => {
                span.style.opacity = 1; // Fade in the word
            }, cumulativeDelay);

            cumulativeDelay += wordDisplayInterval; // Increment delay for the next word
        }
    });
}


function displayImage(container, imageUrl) {
    const imgElement = document.createElement('img');
    imgElement.src = imageUrl;
    imgElement.style.width = '100%';
    imgElement.style.height = 'auto';
    imgElement.style.marginTop = '20px';
    container.appendChild(imgElement);
}

function addPage(content, imageUrl) {
    pages.push({ content, imageUrl, audioUrl: '' });
    currentPageIndex = pages.length - 1;
    fetchAudioForPage(content).then(audioUrl => {
        pages[currentPageIndex].audioUrl = audioUrl;
        if (currentPageIndex === pages.length - 1) {
            playAudio(audioUrl);
            updateAudioButtonVisibility();
        }
    });
    displayPage(currentPageIndex);
}

function displayPage(index) {
    const storyContainer = document.getElementById('story-container');
    storyContainer.innerHTML = ''; // Clear previous content

    if (index >= 0 && index < pages.length) {
        const { content, imageUrl, audioUrl } = pages[index];
        displayContentWithAnimation(storyContainer, content);
        if (imageUrl) {
            displayImage(storyContainer, imageUrl);
        }
        if (audioUrl) {
            playAudio(audioUrl);
        }
    }
}

function fetchNextPage() {
    console.log('Fetching next page of the story');

    const userInput = userTranscription; // Use the transcribed text
    console.log('User input:', userInput);

    axios.get(`http://localhost:5000/continue_story`, {
        params: {
            user_input: userInput
        }
    })
    .then(response => {
        const storyContent = response.data.story; // Adjust according to your response structure
        const storyContainer = document.getElementById('story-container');
        displayContentWithAnimation(storyContainer, storyContent); // Update displayContentWithAnimation to handle the received data
    })
    .catch(error => {
        console.error('Error fetching next page:', error);
    });

    // Clear current content to display new page content
    const storyContainer = document.getElementById('story-container');
    storyContainer.innerHTML = '';
    cumulativeDelay = 0;  // Reset the delay for word animation
}


function initialiseSwipeDetection(element) {
    if (!element) return;

    const hammer = new Hammer(element);
    hammer.get('swipe').set({ direction: Hammer.DIRECTION_HORIZONTAL });

    hammer.on('swipeleft', function(ev) {
        console.log('Swiped left');
        ev.preventDefault();  // Prevent the default scroll behavior
        goToNextPage();
    });

    hammer.on('swiperight', function(ev) {
        console.log('Swiped right');
        ev.preventDefault();  // Prevent the default scroll behavior
        goToPreviousPage();
    });

    // Optionally, prevent touch scrolling on this element
    element.addEventListener('touchmove', function(e) {
        e.preventDefault();
    }, { passive: false });
}


function goToNextPage() {
    if (currentPageIndex < pages.length - 1) {
        currentPageIndex++;
        displayPage(currentPageIndex);
    } else {
        // If at the last page, fetch next page
        fetchNextPage();
    }
}

function goToPreviousPage() {
    if (currentPageIndex > 0) {
        currentPageIndex--;
        displayPage(currentPageIndex);
    } else {
        currentPageIndex = 0;
    }
}

function fetchAudioForPage(text) {
    return new Promise((resolve, reject) => {
        // Assuming this endpoint returns a direct link to the audio file
        const apiUrl = 'http://localhost:5000/text-to-speech';
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.blob();
        })
        .then(blob => {
            const audioUrl = URL.createObjectURL(blob);
            resolve(audioUrl);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            reject(error);
        });
    });
}


function playAudio(audioUrl) {
    const audioPlayer = document.getElementById('audioPlayer'); // Ensure this element exists in your HTML
    audioPlayer.src = audioUrl;
    audioPlayer.play();
}

function updateAudioButtonVisibility() {
    const audioButton = document.getElementById('play-audio-button');
    const audioPlayer = document.getElementById('audioPlayer');
    if (audioPlayer.src) {
        audioButton.style.display = 'block'; // Show the button if there's audio
    } else {
        audioButton.style.display = 'none'; // Hide the button if there's no audio
    }
}

function toggleAudioPlayback() {
    const audioPlayer = document.getElementById('audioPlayer');
    if (audioPlayer.src) {
        if (audioPlayer.paused) {
            audioPlayer.play();
        } else {
            audioPlayer.pause();
        }
    } else {
        console.log('No audio loaded');
    }
}
document.getElementById('play-audio-button').addEventListener('click', toggleAudioPlayback);

// Speech to Text


// set initial state of application variables


function createMicrophone() {
  let stream;
  let audioContext;
  let audioWorkletNode;
  let source;
  let audioBufferQueue = new Int16Array(0);
  return {
    async requestPermission() {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    },
    async startRecording(onAudioCallback) {
      if (!stream) stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioContext = new AudioContext({
        sampleRate: 16_000,
        latencyHint: 'balanced'
      });
      source = audioContext.createMediaStreamSource(stream);

      await audioContext.audioWorklet.addModule('audio-processor.js');
      audioWorkletNode = new AudioWorkletNode(audioContext, 'audio-processor');

      source.connect(audioWorkletNode);
      audioWorkletNode.connect(audioContext.destination);
      audioWorkletNode.port.onmessage = (event) => {
        const currentBuffer = new Int16Array(event.data.audio_data);
        audioBufferQueue = mergeBuffers(
          audioBufferQueue,
          currentBuffer
        );

        const bufferDuration =
          (audioBufferQueue.length / audioContext.sampleRate) * 1000;

        // wait until we have 100ms of audio data
        if (bufferDuration >= 100) {
          const totalSamples = Math.floor(audioContext.sampleRate * 0.1);

          const finalBuffer = new Uint8Array(
            audioBufferQueue.subarray(0, totalSamples).buffer
          );

          audioBufferQueue = audioBufferQueue.subarray(totalSamples)
          if (onAudioCallback) onAudioCallback(finalBuffer);
        }
      }
    },
    stopRecording() {
      stream?.getTracks().forEach((track) => track.stop());
      audioContext?.close();
      audioBufferQueue = new Int16Array(0);
    }
  }
}
function mergeBuffers(lhs, rhs) {
  const mergedBuffer = new Int16Array(lhs.length + rhs.length)
  mergedBuffer.set(lhs, 0)
  mergedBuffer.set(rhs, lhs.length)
  return mergedBuffer
}

// runs real-time transcription and handles global variables
const run = async () => {
  if (isRecording) {
    if (rt) {
      await rt.close(false);
      rt = null;
    }

    if (microphone) {
      microphone.stopRecording();
      microphone = null;
    }
  } else {
    microphone = createMicrophone();
    await microphone.requestPermission();

    const response = await fetch("http://localhost:5000/get_token");
    const data = await response.json();

    if (data.error) {
      alert(data.error);
      return;
    }

    rt = new assemblyai.RealtimeService({ token: data.token });
    // handle incoming messages to display transcription to the DOM
    const texts = {};
    rt.on("transcript", (message) => {
      let msg = "";
      texts[message.audio_start] = message.text;
      const keys = Object.keys(texts);
      keys.sort((a, b) => a - b);
      for (const key of keys) {
        if (texts[key]) {
          msg += ` ${texts[key]}`;
        }
      }
      messageEl.innerText = msg;
    });

    rt.on("error", async (error) => {
      console.error(error);
      await rt.close();
    });

    rt.on("close", (event) => {
      console.log(event);
      rt = null;
    });

    await rt.connect();
    // once socket is open, begin recording
    messageEl.style.display = "";

    await microphone.startRecording((audioData) => {
      rt.sendAudio(audioData);
    });
  }

  isRecording = !isRecording;
  buttonEl.innerText = isRecording ? "Stop" : "Record";
  titleEl.innerText = isRecording
    ? "Click stop to end recording!"
    : "Click start to begin recording!";
};


async function getToken() {
    try {
        const response = await fetch('http://localhost:5000/get_token');
        const data = await response.json();
        if (response.ok) {
            return data.token;
        } else {
            throw new Error(data.error || 'Failed to fetch the token');
        }
    } catch (error) {
        console.error('Token fetch error:', error.message);
        return null;
    }
}