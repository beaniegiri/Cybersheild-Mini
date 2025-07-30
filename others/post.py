import requests
import time
import json

# BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAKvg2AEAAAAA%2BkQhuC70Y3jmb1YqUvvvjsG77PU%3DkXfYWh9ZVXAi6fGBCYvTXRYMzEi4APeT9ZfBxbpqYGMTi6qBwL'
# USERNAME = "elonmusk"  # Change to the desired user

# headers = {
#     "Authorization": f"Bearer {BEARER_TOKEN}",
# }

# # Step 1: Get user ID
# user_url = f"https://api.twitter.com/2/users/by/username/{USERNAME}"
# user_res = requests.get(user_url, headers=headers).json()

# if 'data' not in user_res:
#     print("Couldn't find user:", user_res.get("errors", user_res))
#     exit()

# user_id = user_res['data']['id']
# print(f"User ID for @{USERNAME}: {user_id}")


# # Step 2: Paginate through tweets
# tweets = []
# next_token = None
# max_pages = 10  # can increase this

# for _ in range(max_pages):
#     url = f"https://api.twitter.com/2/users/{user_id}/tweets"
#     params = {
#         "max_results": 100,
#         "pagination_token": next_token,
#         "tweet.fields": "created_at,text"
#     }
#     if not next_token:
#         params.pop("pagination_token")  # omit on first request

#     res = requests.get(url, headers=headers, params=params).json()

#     new_tweets = res.get("data", [])
#     tweets.extend(new_tweets)
#     print(f"📦 Fetched {len(new_tweets)} tweets (Total so far: {len(tweets)})")

#     next_token = res.get("meta", {}).get("next_token")
#     if not next_token:
#         break  # No more pages

#     time.sleep(1)  # Be kind to the API

# # Step 3: Show result
# print(f"\n✅ Total Tweets Retrieved: {len(tweets)}")
# for t in tweets:
#     print(f"{t['created_at']} — {t['text'][:80]}...")

# with open("user_tweets.json", "w", encoding="utf-8") as f:
#     json.dump(tweets, f, ensure_ascii=False, indent=4)

# print("✅ Tweets saved to user_tweets.json")


# import requests
# import time
# import json

# BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAKvg2AEAAAAAW5GCkV00qamgQTjyxsDXnKP2mgc%3DyeeQdKfIxiHu83ANk4gdEz2IbEvYqF3hENuTXdbTSgQAebnjDp'  # Replace with your actual token

# def fetch_user_tweets(username, max_pages=10, save_to_file=True, file_name=None):
#     """
#     Fetches tweets from a given Twitter username using Twitter API v2.

#     Args:
#         username (str): Twitter username (without @).
#         max_pages (int): Number of pages of tweets to fetch (100 tweets per page).
#         save_to_file (bool): Whether to save the tweets to a JSON file.
#         file_name (str): Custom filename to save tweets. Defaults to "<username>_tweets.json".

#     Returns:
#         list: List of tweet dictionaries (each with 'created_at' and 'text').
#     """
#     headers = {
#         "Authorization": f"Bearer {BEARER_TOKEN}",
#     }

#     # Step 1: Get user ID
#     user_url = f"https://api.twitter.com/2/users/by/username/{username}"
#     user_res = requests.get(user_url, headers=headers).json()

#     if 'data' not in user_res:
#         print(f"Couldn't find user: {user_res.get('errors', user_res)}")
#         return []

#     user_id = user_res['data']['id']
#     print(f"User ID for @{username}: {user_id}")

#     # Step 2: Fetch tweets
#     tweets = []
#     next_token = None

#     for _ in range(max_pages):
#         url = f"https://api.twitter.com/2/users/{user_id}/tweets"
#         params = {
#             "max_results": 100,
#             "pagination_token": next_token,
#             "tweet.fields": "created_at,text"
#         }
#         if not next_token:
#             params.pop("pagination_token")

#         res = requests.get(url, headers=headers, params=params).json()

#         new_tweets = res.get("data", [])
#         tweets.extend(new_tweets)
#         print(f"Fetched {len(new_tweets)} tweets (Total: {len(tweets)})")

#         next_token = res.get("meta", {}).get("next_token")
#         if not next_token:
#             break

#         time.sleep(1)  # API rate limiting

#     # Step 3: Save to file if needed
#     if save_to_file:
#         if not file_name:
#             file_name = f"{username}_tweets.json"
#         with open(file_name, "w", encoding="utf-8") as f:
#             json.dump(tweets, f, ensure_ascii=False, indent=4)
#         print(f"Tweets saved to {file_name}")

#     return tweets

# tweets = fetch_user_tweets("elonmusk", max_pages=5)
# for tweet in tweets[:3]:  # Just show first 3
#     print(f"{tweet['created_at']} — {tweet['text'][:100]}")
