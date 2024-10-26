from apify_client import ApifyClient
import config
import requests

# Define your Hugging Face API token
api_token = config.api_token
# Define the endpoint and headers for the request
headers = {"Authorization": f"Bearer {api_token}"}
url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

def analyse_food_relation(text):
    labels = ["restaurant"]

    # Set up the payload for the API request
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": labels},
    }

    # Make the POST request to the Hugging Face API
    response = requests.post(url, headers=headers, json=payload)

    # Parse and print the results
    if response.status_code == 200:
        result = response.json()
        for label, score in zip(result['labels'], result['scores']):
            return score
    else:
        return 0
    

# ========----- TikTok Scraper using APIFY -----======== #

# Initialize the ApifyClient with your API token
client = ApifyClient(config.api_key)

def tiktok_scrape(search_query):
    results_per_page = 5

    # Prepare the Actor input
    run_input = {
        "hashtags": [search_query],
        "resultsPerPage": results_per_page,
        "excludePinnedPosts": False,
        "searchSection": "/video",
        "maxProfilesPerQuery": 10,
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadSlideshowImages": False,
        "proxyCountryCode": "None",
    }

    # Run the Actor and wait for it to finish
    run = client.actor("GdWCkxBtKWOsKjdch").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if 'text' in item:
            text = item.get('text', "No text available in this item")
        
            sentiment_score = analyse_food_relation(text)
            if sentiment_score > 0.45:
                print(text)
                print("With score of: " + str(sentiment_score))
                print("======================================================")

if __name__ == "__main__":
    tiktok_scrape("The Dirty Duck")
    tiktok_scrape("Benugo Bar & Kitchen at Warwick Arts Centre")
    tiktok_scrape("Varsity")
    tiktok_scrape("Bar Fusion")
    tiktok_scrape("Pret A Manger")



