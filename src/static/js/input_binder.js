
var rangeInput = document.getElementById('waste-recycled-range');
var numberInput = document.getElementById('waste-recycled-number');

function updateNumberInput() {
  numberInput.value = rangeInput.value;
}

function updateRangeInput() {
  rangeInput.value = numberInput.value;
}

rangeInput.addEventListener('input', updateNumberInput);
numberInput.addEventListener('input', updateRangeInput);
