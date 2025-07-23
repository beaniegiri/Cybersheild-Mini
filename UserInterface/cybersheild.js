window.addEventListener('DOMContentLoaded', () => {
  console.log('DOM fully loaded and parsed');

  const analyzeBtn = document.getElementById('analyzeBtn');
  const clearBtn = document.getElementById('clearBtn');

  if (analyzeBtn) {
    analyzeBtn.addEventListener('click', analyzeText);
    console.log('Analyze button event listener added.');
  } else {
    console.warn('Element with id "analyzeBtn" not found on this page.');
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', clearText);
    console.log('Clear button event listener added.');
  } else {
    console.warn('Element with id "clearBtn" not found on this page.');
  }
});

async function analyzeText() {
  const text = document.getElementById('inputText').value;
  if (!text.trim()) {
    alert('Please enter some text to analyze');
    return;
  }

  document.getElementById('results').innerHTML = 'Analyzing...';

  try {
      console.log('Sending text to main process:', text); // Log input text
      const result = await window.api.analyzeText(text);
      console.log('Received result from main process:', result); // Log result
  
    // Update the results section with the analysis output
    document.getElementById('results').innerHTML = `
      <strong>Raw Output:</strong><br/>
      <pre>${result}</pre>
    `;
  } catch (error) {
    console.error('Error analyzing text:', error);
    document.getElementById('results').innerHTML = 'An error occurred during analysis.';
  }
    }


function clearText() {
  document.getElementById('inputText').value = '';
  document.getElementById('results').innerHTML =
    'No analysis results yet<br/>Enter text and click analyze to begin';
}

