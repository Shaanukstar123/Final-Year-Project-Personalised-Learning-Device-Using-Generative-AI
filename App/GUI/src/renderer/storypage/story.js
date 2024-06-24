//import assemblyai library:
const assemblyai = require('assemblyai');
const pages = [];
let currentPageIndex = 0;
// let incompleteWord = ''; //For streaming
// let accumulatedStory = '';
let ws = null;  // WebSocket instance
const buttonEl = document.getElementById("speak");
const messageEl = document.getElementById("textarea");
const titleEl = document.getElementById("titlearea");
messageEl.style.display = "none";
let isRecording = false;
let rt;
let microphone = null;
let userTranscription = '';
let cumulativeDelay = 0;
let storyContainer;

document.addEventListener('DOMContentLoaded', () => {
    const storyContainer = document.getElementById('story-container');
    storyContainer.style.fontFamily = 'Comic Sans MS';
    const params = new URLSearchParams(window.location.search);
    const topicId = params.get('topicId');
    const topicName = params.get('topicName');
    const query = params.get('customTopic');
    const buttonEl = document.getElementById("speak");
    const messageEl = document.getElementById("textarea");
    let isRecording = false;
    buttonEl.addEventListener("click", () => run());

    if (topicId) {
        fetchStory(topicId);
    } else if (topicName) {
        fetchTopicContent(topicName);
    }else if (query) {
        fetchCustomContent(query);
    } else {
        console.error('No topicId or topicName provided.');
    }

    const homeButton = document.getElementById('homeButton');
    if (homeButton) {
        homeButton.addEventListener('click', function() {
            window.location.href = '../homepage/index.html';
        });
    }

    const nextPageButton = document.getElementById('next-page-button');
    if (nextPageButton) {
        nextPageButton.addEventListener('click', goToNextPage);
    }

    const prevPageButton = document.getElementById('previous-page-button');
    if (prevPageButton) {
        prevPageButton.addEventListener('click', goToPreviousPage);
    }
    initialiseSwipeDetection(storyContainer);
});

function fetchStory(topicId){
    showLoadingScreen();
    const cachedStory = localStorage.getItem(`story_${topicId}`);
    if (cachedStory) {
        const storyData = JSON.parse(cachedStory);
        const storyContent = storyData.story + storyData.question;
        addPage(storyContent, storyData.imagePrompt, storyData.imagePrompt, storyData.audioUrl)
            .then(() => {
                
                displayContent(storyContainer, storyContent);
                if (storyData.audioUrl) {
                    playAudio(storyData.audioUrl);
                }
                
            });
    } else {
        axios.get(`http://localhost:5000/fetch_story/${topicId}`)
            .then(response => {
                const storyContent = response.data.story + response.data.question;
                const imagePrompt = response.data.imagePrompt;
                const storyData = {
                    story: response.data.story,
                    question: response.data.question,
                    imagePrompt: imagePrompt,
                    audioUrl: ''
                };
                localStorage.setItem(`story_${topicId}`, JSON.stringify(storyData));
                addPage(storyContent, imagePrompt, '', '')
                    .then(() => {
                        displayContent(storyContainer, storyContent);
                        updateImage(imagePrompt);
                    });
            })
            .catch(error => {
                console.error('Error fetching story:', error);
            });
    }
}

function fetchTopicContent(topicName) {
    const cachedStory = localStorage.getItem(`story_${topicName}`);
    if (cachedStory) {
        const storyData = JSON.parse(cachedStory);
        const storyContent = storyData.story + storyData.question;
        addPage(storyContent, storyData.imagePrompt, storyData.imagePrompt, storyData.audioUrl)
            .then(() => {
                displayContent(storyContainer, storyContent);
                if (storyData.audioUrl) {
                    playAudio(storyData.audioUrl);
                }
            });
    } else {
        axios.get(`http://localhost:5000/fetch_content?topic=${encodeURIComponent(topicName)}`)
            .then(response => {
                const storyContent = response.data.story + response.data.question;
                const imagePrompt = response.data.imagePrompt;
                const storyData = {
                    story: response.data.story,
                    question: response.data.question,
                    imagePrompt: imagePrompt,
                    audioUrl: ''
                };
                localStorage.setItem(`story_${topicName}`, JSON.stringify(storyData));
                addPage(storyContent, imagePrompt, '', '')
                    .then(() => {
                        displayContent(storyContainer, storyContent);
                        updateImage(imagePrompt);
                    });
            })
            .catch(error => {
                console.error('Error fetching content:', error);
            });
    }
}

function fetchCustomContent(topicName) {
    axios.get(`http://localhost:5000/custom_content`, { params: { query: topicName } })
    .then(response => {
        //ensure global story container is the one being used
        const storyContent = response.data.story + response.data.question;
        const imagePrompt = response.data.imagePrompt;
        addPage(storyContent, imagePrompt, '', '')
            .then(() => {
                displayContent(storyContainer, storyContent);
                updateImage(imagePrompt);
            });
    })
    .catch(error => {
        console.error('Error fetching story:', error);
    });
}

function fetchNextPage() {
    console.log('Fetching next page of the story');

    const userInput = userTranscription; // Use the transcribed text
    console.log('User input:', userInput);

    const topicId = new URLSearchParams(window.location.search).get('topicId');
    const topicName = new URLSearchParams(window.location.search).get('topicName');
    let storyType = '';
        
    if (topicId) {
        storyType = 'story';
        // const cachedStory = localStorage.getItem(`story_${topicId}`);
        // if (cachedStory) {
        //     storyType = JSON.parse(cachedStory).type;
        // }
    } else if (topicName){
        storyType = 'content';
        // const cachedStory = localStorage.getItem(`story_${topicName}`);
        // if (cachedStory) {
        //     storyType = JSON.parse(cachedStory).type;
        // }
    } else{
        storyType = 'custom';
    }
    console.log("storyType", storyType)
    console.log("TopicId", topicId)
    console.log("TopicName", topicName)

    let endpoint;
    console.log("storyType", storyType)
    if (storyType === 'story') {
        endpoint = 'continue_story';
    } else if (storyType === 'content') {
        endpoint = 'continue_content';
    }
    else if (storyType === 'custom') {
        endpoint = 'continue_custom_content';
    } else {
        console.error('Unknown continuation type.');
        return;
    }

    axios.get(`http://localhost:5000/${endpoint}`, {
        params: {
            user_input: userInput
        }
    })
    .then(response => {
        console.log('Next page content:', response.data);
        const storyContent = response.data.story;
        const imagePrompt = response.data.imagePrompt;
        if (storyContent) {
            addPage(storyContent, ''); // Add new page to pages array, initially without image
            const storyContainer = document.getElementById('story-container');
            displayContent(storyContainer, storyContent);
            updateImage(imagePrompt);

            if (topicId) {
                const cachedStory = localStorage.getItem(`story_${topicId}`);
                let storyData = cachedStory ? JSON.parse(cachedStory) : { story: '', question: '', imagePrompt: '', audioUrl: '' };
                storyData.story += ' ' + storyContent;
                storyData.imagePrompt = imagePrompt;
                localStorage.setItem(`story_${topicId}`, JSON.stringify(storyData));
            } else if (topicName) {
                const cachedStory = localStorage.getItem(`story_${topicName}`);
                let storyData = cachedStory ? JSON.parse(cachedStory) : { story: '', question: '', imagePrompt: '', audioUrl: '' };
                storyData.story += ' ' + storyContent;
                storyData.imagePrompt = imagePrompt;
                localStorage.setItem(`story_${topicName}`, JSON.stringify(storyData));
            }
        } else {
            console.error('Story content is undefined');
        }
    })
    .catch(error => {
        console.error('Error fetching next page:', error);
    });

    // Clear current content to display new page content
    const storyContainer = document.getElementById('story-container');
    storyContainer.innerHTML = '';
    cumulativeDelay = 0;  // Reset the delay for word animation
}

function updateImage(prompt) {
    return new Promise((resolve, reject) => {
        if (prompt.length > 0) {
            const topicId = new URLSearchParams(window.location.search).get('topicId');
            const currentPage = currentPageIndex; // Get the current page index
            const cachedStory = localStorage.getItem(`story_${topicId}`);
            let storyData = cachedStory ? JSON.parse(cachedStory) : { pages: [] };

            // Ensure the pages array exists
            if (!storyData.pages) {
                storyData.pages = [];
            }

            // Check if the image for the current page is already cached
            if (storyData.pages[currentPage] && storyData.pages[currentPage].imageUrl) {
                pages[currentPage].imageUrl = storyData.pages[currentPage].imageUrl;
                displayImage(document.getElementById('story-container'), storyData.pages[currentPage].imageUrl);
                resolve();
            } else {
                axios.post('http://localhost:5000/get_image', { text: prompt })
                    .then(response => {
                        console.log("image response", response.data);
                        const imageUrl = response.data.imageUrl;

                        if (currentPage >= 0 && currentPage < pages.length) {
                            pages[currentPage].imageUrl = imageUrl; // Update current page with the new image URL
                            displayImage(document.getElementById('story-container'), imageUrl);

                            // Cache the new image URL for the current page of the current story
                            if (!storyData.pages[currentPage]) {
                                storyData.pages[currentPage] = {};
                            }
                            storyData.pages[currentPage].imageUrl = imageUrl;
                            localStorage.setItem(`story_${topicId}`, JSON.stringify(storyData));
                            resolve();
                        } else {
                            console.error('Page not found at currentPageIndex');
                            reject();
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching image:', error);
                        reject(error);
                    });
            }
        } else {
            resolve();
        }
    });
}

function updateImageForPage(pageIndex, dallePrompt) {
    return new Promise((resolve, reject) => {
        const topicId = new URLSearchParams(window.location.search).get('topicId');
        if (topicId) {
            const cachedStory = localStorage.getItem(`story_${topicId}`);
            let storyData = cachedStory ? JSON.parse(cachedStory) : { pages: [] };

            // Ensure the pages array exists
            if (!storyData.pages) {
                storyData.pages = [];
            }

            if (storyData.pages[pageIndex] && storyData.pages[pageIndex].imageUrl) {
                pages[pageIndex].imageUrl = storyData.pages[pageIndex].imageUrl;
                displayImage(document.getElementById('story-container'), storyData.pages[pageIndex].imageUrl);
                resolve();
            } else {
                if (dallePrompt) {
                    updateImage(dallePrompt).then(resolve).catch(reject);
                } else {
                    resolve();
                }
            }
        } else {
            resolve();
        }
    });
}


function addPage(content, dallePrompt = '', imageUrl = '', audioUrl = '') {
    return new Promise((resolve, reject) => {
        pages.push({ content, imageUrl, audioUrl });
        currentPageIndex = pages.length - 1;
        if (!audioUrl) {
            fetchAudioForPage(content).then(audioUrl => {
                pages[currentPageIndex].audioUrl = audioUrl;
                if (currentPageIndex === pages.length - 1) {
                    playAudio(audioUrl);
                    updateAudioButtonVisibility();
                }
            });
        } else {
            if (currentPageIndex === pages.length - 1) {
                playAudio(audioUrl);
                updateAudioButtonVisibility();
            }
        }
        displayPage(currentPageIndex);
        // Ensure the image is updated and cached if not already cached
        const topicId = new URLSearchParams(window.location.search).get('topicId');
        const cachedStory = localStorage.getItem(`story_${topicId}`);
        let storyData = cachedStory ? JSON.parse(cachedStory) : { pages: [] };

        // Ensure the pages array exists
        if (!storyData.pages) {
            storyData.pages = [];
        }

        // Ensure the specific page object exists in the pages array
        if (!storyData.pages[currentPageIndex]) {
            storyData.pages[currentPageIndex] = {};
        }

        if (!storyData.pages[currentPageIndex].imageUrl) {
            updateImageForPage(currentPageIndex, dallePrompt).then(resolve).catch(reject);
        } else {
            resolve();
        }
    });
}

function displayContent(container, content, animate = true) {
    // Clear the container first
    container.innerHTML = '';
    hideLoadingScreen();

    if (animate) {
        const words = content.split(/\s+/);
        cumulativeDelay = 0;  // Reset the delay for word animation
        const wordDisplayInterval = 100; // Interval in milliseconds between each word
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
    } else {
        const p = document.createElement('p');
        p.textContent = content;
        p.style.opacity = 1; // Directly visible
        p.style.wordWrap = 'break-word'; // Ensure long words break and don't overflow
        p.style.overflowWrap = 'break-word'; // Break long words
        container.appendChild(p);
    }
}

function displayPage(index, animate = true) {
    const storyContainer = document.getElementById('story-container');
    storyContainer.innerHTML = ''; // Clear previous content

    if (index >= 0 && index < pages.length) {
        const { content, imageUrl, audioUrl } = pages[index];
        displayContent(storyContainer, content, animate);
        if (imageUrl) {
            displayImage(storyContainer, imageUrl);
        }
        if (audioUrl) {
            playAudio(audioUrl);
        }
    }
}

function displayImage(container, imageUrl) {
    const existingImage = container.querySelector('img');
    if (existingImage) {
        existingImage.src = imageUrl;
    } else {
        const imgElement = document.createElement('img');
        imgElement.src = imageUrl;
        imgElement.style.width = '80%'; // Adjust width to be responsive
        imgElement.style.height = 'auto'; // Maintain aspect ratio
        imgElement.style.marginTop = '20px';
        imgElement.style.display = 'block';
        imgElement.style.marginLeft = 'auto';
        imgElement.style.marginRight = 'auto';
        imgElement.style.border = '2px solid black';
        container.appendChild(imgElement);
    }
}

function initialiseSwipeDetection(element) {
    if (!element) return;

    const hammer = new Hammer(element);
    hammer.get('swipe').set({ direction: Hammer.DIRECTION_HORIZONTAL });

    hammer.on('swipeleft', function(ev) {
        console.log('Swiped left');
        if (Math.abs(ev.deltaX) > Math.abs(ev.deltaY)) {
            ev.preventDefault();  // Prevent the default behavior only if the swipe is more horizontal than vertical
            goToNextPage();
        }
    });

    hammer.on('swiperight', function(ev) {
        console.log('Swiped right');
        if (Math.abs(ev.deltaX) > Math.abs(ev.deltaY)) {
            ev.preventDefault();  // Prevent the default behavior only if the swipe is more horizontal than vertical
            goToPreviousPage();
        }
    });

    // // Optionally, prevent touch scrolling on this element
    // element.addEventListener('touchmove', function(e) {
    //     e.preventDefault();
    // }, { passive: false });
}

function goToNextPage() {
    if (currentPageIndex < pages.length - 1) {
        currentPageIndex++;
        displayPage(currentPageIndex,false);
    } else {
        // If at the last page, fetch next page
        fetchNextPage();
    }
}

function goToPreviousPage() {
    if (currentPageIndex > 0) {
        currentPageIndex--;
        displayPage(currentPageIndex,false);
    } else {
        currentPageIndex = 0;
    }
}

function fetchAudioForPage(text) {
    return new Promise((resolve, reject) => {
        // Assuming this endpoint returns the audio content as a blob
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

            // Cache the audio URL
            const topicId = new URLSearchParams(window.location.search).get('topicId');
            if (topicId) {
                const cachedStory = localStorage.getItem(`story_${topicId}`);
                let storyData = cachedStory ? JSON.parse(cachedStory) : { story: '', question: '', imagePrompt: '', audioUrl: '' };
                storyData.audioUrl = audioUrl;
                localStorage.setItem(`story_${topicId}`, JSON.stringify(storyData));
            }

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
    
    // audioPlayer.play();
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
      userTranscription = msg.trim();
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


function showLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.style.display = 'flex';
    }
}

function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.style.display = 'none';
    }
}