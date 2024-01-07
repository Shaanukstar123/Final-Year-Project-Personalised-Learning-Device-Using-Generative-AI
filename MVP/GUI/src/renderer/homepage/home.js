function getTopicsFromAPI() {
    document.addEventListener('DOMContentLoaded', (event) => {
        const topics = ["Topic1", "Topic2", "Topic3", "Topic4", "Topic5","Topic6","Topic7","Topic8","Topic9","Topic10"];

        // Directly call createTopicButtons with the static array
        createTopicButtons(topics);
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
