import requests
import time
import json
import sys

class Fetcher:
    def __init__(self, acess_token):
        self.access_token = acess_token
    
    def fetch(self, api_url):
        try:
            response = requests.get(api_url, params={'access_token': self.access_token})
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def save_to_file(self, data, filename='social_media_data.json'):
        try: 
            with open(filename, 'a', encoding="utf-8") as file:
                json.dumps(data, file, indent=4, ensure_ascii=False)
            print(f"Data saved to {filename}")
        except IOError as e:
            print(f"Error saving data to file: {e}")
            sys.exit(1)


if __name__ == '__main__':
    access_token = sys.argv[1]
    api_url = sys.argv[2]
    fetcher = Fetcher(access_token)
    data = fetcher.fetch(api_url)
    # print(f"This is data is loading from the provided user API,/n {json.dumps(data)}")  # Output result to stdout
    print(data)
 


