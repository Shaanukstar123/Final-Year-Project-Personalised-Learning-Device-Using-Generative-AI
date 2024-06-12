const axios = require('axios');

document.addEventListener('DOMContentLoaded', () => {
    fetchRecommendations();

    const backButton = document.getElementById('back-button');
    if (backButton) {
        backButton.addEventListener('click', () => {
            window.location.href = '../homepage/index.html'; // Adjust the path to your homepage
        });
    }
});

function fetchRecommendations() {
    axios.get('http://localhost:5000/recommendation_topics')
        .then(response => {
            const topics = response.data.topics;
            console.log("Fetched topics with colors:", topics); // Debug log
            displayRecommendations(topics);
        })
        .catch(error => {
            console.error('Error fetching recommendations:', error);
            displayError();
        });
}

function displayRecommendations(topics) {
    const recommendationsGrid = document.getElementById('recommendations-grid');
    if (!recommendationsGrid) {
        console.error('recommendations-grid element not found');
        return;
    }
    recommendationsGrid.innerHTML = ''; // Clear any existing topics

    topics.forEach(topicData => {
        console.log(`Setting color ${topicData.color} for topic ${topicData.topic}`); // Debug log
        const topicCard = document.createElement('div');
        topicCard.className = 'recommendation-topic-card';
        topicCard.textContent = topicData.topic;
        topicCard.dataset.name = topicData.topic; // Set topic name as a data attribute

        const gradientColors = getGradientColors(topicData.color);
        topicCard.style.setProperty('--start-color', gradientColors.start);
        topicCard.style.setProperty('--end-color', gradientColors.end);

        topicCard.addEventListener('click', handleTopicClick);
        recommendationsGrid.appendChild(topicCard);
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
    
    console.log(`Shaded color: ${newColor} from base color: ${color}`); // Debug log
    return newColor;
}

// Example usage:
console.log(shadeColor("#ff5733", 0.2));  // Lighten by 20%
console.log(shadeColor("#ff5733", -0.2)); // Darken by 20%


function handleTopicClick(event) {
    const topicName = event.target.dataset.name;
    localStorage.setItem('continuationType', 'content'); // Set the type to 'content'
    localStorage.setItem('continuationTopic', topicName); // Save the topic name
    window.location.href = `../storypage/story.html?topicName=${encodeURIComponent(topicName)}`;
    // Redirect to the story page with the topicName
}

function displayError() {
    const recommendationsGrid = document.getElementById('recommendations-grid');
    if (recommendationsGrid) {
        recommendationsGrid.innerHTML = '<p class="text-red-500">Failed to load recommendations. Please try again later.</p>';
    } else {
        console.error('recommendations-grid element not found');
    }
}
