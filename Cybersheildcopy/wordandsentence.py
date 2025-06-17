from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initialize the sentiment analyzer with a specified model.
        
        Args:
            model_name (str): HuggingFace model name/path for sentiment analysis.
                             Default is a general-purpose English sentiment model.
        """
        self.sentiment_analysis = pipeline("sentiment-analysis", model=model_name)
    
    def analyze_multi_word(self, texts):
        """
        Analyzes the overall sentiment of multiple text entries.
        
        Args:
            texts (list of dict): List where each dict contains 'id' and 'text'
            
        Returns:
            list: Formatted strings with ID and sentiment label
        """
        results = []
        for entry in texts:
            sentiment = self.sentiment_analysis(entry['text'])[0]
            results.append(f"{entry['id']}:{sentiment['label']}")
        return results
    
    def analyze_word_level(self, texts):
        """
        Analyzes sentiment at word level for multiple text entries.
        
        Args:
            texts (list of dict): List where each dict contains 'id' and 'text'
            
        Returns:
            list: Formatted strings with ID, word, and sentiment label
        """
        results = []
        for entry in texts:
            for word in entry['text'].split():
                sentiment = self.sentiment_analysis(word)[0]
                results.append(f"{entry['id']} - {word}: {sentiment['label']}")
        return results
    
    def analyze(self, texts, granularity="sentence"):
        """
        Flexible sentiment analysis with configurable granularity.
        
        Args:
            texts (list of dict): List where each dict contains 'id' and 'text'
            granularity (str): 'sentence', 'word', or 'both'
            
        Returns:
            list: Formatted results based on granularity
        """
        results = []
        
        for entry in texts:
            text = entry['text']
            
            if granularity in ["sentence", "both"]:
                sent_sentiment = self.sentiment_analysis(text)[0]
                results.append(f"{entry['id']} (Sentence): {sent_sentiment['label']}")
            
            if granularity in ["word", "both"]:
                for word in text.split():
                    word_sentiment = self.sentiment_analysis(word)[0]
                    results.append(f"{entry['id']} - {word}: {word_sentiment['label']}")
                    
        return results


# Example Usage
if __name__ == "__main__":
    # Initialize analyzer (can configure with different model)
    analyzer = SentimentAnalyzer()
    
    # Sample data
    texts = [
         "1": {
            "TEXT": "You are not that stupid.",
            "Sentiment": "Positive",
            "Language": "EN"
        },
        "2": {
            "TEXT": "You are stupid",
            "Sentiment": "Negative",
            "Language": "EN"
        },
        "3": {
            "TEXT": "Schiesse! du bist dumm",
            "Sentiment": "Negative",
            "Language": "DE"
        },
        "4": {
            "TEXT": "I hate nothing!",
            "Sentiment": "Neutral",
            "Language": "EN"
        },
        "5": {
            "TEXT": "algo esta mal",
            "Sentiment": "Negative",
            "Language": "ES"
        },
        "6": {
            "TEXT": "No eres tan inocente",
            "Sentiment": "Neutral",
            "Language": "ES"}
    ]
    
    # Use different analysis methods
    print("Sentence-level analysis:")
    for result in analyzer.analyze_multi_word(texts):
        print(result)
    
    print("\nWord-level analysis:")
    for result in analyzer.analyze_word_level(texts):
        print(result)
    
    print("\nCombined analysis:")
    for result in analyzer.analyze(texts, granularity="both"):
        print(result)