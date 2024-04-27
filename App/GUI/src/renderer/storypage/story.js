
const pages = [];
let currentPageIndex = 0;
document.addEventListener('DOMContentLoaded', () => {
    const storyContainer = document.getElementById('story-container');
    const params = new URLSearchParams(window.location.search);
    const topicId = params.get('topicId');

    if (topicId) {
        const eventSource = new EventSource(`http://localhost:5000/fetch_story/${topicId}`);
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            displayContentWithAnimation(storyContainer, data.story);
            // Optionally, trigger image updates only if there's significant new content
            updateImage(data.story);
        };

        eventSource.onerror = function() {
            console.log('Event Source failed');
            eventSource.close();
        };
    }

    const nextPageButton = document.getElementById('next-page-button');
    if (nextPageButton) {
        nextPageButton.addEventListener('click', fetchNextPage);
    }
    initializeSwipeDetection(storyContainer);
});

// Existing functions from story.js here...

function updateImage(storyContent) {
    axios.post('http://localhost:5000/get_image', { text: storyContent })
        .then(response => {
            const { image_url } = response.data;
            pages[currentPageIndex].imageUrl = image_url; // Update current page with the new image URL
            displayImage(document.getElementById('story-container'), image_url);
        })
        .catch(error => console.error('Error fetching image:', error));
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
function displayContentWithAnimation(container, contentChunk) {
    const words = contentChunk.split(' ');
    words.forEach(word => {
        const span = document.createElement('span');
        span.textContent = word + ' ';
        container.appendChild(span);
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
    const userInput = "User's input here"; // Placeholder for actual user input
    axios.post('http://localhost:5000/continue_story/', { user_input: userInput })
        .then(response => {
            const { story } = response.data;
            addPage(story, ''); // Add new page to pages array, initially without image
            updateImage(story); // Fetch and update the image based on the new story part
        })
        .catch(error => console.error('Error fetching next page:', error));
}

function initializeSwipeDetection(element) {
    // Create a new instance of Hammer on the element
    const hammer = new Hammer(element);

    // Listen for swipeleft events
    hammer.on('swipeleft', function() {
        console.log('Swiped left');
        goToNextPage(); // Call your function to fetch the next page of the story
    });

    // Optionally, listen for swiperight events to go back
    hammer.on('swiperight', function() {
        console.log('Swiped right');
        goToPreviousPage();
        // Implement or call a function to go back in the story, if applicable
    });
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