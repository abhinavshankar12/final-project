// Basic JavaScript for hover effects
function showPoster(element, posterUrl) {
    element.innerHTML = `<img src="${posterUrl}" alt="Movie Poster" style="position: absolute; width: 150px; z-index: 100;">`;
}

function hidePoster(element) {
    element.innerHTML = '';
}

// Add any other JavaScript functions here

// Add a document ready function to set up event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Set up all event listeners here
    
    // Example: Add click event listeners to buttons instead of using inline onclick
    const buttons = document.querySelectorAll('.some-button-class');
    buttons.forEach(button => {
        button.addEventListener('click', function(event) {
            // Handle the click event
        });
    });
    
    // Add other initialization code here

    // Find all movie title links that should have hover effects
    const movieTitleLinks = document.querySelectorAll('.movie-title a');
    
    movieTitleLinks.forEach(link => {
        // Get the movie ID and poster URL from data attributes
        const previewElement = document.getElementById(link.getAttribute('data-preview-id'));
        const posterUrl = link.getAttribute('data-poster-url');
        
        // Add event listeners
        link.addEventListener('mouseover', function() {
            showPoster(previewElement, posterUrl);
        });
        
        link.addEventListener('mouseout', function() {
            hidePoster(previewElement);
        });
    });
}); 