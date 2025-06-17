import json
from transformers import pipeline
from pathlib import Path
from datetime import datetime

class SentimentAnalyzer:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initialize the sentiment analyzer with a specified model.
        
        Args:
            model_name (str): HuggingFace model name/path for sentiment analysis.
                             Default is a general-purpose English sentiment model.
        """
        self.sentiment_analysis = pipeline("sentiment-analysis", model=model_name)
    
    def _extract_text(self, data, text_field="text"):
        """
        Extract text entries from various JSON structures.
        
        Args:
            data: Loaded JSON data (dict or list)
            text_field: Field name containing the text to analyze
            
        Returns:
            list: List of tuples with (id, text) pairs
        """
        entries = []
        
        # Handle list of dicts
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                if isinstance(item, dict):
                    text = item.get(text_field) or item.get('TEXT') or item.get('content') or next((v for k, v in item.items() if isinstance(v, str)), "")
                    entries.append((str(i), text))
        
        # Handle dict with IDs
        elif isinstance(data, dict):
            for id, item in data.items():
                if isinstance(item, dict):
                    text = item.get(text_field) or item.get('TEXT') or item.get('content') or next((v for k, v in item.items() if isinstance(v, str)), "")
                elif isinstance(item, str):
                    text = item
                else:
                    text = str(item)
                entries.append((str(id), text))
        
        return entries
    
    def _save_results(self, results, output_path=None, output_prefix="sentiment"):
        """
        Save results to JSON file.
        
        Args:
            results: Analysis results to save
            output_path: Directory to save results (None for current directory)
            output_prefix: Prefix for output filename
            
        Returns:
            str: Path to saved file
        """
        if output_path is None:
            output_path = Path.cwd()
        else:
            output_path = Path(output_path)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_path / f"{output_prefix}_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return str(output_file)
    
    def analyze_multi_word(self, json_data, text_field="text", save_results=False, output_path=None):
        """
        Analyzes the overall sentiment of text entries in JSON data.
        
        Args:
            json_data: Loaded JSON data (dict or list)
            text_field: Field name containing the text to analyze
            save_results: Whether to save results to JSON file
            output_path: Directory to save results
            
        Returns:
            dict: Analysis results in dictionary format
        """
        entries = self._extract_text(json_data, text_field)
        results = {"sentence_level": []}
        
        for entry_id, text in entries:
            if text:  # Only analyze non-empty text
                sentiment = self.sentiment_analysis(text)[0]
                result = {
                    "id": entry_id,
                    "text": text,
                    "label": sentiment['label'],
                    "score": float(sentiment['score']),
                    "analysis_level": "sentence"
                }
                results["sentence_level"].append(result)
        
        if save_results:
            saved_path = self._save_results(results, output_path, "sentence_level")
            print(f"Results saved to: {saved_path}")
        
        return results
    
    def analyze_word_level(self, json_data, text_field="text", save_results=False, output_path=None):
        """
        Analyzes sentiment at word level for text entries in JSON data.
        
        Args:
            json_data: Loaded JSON data (dict or list)
            text_field: Field name containing the text to analyze
            save_results: Whether to save results to JSON file
            output_path: Directory to save results
            
        Returns:
            dict: Analysis results in dictionary format
        """
        entries = self._extract_text(json_data, text_field)
        results = {"word_level": []}
        
        for entry_id, text in entries:
            if text:  # Only analyze non-empty text
                for word in text.split():
                    sentiment = self.sentiment_analysis(word)[0]
                    result = {
                        "id": entry_id,
                        "word": word,
                        "label": sentiment['label'],
                        "score": float(sentiment['score']),
                        "analysis_level": "word"
                    }
                    results["word_level"].append(result)
        
        if save_results:
            saved_path = self._save_results(results, output_path, "word_level")
            print(f"Results saved to: {saved_path}")
        
        return results
    
    def analyze(self, json_data, granularity="sentence", text_field="text", save_results=False, output_path=None):
        """
        Flexible sentiment analysis with configurable granularity.
        
        Args:
            json_data: Loaded JSON data (dict or list)
            granularity (str): 'sentence', 'word', or 'both'
            text_field: Field name containing the text to analyze
            save_results: Whether to save results to JSON file
            output_path: Directory to save results
            
        Returns:
            dict: Analysis results in dictionary format
        """
        entries = self._extract_text(json_data, text_field)
        results = {}
        
        if granularity in ["sentence", "both"]:
            results["sentence_level"] = []
        
        if granularity in ["word", "both"]:
            results["word_level"] = []
        
        for entry_id, text in entries:
            if not text:
                continue
                
            if granularity in ["sentence", "both"]:
                sent_sentiment = self.sentiment_analysis(text)[0]
                results["sentence_level"].append({
                    "id": entry_id,
                    "text": text,
                    "label": sent_sentiment['label'],
                    "score": float(sent_sentiment['score']),
                    "analysis_level": "sentence"
                })
            
            if granularity in ["word", "both"]:
                for word in text.split():
                    word_sentiment = self.sentiment_analysis(word)[0]
                    results["word_level"].append({
                        "id": entry_id,
                        "word": word,
                        "label": word_sentiment['label'],
                        "score": float(word_sentiment['score']),
                        "analysis_level": "word"
                    })
        
        if save_results:
            saved_path = self._save_results(results, output_path, f"sentiment_{granularity}")
            print(f"Results saved to: {saved_path}")
        
        return results


def load_json_file(file_path):
    """Helper function to load JSON data from a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Example Usage
if __name__ == "__main__":
    import sys
    
    # Initialize analyzer
    analyzer = SentimentAnalyzer()
    
    if len(sys.argv) > 1:
        # If file path provided as argument
        file_path = sys.argv[1]
        try:
            json_data = load_json_file(file_path)
            
            print("\nSentence-level analysis:")
            sentence_results = analyzer.analyze_multi_word(json_data, save_results=True)
            print(json.dumps(sentence_results, indent=2))
            
            print("\nWord-level analysis:")
            word_results = analyzer.analyze_word_level(json_data, save_results=True)
            print(json.dumps(word_results, indent=2))
            
            print("\nCombined analysis:")
            combined_results = analyzer.analyze(json_data, granularity="both", save_results=True)
            print(json.dumps(combined_results, indent=2))
                
        except Exception as e:
            print(f"Error processing file: {e}")
    else:
        # Use sample data if no file provided
        sample_data = {
            "1": {"TEXT": "You are not that stupid.", "Sentiment": "Positive", "Language": "EN"},
            "2": {"TEXT": "You are stupid", "Sentiment": "Negative", "Language": "EN"},
            "3": {"content": "Schiesse! du bist dumm", "Language": "DE"},
            "4": ["I", "hate", "nothing!"],
            "5": "algo esta mal",
            "6": {"message": "No eres tan inocente", "lang": "ES"}
        }
        
        print("No file provided. Using sample data.\n")
        
        print("Sentence-level analysis:")
        sentence_results = analyzer.analyze_multi_word(sample_data, save_results=True)
        print(json.dumps(sentence_results, indent=2))
        
        print("\nWord-level analysis:")
        word_results = analyzer.analyze_word_level(sample_data, save_results=True)
        print(json.dumps(word_results, indent=2))
        
        print("\nCombined analysis:")
        combined_results = analyzer.analyze(sample_data, granularity="both", save_results=True)
        print(json.dumps(combined_results, indent=2))