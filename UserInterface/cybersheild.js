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

function formatProcessedResult(processedResult) {
  let formatted = '';

  processedResult.forEach((entry) => {
    const sentimentClass = entry.sentiment.toLowerCase() === 'positive'
      ? 'sentiment-positive'
      : entry.sentiment.toLowerCase() === 'negative'
        ? 'sentiment-negative'
        : 'sentiment-neutral';

    formatted += `
      <div class="result-item">
        <p><strong>Text Analyzed:</strong> ${entry.original_text || 'N/A'}</p>
        <p><strong>Sentiment:</strong> 
          <span class="${sentimentClass}">
            ${entry.sentiment} (${(entry.confidence * 100).toFixed(2)}% confidence)
          </span>
        </p>
        <p><strong>Abusive Words Found:</strong> ${
          entry.abusive_words.length > 0
            ? entry.abusive_words.join(', ')
            : '<span style="color: green;">None</span>'
        }</p>
      </div>
      <hr/>
    `;
  });

  console.log('Formatted result:', formatted);
  return formatted;
}

async function analyzeText() {
  const text = document.getElementById('inputText').value;
  if (!text.trim()) {
    alert('Please enter some text to analyze');
    return;
  }

  document.getElementById('results').innerHTML = 'Analyzing...';

  try {
    console.log('Sending text to main process:', text);
    const rawResult = await window.api.analyzeText(text);
    console.log('Received result from main process:', rawResult);
    const parsedResult = JSON.parse(rawResult);
    console.log('Parsed result:', parsedResult);

    let processedResult;

    // Handle both single result and multiple entries
    if ('original_text' in parsedResult && 'abuse_report' in parsedResult) {
      const abuseReport = parsedResult.abuse_report || {};
      const abusiveWordsArray = abuseReport["abusive-words-found"] || abuseReport["abusive-words_found"] || [];

      const fallbackSentiment = abusiveWordsArray[0]?.sentiment?.sentiment || 'UNKNOWN';
      const fallbackConfidence = abusiveWordsArray[0]?.sentiment?.confidence || 0;
    
      processedResult = [
        {
          id: 'Single Input',
          original_text: parsedResult.original_text || '',
          text_analyzed: abuseReport.text_analyze || abusiveWordsArray[0]?.text_analyzed || parsedResult.original_text || '',
          sentiment: abuseReport.sentiment?.sentiment || fallbackSentiment,
          confidence: abuseReport.sentiment?.confidence || fallbackConfidence,
          abusive_words: abusiveWordsArray.map(wordInfo => wordInfo.word_in_text)
        }
      ];
    } else {
      // processedResult = extractAbuseAndSentimentInfo(parsedResult);
      console.log('Processed result:', processedResult);
    }

    const formattedResult = formatProcessedResult(processedResult);

    document.getElementById('results').innerHTML = `
      <strong>Analysis Results:</strong><br/>
      ${formattedResult}
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