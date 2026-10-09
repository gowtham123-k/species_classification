document.addEventListener('DOMContentLoaded', () => {
  // Select DOM Elements
  const predictionForm = document.getElementById('predictionForm');
  const errorContainer = document.getElementById('errorContainer');
  const errorMessage = document.getElementById('errorMessage');
  
  const islandInput = document.getElementById('island');
  const billLengthInput = document.getElementById('billLength');
  const billDepthInput = document.getElementById('billDepth');
  const flipperLengthInput = document.getElementById('flipperLength');
  const bodyMassInput = document.getElementById('bodyMass');
  
  const clearBtn = document.getElementById('clearBtn');
  
  const resultCard = document.getElementById('resultCard');
  const resultEmoji = document.getElementById('resultEmoji');
  const resultSpeciesName = document.getElementById('resultSpeciesName');
  const resultSummary = document.getElementById('resultSummary');
  const resultExplanation = document.getElementById('resultExplanation');

  // Handle Form Submission / Prediction Action
  predictionForm.addEventListener('submit', (event) => {
    event.preventDefault();
    
    // 1. Hide any existing results or errors
    resultCard.classList.add('hidden');
    resultCard.classList.remove('revealed');
    errorContainer.classList.add('hidden');

    // 2. Extract values and validate
    const island = islandInput.value;
    const billLength = parseFloat(billLengthInput.value);
    const billDepth = parseFloat(billDepthInput.value);
    const flipperLength = parseFloat(flipperLengthInput.value);
    const bodyMass = parseFloat(bodyMassInput.value);

    // Friendly Validation
    if (!island) {
      showError('Please select an Island.');
      return;
    }

    if (isNaN(billLength) || isNaN(billDepth) || isNaN(flipperLength) || isNaN(bodyMass)) {
      showError('Please enter numerical measurements for all fields.');
      return;
    }

    if (billLength <= 0 || billDepth <= 0 || flipperLength <= 0 || bodyMass <= 0) {
      showError('Measurements must be positive numbers greater than zero.');
      return;
    }

    // 3. Classification Algorithm
    let speciesName = '';
    let emoji = '🐧';
    let explanation = '';

    if (bodyMass >= 4500) {
      speciesName = 'Gentoo Penguin';
      emoji = '🐧'; // Can be customized or kept as standard penguin emoji
      explanation = `The body mass is ${bodyMass}g (which is 4500g or more), matching the primary rule to classify as a Gentoo Penguin.`;
    } else if (billDepth >= 18) {
      speciesName = 'Adelie Penguin';
      emoji = '🐧';
      explanation = `The body mass is ${bodyMass}g (less than 4500g) and the bill depth is ${billDepth}mm (18mm or more), which matches the characteristics of an Adelie Penguin.`;
    } else {
      speciesName = 'Chinstrap Penguin';
      emoji = '🐧';
      explanation = `The body mass is ${bodyMass}g (less than 4500g) and the bill depth is ${billDepth}mm (less than 18mm), which matches the characteristics of a Chinstrap Penguin.`;
    }

    // 4. Populate & Reveal Result Card
    resultSpeciesName.textContent = speciesName;
    resultEmoji.textContent = emoji;
    resultSummary.textContent = `Based on the provided measurements, this penguin is most likely a ${speciesName}.`;
    resultExplanation.textContent = explanation;

    resultCard.classList.remove('hidden');
    resultCard.classList.add('revealed');
  });

  // Handle Clear Button Action
  clearBtn.addEventListener('click', () => {
    // Reset the form inputs
    predictionForm.reset();
    
    // Hide error container
    errorContainer.classList.add('hidden');
    
    // Hide result card and remove its reveal animation class
    resultCard.classList.add('hidden');
    resultCard.classList.remove('revealed');
  });

  // Helper function to display errors
  function showError(message) {
    errorMessage.textContent = message;
    errorContainer.classList.remove('hidden');
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
});
