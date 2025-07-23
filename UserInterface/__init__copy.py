# analyze.py

import json
import sys
import argparse
from text_sniffer import load_abusive_words, detect_abuse

def analyze_text(text, abusive_words):
    return detect_abuse(text, abusive_words, similarity_threshold=0.6)

def analyze_file(file_path, abusive_words):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content_list = json.load(file)
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        sys.exit(1)

    report_dict = {}
    for index, item in enumerate(content_list):
        post_id = item.get('id', f'post_{index}')
        text = item.get('text') or item.get('caption')
        if not text:
            print(f"Skipping post {post_id} — no text or caption found.")
            continue

        report = analyze_text(text, abusive_words)
        report_dict[post_id] = {
            "original_text": text,
            "abuse_report": report
        }

    with open("abuse_report.json", "w", encoding='utf-8') as f:
        json.dump(report_dict, f, indent=4, ensure_ascii=False)
    print("Batch analysis complete! Report saved to 'abuse_report.json'.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', type=str, help="Analyze a single user-provided text input")
    parser.add_argument('--file', type=str, help="Analyze a JSON file of posts")
    args = parser.parse_args()

    abusive_words = load_abusive_words("abusive_words.txt")

    if args.text:
        report = analyze_text(args.text, abusive_words)
        print(json.dumps({
            "original_text": args.text,
            "abuse_report": report
        }, ensure_ascii=False))
    elif args.file:
        analyze_file(args.file, abusive_words)
    else:
        print("Error: Provide either --text or --file input")
        sys.exit(1)

if __name__ == "__main__":
    main()
