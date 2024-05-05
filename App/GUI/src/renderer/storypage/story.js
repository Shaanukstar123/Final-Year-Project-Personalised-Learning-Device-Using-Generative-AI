
const pages = [];
let currentPageIndex = 0;
let incompleteWord = '';
let accumulatedStory = '';

document.addEventListener('DOMContentLoaded', () => {
    const storyContainer = document.getElementById('story-container');
    storyContainer.style.fontFamily = 'Comic Sans MS';
    const params = new URLSearchParams(window.location.search);
    const topicId = params.get('topicId');

    if (topicId) {
        const eventSource = new EventSource(`http://localhost:5000/fetch_story/${topicId}`);
        eventSource.onmessage = function(event) {
            console.log('Received:', event.data);
            // Append data to the container or process it as needed
            const storyContainer = document.getElementById('story-container');
            storyContainer.textContent += event.data + ' ';  // Append each word with a space
        };
        
        eventSource.onerror = function() {
            console.log('Event Source failed');
            eventSource.close();
        };
        
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

function displayContentWithAnimation(container, contentChunk) {
    // Handle incomplete words from previous chunks
    contentChunk = incompleteWord + contentChunk;
    incompleteWord = '';

    // Check if the last character is not a space, indicating a potentially incomplete last word
    if (contentChunk.slice(-1) !== ' ') {
        let lastSpaceIndex = contentChunk.lastIndexOf(' ');
        if (lastSpaceIndex !== -1) {
            incompleteWord = contentChunk.slice(lastSpaceIndex + 1);
            contentChunk = contentChunk.slice(0, lastSpaceIndex);
        } else {
            incompleteWord = contentChunk; // The whole chunk is an incomplete word
            return; // Don't display anything yet
        }
    }

    // Split the content into words and animate each word
    const words = contentChunk.split(/\s+/);

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

// function displayContentWithAnimation(container, content) {
//     container.innerHTML = ''; // Clear previous content
//     const words = content.split(' ');
//     words.forEach((word, index) => {
//         const span = document.createElement('span');
//         span.textContent = word + ' ';
//         span.style.opacity = 0;
//         // Remove any absolute positioning if present and ensure natural text flow
//         span.style.position = 'relative';  // Ensure spans are not positioned absolutely
//         span.style.display = 'inline';     // Display as inline to allow natural flow in text
//         span.style.animation = `fadeIn 0.3s ease forwards ${index * 0.05}s`;
//         container.appendChild(span);
//     });
// }
// function displayContentWithAnimation(container, contentChunk) {
//     const words = contentChunk.split(' ');
//     words.forEach(word => {
//         const span = document.createElement('span');
//         span.textContent = word + ' ';
//         container.appendChild(span);
//     });
// }



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
    const userInput = "User's input here"; // Placeholder for actual user input
    axios.post('http://localhost:5000/continue_story/', { user_input: userInput })
        .then(response => {
            const { story } = response.data;
            addPage(story, ''); // Add new page to pages array, initially without image
            updateImage(story); // Fetch and update the image based on the new story part
        })
        .catch(error => console.error('Error fetching next page:', error));
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


function goToPreviousPage() {
    if (currentPageIndex > 0) {
        currentPageIndex--;
        displayPage(currentPageIndex);
    }
    else{
        currentPageIndex = 0;
    }
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