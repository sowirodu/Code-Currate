// scripts.js
function updateUserMenu(isLoggedIn) {
    var menu = document.getElementById("userMenu");
    if(isLoggedIn) {
        menu.innerHTML = '<a href="/logout">Logout</a>';
    } else {
        menu.innerHTML = '<a href="/register">Register</a><a href="/login">Login</a>';
    }
}
