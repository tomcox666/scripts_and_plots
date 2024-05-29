// Get the display element
let display = document.getElementById('display');
let expression = '';

/**
 * Append a character to the expression and update the display.
 * @param {string} char - The character to append.
 */
function append(char) {
    expression += char;
    display.value = expression;
}

/**
 * Clear the display and reset the expression.
 */
function clearDisplay() {
    expression = '';
    display.value = expression;
}

/**
 * Remove the last character from the expression and update the display.
 */
function backspace() {
    expression = expression.slice(0, -1);
    display.value = expression;
}

/**
 * Calculate the result of the expression and update the display.
 */
function calculate() {
    try {
        // Evaluate the expression
        let result = eval(expression);
        expression = result.toString();
        display.value = expression;
    } catch (error) {
        // Display an error message if the expression is invalid
        display.value = 'Error';
        expression = '';
    }
}

// Add event listener for keyboard input
document.addEventListener('keydown', (event) => {
    if (event.key >= '0' && event.key <= '9') {
        append(event.key);
    } else if (event.key === '+' || event.key === '-' || event.key === '*' || event.key === '/') {
        append(event.key);
    } else if (event.key === '(' || event.key === ')') {
        append(event.key);
    } else if (event.key === 'Backspace') {
        backspace();
    } else if (event.key === 'Enter') {
        calculate();
    } else if (event.key === 'Delete') {
        clearDisplay();
    }
});