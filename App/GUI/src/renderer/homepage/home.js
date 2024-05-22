const axios = require('axios');

function getTopicsFromAPI() {
    document.addEventListener('DOMContentLoaded', async () => {
        // Check if topics data is stored in localStorage
        const storedTopics = localStorage.getItem('topics');
        if (storedTopics) {
            console.log("Using cached topics");
            createTopicButtons(JSON.parse(storedTopics));
        } else {
            axios.get('http://localhost:5000/get_topics')
                .then(response => {
                    console.log("Topics: ", response.data);
                    createTopicButtons(response.data); // Pass the entire topic object array
                    // Store the topics data in localStorage
                    localStorage.setItem('topics', JSON.stringify(response.data));
                })
                .catch(error => console.error('Error fetching topics:', error));
        }
    });
}



function createTopicButtons(topics) {
    const container = document.getElementById('trending-topics');
    container.innerHTML = ''; // Clear any existing buttons

    topics.forEach(topic => {
        const button = document.createElement('div');
        button.className = 'trending-topic-button';
        button.textContent = topic.new_title;
        button.dataset.id = topic.id; // Set article ID as a data attribute
        button.dataset.content = topic.content;
        button.addEventListener('click', handleButtonClick);
        container.appendChild(button);
    });
    startRandomAnimations();
}

function startRandomAnimations() {
    const buttons = document.querySelectorAll('.trending-topic-button');
    setInterval(() => {
        buttons.forEach(button => button.classList.remove('expandContract'));
        const randomButton = buttons[Math.floor(Math.random() * buttons.length)];
        randomButton.classList.add('expandContract');
    }, 3000);
}

// function handleButtonClick(event) {
//     //print topic.content to console
//     console.log(event.target.dataset.content);
// }

function handleButtonClick(event) {
    const topicId = event.target.dataset.id;
    // Redirect to the story page with just the topic ID
    window.location.href = `../storypage/story.html?topicId=${encodeURIComponent(topicId)}`;
}

getTopicsFromAPI();

