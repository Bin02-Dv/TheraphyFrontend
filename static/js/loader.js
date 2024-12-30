window.addEventListener("load", () => {
    const loader = document.querySelector(".loader");

    loader.classList.add("loader-hidden");

    loader.addEventListener("transitionend", () => {
        document.body.removeChild("loader");
    })
})

// ======== dark mode ========
document.addEventListener('DOMContentLoaded', function() {
    const toggleMode = document.getElementById('toggle-mode');
    const icon = toggleMode.querySelector('i');

    // Check local storage to keep user preference
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-moon');
    }

    toggleMode.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent the default anchor behavior

        document.body.classList.toggle('dark-mode');
        
        // Toggle the icon
        if (document.body.classList.contains('dark-mode')) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-moon');
            localStorage.setItem('theme', 'dark');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            localStorage.setItem('theme', 'light');
        }
    });
});