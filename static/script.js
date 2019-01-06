var popupLogin = document.getElementById("popup-login");
var popupRegister = document.getElementById("popup-register");
var buttonLogin = document.getElementById("button-login");
var buttonCloseLogin = document.getElementsByClassName("close")[0];
var linkRegister = document.getElementById("link-register");
var linkLogin = document.getElementById("link-login");

function showLogin() {
    popupLogin.style.display = "block";
}

function showRegister() {
    popupRegister.style.display = "block";
}

function closePopup() {
    popup = document.querySelector(".popup-container");
    popup.style.display = "none";
}

// When login button is clicked, show the login popup
buttonLogin.onclick = function() {
    showLogin();
};

linkRegister.onclick = function() {
    closePopup();
    showRegister();
}

linkLogin.onclick = function() {
    closePopup();
}


// Close login popup by clicking outside of it
window.onclick = function(event) {
  if (event.target == popupLogin) {
      closePopup();
  }
}

// Close window by clicking 'X' button
buttonCloseLogin.onclick = function () {
    closePopup();
}

// Register
