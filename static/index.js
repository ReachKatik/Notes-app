document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');

    // Close button event listener
    alerts.forEach(function(alert) {
        const closeBtn = alert.querySelector('.close-msg');
        closeBtn.addEventListener('click', function() {
            alert.style.display = 'none';
        });

        // Timeout to hide flash messages after 5 seconds (5000 milliseconds)
        setTimeout(function() {
            alert.style.display = 'none';
        }, 5000);  // Adjust the time as per your requirement (in milliseconds)
    });
});

function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId}),
    }).then(_res_ => {
        window.location.href = "/";
    
    });
}