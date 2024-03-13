
const pages = [];
let currentPageIndex = 0;
document.addEventListener('DOMContentLoaded', () => {
    const storyContainer = document.getElementById('story-container');
    const params = new URLSearchParams(window.location.search);
    const content = params.get('content');
    const imageUrl = params.get('image');
    if (content && imageUrl) {
        addPage(content, imageUrl); // This will also automatically display the page
    }
    displayPage(currentPageIndex);
    // displayContentWithAnimation(storyContainer, content);
    // displayImage(storyContainer, imageUrl);

    // Initialize Hammer.js on the storyContainer

    const nextPageButton = document.getElementById('next-page-button');
    if (nextPageButton) {
        nextPageButton.addEventListener('click', fetchNextPage);
    }
    initializeSwipeDetection(storyContainer);
});

function displayContentWithAnimation(container, content) {
    const words = content.split('.');
    words.forEach((word, index) => {
        const span = document.createElement('span');
        span.textContent = word + '. ';
        span.style.opacity = 0;
        span.style.animation = `fadeIn 0.3s ease forwards ${index * 3}s`;
        container.appendChild(span);
    });
}

function displayImage(container, imageUrl) {
    const image = document.createElement('img');
    image.src = imageUrl;
    image.style.width = '100%'; // Adjust as needed
    image.style.height = 'auto';
    image.style.marginTop = '20px'; // Space above the image
    container.appendChild(image);
}

function addPage(content, imageUrl) {
    pages.push({ content, imageUrl, audioUrl: '' });
    currentPageIndex = pages.length - 1; // Update current page to the latest

    fetchAudioForPage(content).then(audioUrl => {
        // Update the audio URL for the current page
        pages[currentPageIndex].audioUrl = audioUrl;
        // Update audio player source if this is the current page being displayed
        if(currentPageIndex === pages.length - 1) {
            playAudio(audioUrl);
            updateAudioButtonVisibility();
        }
    });

    displayPage(currentPageIndex); // Display the latest page
}

function displayPage(index) {
    console.log('Displaying page', index);
    console.log("Current page content: ", pages[index].content);
    const storyContainer = document.getElementById('story-container');
    storyContainer.innerHTML = '';

    if (index >= 0 && index < pages.length) {
        const { content, imageUrl, audioUrl } = pages[index];
        displayContentWithAnimation(storyContainer, content);
        displayImage(storyContainer, imageUrl);
        updateAudioButtonVisibility();
        if (audioUrl) {
            playAudio(audioUrl); // Play the audio if it's available
        }
    }
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

function fetchNextPage() {
    //Post call for the flask backend:@app.route('/continue_story/', methods=['POST'])
    // def continue_story():
    // # Extract user input from the request
    // user_input = request.json.get('user_input', '')
    // # Continue the story
    // output, imageUrl = generateNextPage(user_input, storyChain)
    // return jsonify({"story": output, "image_url": imageUrl})
    console.log('Fetching next page of the story');
    const storyContainer = document.getElementById('story-container');
    const user_input = "I don't know you tell me"
    axios.post('http://localhost:5000/continue_story/', { user_input })
        .then(response => {
            const { story, image_url } = response.data;
            addPage(story, image_url); // Add new page to pages array
        })
        .catch(error => console.error('Error fetching next page:', error));
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