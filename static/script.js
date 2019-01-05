console.log(document.documentURI);

window.onload = function () {
    var popupLogin = document.getElementById("popup-login");
    var buttonLogin = document.getElementById("button-login");

    // When login button is clicked, show the login popup
    buttonLogin.onclick = function () {
        popupLogin.style.display = "block";
    }

    // Close login popup by clicking outside of it
    window.onclick = function(event) {
      if (event.target == popupLogin) {
        popupLogin.style.display = "none";
      }
    }
}