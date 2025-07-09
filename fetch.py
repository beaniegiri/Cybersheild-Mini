import requests
import json

class Fetcher:
    def __init__(self, acess_token):
        self.access_token = acess_token
    
    def fetch(self, api_url):
        response = requests.get(api_url, params={'access_token': self.access_token})
        return response.json().get('data', [])

    def save_to_file(self, data, filename='social_media_data.json'):
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")


# Example usage:
if __name__ == "__main__":
    ACCESS_TOKEN = 'EAA4BJ7sqnR8BPNHDJfhZAC0PeSO3uKxMdhmUUYzI0o0vLCu5QK4394PH35lrwzlVLvF03UfziYeD5yqZAZBT7vDTVmJTU9msaylyCVEWbfCEdZB3AZCdZBuzn0UcuU9KbgMMOHev2lI46uZBr3jUiPKGoxdeZBMHMkmuvBZATPezB2AtQVjxvEZBa59Rxoi1ZBYrXC9VYP8'
    API_URL = 'https://graph.facebook.com/v19.0/17959954520806555/comments?fields=id,text,username,timestamp&access_token=EAA4BJ7sqnR8BPNHDJfhZAC0PeSO3uKxMdhmUUYzI0o0vLCu5QK4394PH35lrwzlVLvF03UfziYeD5yqZAZBT7vDTVmJTU9msaylyCVEWbfCEdZB3AZCdZBuzn0UcuU9KbgMMOHev2lI46uZBr3jUiPKGoxdeZBMHMkmuvBZATPezB2AtQVjxvEZBa59Rxoi1ZBYrXC9VYP8'


    fetcher = Fetcher(ACCESS_TOKEN)
    data = fetcher.fetch(API_URL)
    if data:
        fetcher.save_to_file(data)
    else:
        print("No data found or an error occurred.")
        print("Please check your access token and API URL.")
    print("Data fetching and saving completed.")