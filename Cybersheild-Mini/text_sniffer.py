import json

# Step 1: Load abusive words from file
def load_abusive_words(file_path):
    with open(file_path, 'r') as file:
        return [word.strip().lower() for word in file.readlines()]

# Step 2: Check text for abusive words
def detect_abuse(text, abusive_words):
    detected = []
    words_in_text = text.lower().split()  # Split input text into words
    
    for word in abusive_words:
        if word in words_in_text:
            detected.append({
                "word": word,
                "severity": "high", 
                "text_analyzed": text 
                  # Move the text analyze into the dictionary itself. #implement sentiment analysis librays, # share the offensive model repo

            })
    if detected:
        return{
            'abusive-words-found':detected
        }
    else:
        return{
            "abusive-words_found":[],
            "text_analyze":text
        }
    # return {
    #     "abusive_words_found": detected,
    #     #"text_analyzed": text,
        
        
    

# Step 3: Main function (runs when script is executed)
if __name__ == "__main__":
    # Load abusive words
    abusive_words = load_abusive_words("abusive_words.txt")
    
    # Ask user for input
    user_text = input("Enter text to analyze: ")
    
    # Detect abusive words
    report = detect_abuse(user_text, abusive_words)
    
    # Save report to JSON
    with open("abuse_report.json", "w") as f:
        json.dump(report, f, indent=4)  # `indent=4` makes JSON readable
    
    print("Analysis complete! Report saved to 'abuse_report.json'.")