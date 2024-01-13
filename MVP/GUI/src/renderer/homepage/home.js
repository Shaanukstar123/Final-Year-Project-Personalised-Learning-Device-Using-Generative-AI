const axios = require('axios');

function getTopicsFromAPI() {
    document.addEventListener('DOMContentLoaded', async () => {
        axios.get('http://localhost:5000/get_topics')
            .then(response => {
                console.log("Topics: ", response.data);
                createTopicButtons(response.data); // Pass the entire topic object array
            })
            .catch(error => console.error('Error fetching topics:', error));
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
}

// function handleButtonClick(event) {
//     //print topic.content to console
//     console.log(event.target.dataset.content);
// }

function handleButtonClick(event) {
    const content = event.target.dataset.content;
    //call api with parameter topic id to update content
    axios.get(`http://localhost:5000/update_topic/${event.target.dataset.id}`)
        .then(response => {
            console.log("Updated topic: ", response.data);
            content = response.data
        })
        .catch(error => console.error('Error updating topic:', error));
    // Option 1: Using query parameters
    window.location.href = `../storypage/story.html?content=${encodeURIComponent(content)}`;

    // Option 2: Using local storage
    // localStorage.setItem('storyContent', content);
    // window.location.href = 'story.html';
}

getTopicsFromAPI();
