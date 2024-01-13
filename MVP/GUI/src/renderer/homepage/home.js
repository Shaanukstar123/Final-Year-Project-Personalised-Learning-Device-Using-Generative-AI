const axios = require('axios');

function getTopicsFromAPI() {
    document.addEventListener('DOMContentLoaded', async () => {
        console.log("Working");
        axios.get('http://localhost:5000/get_topics')
            .then(response => {
                const topics = response.data.map(item => item.new_title);
                console.log("Topics: ", topics);
                createTopicButtons(topics);
            })
            .catch(error => console.error('Error fetching topics:', error));
    });
}


function createTopicButtons(topics) {
    const container = document.getElementById('bottom-topics'); // New container ID
    // Clear any existing buttons first
    container.innerHTML = '';
    topics.forEach(topic => {
      const button = document.createElement('div');
      button.className = 'bottom-topic-button'; // New class for smaller buttons
      button.textContent = topic;
      container.appendChild(button);
    });
}

getTopicsFromAPI();
