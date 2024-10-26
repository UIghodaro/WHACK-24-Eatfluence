from apify_client import ApifyClient
import config

# ========----- TikTok Scraper using APIFY -----======== #

# Initialize the ApifyClient with your API token
client = ApifyClient(config.api_key)

def tiktok_scrape():
    target_hashtag = "thedirtyduckwarwicksu"
    results_per_page = 5

    # Prepare the Actor input
    run_input = {
        "hashtags": [target_hashtag],
        "resultsPerPage": results_per_page,
        "excludePinnedPosts": False,
        "searchSection": "",
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
        print(item)