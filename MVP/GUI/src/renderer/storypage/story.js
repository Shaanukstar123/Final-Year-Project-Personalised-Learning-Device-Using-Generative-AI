document.addEventListener('DOMContentLoaded', () => {
    const storyContainer = document.getElementById('story-container');

    // Option 1: Retrieve content from query parameters
    const params = new URLSearchParams(window.location.search);
    const content = params.get('content');

    // Option 2: Retrieve content from local storage
    // const content = localStorage.getItem('storyContent');

    // Display content with animation
    displayContentWithAnimation(storyContainer, content);
});

function displayContentWithAnimation(container, content) {
    console.log("Content: ", content);
    // Split the content into words or characters

    const words = content.split('.');

    words.forEach((word, index) => {
        const span = document.createElement('span');
        span.textContent = word + '. ';
        span.style.opacity = 0;
        span.style.animation = `fadeIn 0.5s ease forwards ${index * 3}s`;
        container.appendChild(span);
    });
}
