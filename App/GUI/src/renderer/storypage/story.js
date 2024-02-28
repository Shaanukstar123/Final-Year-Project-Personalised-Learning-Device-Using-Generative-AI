document.addEventListener('DOMContentLoaded', () => {
    const storyContainer = document.getElementById('story-container');
    const params = new URLSearchParams(window.location.search);
    const content = params.get('content');
    const imageUrl = params.get('image');

    displayContentWithAnimation(storyContainer, content);
    displayImage(storyContainer, imageUrl);
});

function displayContentWithAnimation(container, content) {
    const words = content.split('.');
    words.forEach((word, index) => {
        const span = document.createElement('span');
        span.textContent = word + '. ';
        span.style.opacity = 0;
        span.style.animation = `fadeIn 0.5s ease forwards ${index * 3}s`;
        container.appendChild(span);
    });
}

function displayImage(container, imageUrl) {
    const image = document.createElement('img');
    image.src = imageUrl;
    image.style.width = '100%'; // Adjust as needed
    image.style.height = 'auto';
    image.style.marginTop = '20px'; // Space above the image
    container.appendChild(image);
}
