/*document.getElementById('phone_number').addEventListener('input', function (event) {
    var phoneNumber = event.target.value.replace(/\D/g, ''); // Remove non-digits
    var formattedPhoneNumber = phoneNumber.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
    event.target.value = formattedPhoneNumber;
});

function validatePassword() {
    var password = document.getElementById('password').value;

    // Define your password strength criteria
    var lengthRegex = /^.{8,}$/;
    var uppercaseRegex = /[A-Z]/;
    var lowercaseRegex = /[a-z]/;
    var digitRegex = /\d/;
    var specialCharRegex = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]/;

    // Check if the password meets the criteria
    var isLengthValid = lengthRegex.test(password);
    var isUppercaseValid = uppercaseRegex.test(password);
    var isLowercaseValid = lowercaseRegex.test(password);
    var isDigitValid = digitRegex.test(password);
    var isSpecialCharValid = specialCharRegex.test(password);

    // Display error messages based on validation results
    var errorMessage = "";

    if (!isLengthValid) {
        errorMessage += "Password must be at least 8 characters long.\n";
    }

    if (!isUppercaseValid) {
        errorMessage += "Password must contain at least one uppercase letter.\n";
    }

    if (!isLowercaseValid) {
        errorMessage += "Password must contain at least one lowercase letter.\n";
    }

    if (!isDigitValid) {
        errorMessage += "Password must contain at least one digit.\n";
    }

    if (!isSpecialCharValid) {
        errorMessage += "Password must contain at least one special character.\n";
    }

    // Display the error message or allow form submission
    if (errorMessage !== "") {
        alert(errorMessage);
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}
*/

document.addEventListener('DOMContentLoaded', function () {
    // Toggle mobile menu
    var navbar = document.querySelector('.navbar');
    var menuIcon = document.querySelector('.menu-icon');

    console.log('DOMContentLoaded event fired');

    if (menuIcon && navbar) {
        menuIcon.addEventListener('click', function () {
            navbar.classList.toggle('show');
            console.log('Menu icon clicked');
        });
    } else {
        console.log('Menu icon or navbar not found');
    }
});

