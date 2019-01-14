/*
 * Code to handle opening and closing of login screen
 */

var popupLogin = document.getElementById("popup-login");
var buttonLogin = document.getElementById("button-login");
var buttonCloseLogin = document.getElementById("close-login");
var checkboxTogglePwd = document.getElementById("toggle-pwd");
var inputPassword = document.getElementById("input-pwd");
var inputVerify = document.getElementById("input-verify");


// Handles login and registration button actions
if (buttonLogin) {

    buttonLogin.onclick = function () {
        popupLogin.style.display = "block";
    }

    buttonCloseLogin.onclick = function () {
        popupLogin.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == popupLogin)
            popupLogin.style.display = "none";
    }

    // Toggle password visibility
    checkboxTogglePwd.onclick = function () {
        if (inputPassword.type == "password") {
            inputPassword.type = "text";
            if (inputVerify) inputVerify.type = "text";
        } else {
            inputPassword.type = "password";
            if (inputVerify) inputVerify.type = "password";
        }
    }
}
