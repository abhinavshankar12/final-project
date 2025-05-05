// javascript for hover effects and more

// shows the movie poster when hovering over title
function showPoster(element, posterUrl) {
    element.innerHTML = '<img src="' + posterUrl + '" alt="Movie Poster" style="position: absolute; width: 150px; z-index: 100;">';
}

// hides the movie poster when not hovering
function hidePoster(element) {
    element.innerHTML = '';
}

// runs when page loads
window.onload = function() {
    var movieLinks = document.getElementsByClassName('movie-title');
    
    for (var i = 0; i < movieLinks.length; i++) {
        var links = movieLinks[i].getElementsByTagName('a');
        if (links.length > 0) {
            var link = links[0];
            
            var previewId = link.getAttribute('data-preview-id');
            var posterUrl = link.getAttribute('data-poster-url');
            
            if (previewId && posterUrl) {
                var previewElement = document.getElementById(previewId);
                
                link.onmouseover = function(previewElement, posterUrl) {
                    return function() {
                        showPoster(previewElement, posterUrl);
                    };
                }(previewElement, posterUrl);
                
                link.onmouseout = function(previewElement) {
                    return function() {
                        hidePoster(previewElement);
                    };
                }(previewElement);
            }
        }
    }
    
    var searchButton = document.querySelector('.search-form button');
    if (searchButton) {
        searchButton.onclick = function() {
            var searchInput = document.querySelector('.search-form input[type="text"]');
            return true;
        };
    }
};