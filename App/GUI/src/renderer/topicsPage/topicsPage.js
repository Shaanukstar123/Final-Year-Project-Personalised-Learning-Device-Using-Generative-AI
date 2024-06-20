const axios = require('axios');
const { ipcRenderer } = require('electron');

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const subject = urlParams.get('subject');

    if (subject) {
        fetchTopics(subject);
    }

    const backButton = document.getElementById('back-button');
    if (backButton) {
        backButton.addEventListener('click', () => {
            window.location.href = '../homepage/index.html'; // Adjust the path to your homepage
        });
    }

    const refreshButton = document.getElementById('refresh-button');
    refreshButton.addEventListener('click', () => {
        location.reload();
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

    topics.forEach(topicData => {
        const topicCard = document.createElement('div');
        topicCard.className = 'topic-card';
        topicCard.textContent = topicData.topic;
        topicCard.dataset.name = topicData.topic; // Set topic name as a data attribute

        const gradientColors = getGradientColors(topicData.color);
        topicCard.style.setProperty('--start-color', gradientColors.start);
        topicCard.style.setProperty('--end-color', gradientColors.end);

        topicCard.addEventListener('click', handleTopicClick);
        topicsGrid.appendChild(topicCard);
    });
}

function getGradientColors(baseColor) {
    // Function to generate gradient colors from the base color
    // Adjust the lightness to create a gradient effect
    const startColor = shadeColor(baseColor, -0.1); // Slightly darker
    const endColor = shadeColor(baseColor, 0.1); // Slightly lighter
    return { start: startColor, end: endColor };
}

function shadeColor(color, percent) {
    const f = parseInt(color.slice(1), 16),
          t = percent < 0 ? 0 : 255,
          p = percent < 0 ? -percent : percent,
          R = f >> 16,
          G = f >> 8 & 0x00FF,
          B = f & 0x0000FF;

    const newR = Math.min(Math.max(Math.round((t - R) * p) + R, 0), 255);
    const newG = Math.min(Math.max(Math.round((t - G) * p) + G, 0), 255);
    const newB = Math.min(Math.max(Math.round((t - B) * p) + B, 0), 255);

    const newColor = "#" + (0x1000000 + (newR * 0x10000) + (newG * 0x100) + newB).toString(16).slice(1).toUpperCase();
    
    return newColor;
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
