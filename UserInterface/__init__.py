import json
from text_sniffer import load_abusive_words, detect_abuse

#THis file is excuted after the data is loaded from the social media platform
# It processes the data to detect abusive content and generates a report.

if __name__ == "__main__":
    # Load abusive words
    abusive_words = load_abusive_words("abusive_words.txt")
    
    file_path= "social_media_data.json"  # Path to the JSON file containing user text

# Open and read the file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content_list = json.load(file)  # Load list of post dictionaries
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
        exit(1)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        exit(1)
    report_dict = {}
    for index, item in enumerate(content_list):
        post_id = item.get('id', f'post_{index}')  # Use ID if available, else use fallback
        text = item.get('text') or item.get('caption')  # Prefer 'text', fallback to 'caption'

        if not text:
            print(f"Skipping post {post_id} — no text or caption found.")
            continue

        # Detect abusive content
        report = detect_abuse(text, abusive_words, similarity_threshold=0.6)
        report_dict[post_id] = {
            "original_text": text,
            "abuse_report": report
        }

    # Save the report
    with open("abuse_report.json", "w", encoding='utf-8') as f:
        json.dump(report_dict, f, indent=4, ensure_ascii=False)

    print("Analysis complete! Report saved to 'abuse_report.json'.")
