
// Get the elements
var rangeInput = document.getElementById('waste-recycled-range');
var numberInput = document.getElementById('waste-recycled-number');

// Function to update the number input
function updateNumberInput() {
    numberInput.value = rangeInput.value;
}

// Function to update the range input
function updateRangeInput() {
    rangeInput.value = numberInput.value;
}

// Add event listener to the range input
rangeInput.addEventListener('input', updateNumberInput);

// Add event listener to the number input
numberInput.addEventListener('input', updateRangeInput);
