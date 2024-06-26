const axios = require('axios');
const { runKioskBoard } = require('./keyboard.js');
const { ipcRenderer } = require('electron');

function getTopicsFromAPI() {
    document.addEventListener('DOMContentLoaded', async () => {
        const storedTopics = localStorage.getItem('topics');
        if (storedTopics) {
            console.log("Using cached topics");
            createTopicButtons(JSON.parse(storedTopics));
        } else {
            axios.get('http://localhost:5000/get_topics')
                .then(response => {
                    console.log("Topics: ", response.data);
                    createTopicButtons(response.data);
                    localStorage.setItem('topics', JSON.stringify(response.data));
                })
                .catch(error => console.error('Error fetching topics:', error));
        }
        setupSubjectButtons();
        setupClusterButton();
        setupRecommendationsButton();
        setupFullscreenToggleButton();

        // Initialize the on-screen keyboard for the search input
        initializeVirtualKeyboard();
        setupSearchBar(); // Add this line to set up the search bar
    });
}

function initializeVirtualKeyboard() {
    const searchBar = document.getElementById('search-input');
    if (searchBar) {
        searchBar.classList.add('js-virtual-keyboard');
        searchBar.addEventListener('focus', runKioskBoard);
    }
}

function createTopicButtons(topics) {
    const container = document.getElementById('trending-topics');
    container.innerHTML = '';

    topics.forEach(topic => {
        const button = document.createElement('div');
        button.className = 'trending-topic-button';
        button.textContent = topic.new_title;
        button.dataset.id = topic.id;
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
        const numButtons = Math.floor(Math.random() * buttons.length / 4) + 1;
        for (let i = 0; i < numButtons; i++) {
            const randomButton = buttons[Math.floor(Math.random() * buttons.length)];
            randomButton.classList.add('expandContract');
        }
    }, 1500);
}

function handleButtonClick(event) {
    const topicId = event.target.dataset.id;
    window.location.href = `../storypage/story.html?topicId=${encodeURIComponent(topicId)}`;
}

function setupClusterButton() {
    const clusterButton = document.getElementById('cluster-button');
    if (clusterButton) {
        clusterButton.addEventListener('click', () => {
            axios.get('http://localhost:5000/run_clustering')
                .then(response => {
                    console.log("Clustering run successfully:", response.data);
                })
                .catch(error => {
                    console.error("Error running clustering:", error);
                });
        });
    }
}

function setupSubjectButtons() {
    const subjects = ['history', 'geography', 'science', 'maths', 'english', 'music'];
    subjects.forEach(subject => {
        const subjectElement = document.querySelector(`.${subject}`);
        if (subjectElement) {
            subjectElement.addEventListener('click', () => {
                window.location.href = `../topicsPage/topics.html?subject=${subject}`;
            });
        }
    });
}

function setupRecommendationsButton() {
    const recommendationsButton = document.getElementById('recommendations-button');
    if (recommendationsButton) {
        recommendationsButton.addEventListener('click', () => {
            window.location.href = '../recommendationspage/recommendations.html';
        });
    }
}

function setupSearchBar() {
    const searchBar = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    if (searchBar && searchButton) {
        searchButton.addEventListener('click', () => {
            const query = searchBar.value;
            if (query) {
                window.location.href = `../storypage/story.html?customTopic=${encodeURIComponent(query)}`;
            }
        });
    }
}

function setupFullscreenToggleButton() {
    const fullscreenButton = document.getElementById('fullscreen-toggle');
    if (fullscreenButton) {
        fullscreenButton.addEventListener('click', () => {
            ipcRenderer.send('toggle-fullscreen');
        });
    }
}

getTopicsFromAPI();
