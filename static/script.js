/*
 * Code to handle opening and closing of login screen
 */

var popupLogin = document.getElementById("popup-login");
var popupRegister = document.getElementById("popup-register");
var buttonLogin = document.getElementById("button-login");
var buttonCloseLogin = document.getElementsByClassName("close")[0];
var buttonCloseRegister = document.getElementsByClassName("close")[1];
var linkRegister = document.getElementById("link-register");
var linkLogin = document.getElementById("link-login");

function showLogin() {
    popupLogin.style.display = "block";
}

function showRegister() {
    popupRegister.style.display = "block";
}

function closePopups() {
    popups = document.getElementsByClassName("popup-container");
    for (var i = 0; i < popups.length; i++)
        popups[i].style.display = "none";
}

// When login button is clicked, show the login popup
buttonLogin.onclick = function() {
    showLogin();
};

linkRegister.onclick = function() {
    closePopups();
    showRegister();
}

linkLogin.onclick = function() {
    closePopups();
    showLogin();
}


// Close login popup by clicking outside of it
window.onclick = function(event) {
    if (event.target == popupLogin || event.target == popupRegister)
        closePopups();
}

// Close window by clicking 'X' button
buttonCloseLogin.onclick = function () {
    closePopups();
}

buttonCloseRegister.onclick = function () {
    closePopups();
}