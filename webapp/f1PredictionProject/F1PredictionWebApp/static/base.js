const staticUrls = {
    moon: "/static/moon.png",
    lightProfileIcon: "/static/light-profile-icon.png",
    sun: "/static/sun.png",
    profileIcon: "/static/profileicon.png"
};

document.addEventListener("DOMContentLoaded", function() {
    var theme = localStorage.getItem("theme");
    if (theme) {
        applyTheme(theme);
    }
});

function toggleTheme() {
    var themeImage = document.getElementById("theme_switch");
    var profileImage = document.getElementById("profile_image");

    var currentSrc = themeImage.src;
    var currentFilename = currentSrc.split('/').pop();
    var body = document.body;
    var cards = document.querySelectorAll('.nav-card');

    if (currentFilename === "sun.png") {
        themeImage.src = staticUrls.moon;
        if (profileImage) {
            profileImage.src = staticUrls.lightProfileIcon;
        }
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        cards.forEach(function(card) {
            card.classList.remove('light');
            card.classList.add('dark');
        });
        localStorage.setItem("theme", "dark-mode");
    } else {
        themeImage.src = staticUrls.sun;
        if (profileImage) {
            profileImage.src = staticUrls.profileIcon;
        }
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        cards.forEach(function(card) {
            card.classList.remove('dark');
            card.classList.add('light');
        });
        localStorage.setItem("theme", "light-mode");
    }

    return false;
}

function applyTheme(theme) {
    var themeImage = document.getElementById("theme_switch");
    var profileImage = document.getElementById("profile_image");
    var body = document.body;
    var cards = document.querySelectorAll('.light');

    if (theme === "dark-mode") {
        themeImage.src = staticUrls.moon;
        if (profileImage) {
            profileImage.src = staticUrls.lightProfileIcon;
        }
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        cards.forEach(function(card) {
            card.classList.remove('light');
            card.classList.add('dark');
        });
    } else {
        themeImage.src = staticUrls.sun;
        if (profileImage) {
            profileImage.src = staticUrls.profileIcon;
        }
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        cards.forEach(function(card) {
            card.classList.remove('dark');
            card.classList.add('light');
        });
    }
}

function toggleMenu() {
    const menu = document.getElementById('menu-div');
    menu.classList.toggle('show');
    if (menu.classList.contains('show')) {
        menu.style.maxHeight = menu.scrollHeight + "px";
    } else {
        menu.style.maxHeight = "0";
    }

}