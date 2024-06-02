const axios = require('axios');

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const subject = urlParams.get('subject');

    if (subject) {
        fetchTopics(subject);
    }

    const backButton = document.getElementById('back-button');
    backButton.addEventListener('click', () => {
        window.location.href = '../homepage/index.html'; // Adjust the path to your homepage
    });
});

function fetchTopics(subject) {
    axios.get(`http://localhost:5000/get_subject_topics?subject=${subject}`)
        .then(response => {
            const topics = response.data.topics;
            displayTopics(topics);
        })
        .catch(error => {
            console.error(`Error fetching topics for ${subject}:`, error);
            displayError();
        });
}

function displayTopics(topics) {
    const topicsGrid = document.getElementById('topics-grid');
    topicsGrid.innerHTML = ''; // Clear any existing topics

    topics.forEach(topic => {
        const topicCard = document.createElement('div');
        topicCard.className = 'topic-card';
        topicCard.textContent = topic;
        topicCard.dataset.name = topic; // Set topic name as a data attribute
        topicCard.addEventListener('click', handleTopicClick);
        topicsGrid.appendChild(topicCard);
    });
}

function handleTopicClick(event) {
    const topicName = event.target.dataset.name;
    localStorage.setItem('continuationType', 'content'); // Set the type to 'content'
    localStorage.setItem('continuationTopic', topicName); // Save the topic name
    window.location.href = `../storypage/story.html?topicName=${encodeURIComponent(topicName)}`;
    // Redirect to the story page with the topicName
}

function displayError() {
    const topicsGrid = document.getElementById('topics-grid');
    topicsGrid.innerHTML = '<p class="text-red-500">Failed to load topics. Please try again later.</p>';
}
