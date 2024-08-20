// massage js 

// Automatically close the message after 3 seconds (3000 milliseconds)
setTimeout(function() {
    var messageDivs = document.querySelectorAll('.messages .alert');
    messageDivs.forEach(function(div) {
        div.classList.add('fade-out'); // Start the fade-out effect
        setTimeout(function() {
            div.style.display = 'none'; // Hide the element after the fade-out
        }, 500); // Wait for the fade-out transition to complete
    });
}, 3000);

