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

function analyzeText() {
  const text = document.getElementById('inputText').value;
  if (!text.trim()) {
    alert('Please enter some text to analyze');
    return;
  }

  document.getElementById('results').innerHTML = `
    <strong>Analysis Complete:</strong><br/><br/>
    <strong>Sentiment:</strong> Positive<br/>
    <strong>Toxicity Score:</strong> 12%<br/>
    <strong>Abusive Language Detected:</strong> No<br/>
    <strong>Key Phrases:</strong> "great experience", "highly recommend"<br/><br/>
    <em>Note: This is a demo. Real analysis would use DistilBERT or similar model.</em>
  `;
}

function clearText() {
  document.getElementById('inputText').value = '';
  document.getElementById('results').innerHTML =
    'No analysis results yet<br/>Enter text and click analyze to begin';
}

