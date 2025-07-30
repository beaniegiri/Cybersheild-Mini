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

      // Dynamically insert styled results
    const abuseReport = result['abuse_report'] || {};
    const abusiveWords = abuseReport['abusive-words-found'] || [];
    const sentiment = abuseReport['sentiment'] || {sentiment: 'NEUTRAL', confidence: 0};

    const resultContent = `
      <div class="result-item">
        <span>Original Text:</span> ${result['original_text']}
      </div>
      <div class="result-item">
        <span>Sentiment:</span> 
        <span class="${sentiment.sentiment.toLowerCase() === 'positive' ? 'sentiment-positive' : 'sentiment-negative'}">
          ${sentiment.sentiment} (${(sentiment.confidence * 100).toFixed(2)}% confidence)
        </span>
      </div>
      <div class="result-item">
        <span>Abusive Words Found:</span> ${
          abusiveWords.length > 0
            ? abusiveWords
                .map(
                  (word) => `
                  <div>
                    <span>Word:</span> ${word.word_in_text}<br/>
                    <span>Matched With:</span> ${word.matched_with}<br/>
                    <span>Similarity:</span> ${(word.similarity * 100).toFixed(2)}%<br/>
                    <span>Severity:</span> <span class="severity-${word.severity.toLowerCase()}">${word.severity}</span>
                  </div>
                `
                )
                .join('')
            : 'None'
        }
      </div>
    `;

  
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

