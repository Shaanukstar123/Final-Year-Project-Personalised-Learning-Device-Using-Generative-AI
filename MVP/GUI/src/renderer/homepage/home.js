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
    const topicId = event.target.dataset.id;
    axios.get(`http://localhost:5000/fetch_story/${topicId}`)
        .then(response => {
            const content = response.data.story;
            const imageUrl = response.data.image_url;
            window.location.href = `../storypage/story.html?content=${encodeURIComponent(content)}&image=${encodeURIComponent(imageUrl)}`;
        })
        .catch(error => console.error('Error fetching story and image:', error));
}

getTopicsFromAPI();
