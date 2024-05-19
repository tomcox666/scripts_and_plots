// Select the form, input fields, and validation message elements
const form = document.getElementById('email-form');
const firstNameInput = document.getElementById('first-name');
const lastNameInput = document.getElementById('last-name');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const validationMessageElement = document.getElementById('validation-message');
const strengthMeter = document.querySelector('.strength-meter');

// Function to validate the first name
function validateFirstName(firstName) {
    if (firstName === '') { 
        return {
            isValid: false,
            message: 'First name is required.'
        };
    }

    return {
        isValid: true,
        message: ''
    };
}

// Function to validate the last name
function validateLastName(lastName) {
    if (lastName === '') {
        return {
            isValid: false,
            message: 'Last name is required.'
        };
    }

    return {
        isValid: true,
        message: ''
    };
}

// Function to validate the email address
function validateEmail(email) {
    // Regular expression pattern for valid email addresses.
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$/;

    // Check if the email is empty.
    if (email === '') {
        return {
            isValid: false,
            message: 'Email is required.'
        };
    }

    // Check if the email contains the '@' symbol.
    if (email.indexOf('@') === -1) {
        return {
            isValid: false,
            message: 'Email is missing the @ symbol.'
        };
    }

    // Check if the email matches the regular expression pattern.
    if (!emailRegex.test(email)) {
        // If the email does not match the pattern, check if it's because the domain is invalid.
        const parts = email.split('@');
        if (parts.length > 1 && !parts[1].includes('.')) {
            return {
                isValid: false,
                message: 'Email domain is invalid.'
            };
        } else {
            return {
                isValid: false,
                message: 'Email format is invalid.'
            };
        }
    }

    // If all checks pass, the email is valid.
    return {
        isValid: true,
        message: ''
    };
}

// Function to validate the password
function validatePassword(password) {
    if (password === '') {
        return {
            isValid: false,
            message: 'Password is required.'
        };
    }

    if (password.length < 8) {
        return {
            isValid: false,
            message: 'Password must be at least 8 characters long.'
        };
    }

    return {
        isValid: true,
        message: ''
    };
}

// Function to calculate the password strength
function calculatePasswordStrength(password) {
    let strength = 0;

    if (password.length >= 8) {
        strength++;
    }

    if (/[A-Z]/.test(password)) {
        strength++;
    }

    if (/[a-z]/.test(password)) {
        strength++;
    }

    if (/[0-9]/.test(password)) {
        strength++;
    }

    if (/[^A-Za-z0-9]/.test(password)) {
        strength++;
    }

    return strength;
}
function updateStrengthMeter(strength) {
    const strengthMeter = document.querySelector('.strength-meter');
    const strengthLabel = strengthMeter.querySelector('.strength-label');
  
    if (strength === 1) {
      strengthLabel.textContent = 'Weak';
    } else if (strength === 2) {
      strengthLabel.textContent = 'Medium';
    } else if (strength === 3) {
      strengthLabel.textContent = 'Strong';
    } else if (strength === 4) {
      strengthLabel.textContent = 'Very Strong';
    }
  
    strengthMeter.dataset.strength = strength;
  }

// Add event listeners to the input fields for real-time validation
firstNameInput.addEventListener('input', () => {
    // Get the current first name value from the input field
    const firstName = firstNameInput.value;

    // Validate the first name
    const result = validateFirstName(firstName);

    // Display the validation message
    if (!result.isValid) {
        validationMessageElement.textContent = result.message;
    } else {
        validationMessageElement.textContent = '';
    }
});

lastNameInput.addEventListener('input', () => {
    // Get the current last name value from the input field
    const lastName = lastNameInput.value;

    // Validate the last name
    const result = validateLastName(lastName);

    // Display the validation message
    if (!result.isValid) {
        validationMessageElement.textContent = result.message;
    } else {
        validationMessageElement.textContent = '';
    }
});

emailInput.addEventListener('input', () => {
    // Get the current email value from the input field
    const email = emailInput.value;

    // Validate the email
    const result = validateEmail(email);

    // Display the validation message
    if (!result.isValid) {
        validationMessageElement.textContent = result.message;
    } else {
        validationMessageElement.textContent = '';
    }
});

passwordInput.addEventListener('input', () => {
    // Get the current password value from the input field
    const password = passwordInput.value;

    // Validate the password
    const result = validatePassword(password);

    // Calculate the password strength
    const strength = calculatePasswordStrength(password);

    // Update the password strength meter
    updateStrengthMeter(strength);

    // Display the validation message
    if (!result.isValid) {
        validationMessageElement.textContent = result.message;
    } else {
        validationMessageElement.textContent = '';
    }
});

// Add a submit event listener to the form
form.addEventListener('submit', (event) => {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the values from the input fields
    const firstName = firstNameInput.value;
    const lastName = lastNameInput.value;
    const email = emailInput.value;
    const password = passwordInput.value;

    // Validate the input fields
    const firstNameResult = validateFirstName(firstName);
    const lastNameResult = validateLastName(lastName);
    const emailResult = validateEmail(email);
    const passwordResult = validatePassword(password);

    // Check if all fields are valid
    if (!firstNameResult.isValid || !lastNameResult.isValid || !emailResult.isValid || !passwordResult.isValid) { 
        // Display the validation message
        validationMessageElement.textContent = 'Please fix the errors in the form.';
    } else {
        // Clear the validation message
        validationMessageElement.textContent = '';

        // Alert the user that the form has been submitted successfully
        alert('Form submitted successfully.');
    }
});