import requests

# Twitter API Bearer Token
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAKvg2AEAAAAA%2BkQhuC70Y3jmb1YqUvvvjsG77PU%3DkXfYWh9ZVXAi6fGBCYvTXRYMzEi4APeT9ZfBxbpqYGMTi6qBwL'

headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}',
}
# Twitter Username to look up
username = "elonmusk"

# Step 1: Get User ID by Username
user_url = f"https://api.twitter.com/2/users/by/username/{username}"
user_response = requests.get(user_url, headers=headers)

# Print status and JSON for debugging
print(f"Status Code: {user_response.status_code}")
print("Response JSON:", user_response.json())

# Step 2: Extract User ID 
response_data = user_response.json()
if 'data' in response_data:
    user_id = response_data['data']['id']
    print(f"User ID: {user_id}")

    # Step 3: Get Tweets from User
    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": 5
    }
    tweets_response = requests.get(tweets_url, headers=headers, params=params)
    print("Recent Tweets:")

    for tweet in tweets_response.json().get("data", []):
        print("-", tweet["text"])
else:
    print("❌ Error: 'data' not found in response.")
    if 'errors' in response_data:
        print("Error details:", response_data['errors'])
