from apify_client import ApifyClient
import config
import requests

# API token
client = ApifyClient(config.api_key)

# Prepare the Actor input

run_input = {
    "searchStringsArray": ["restaurant"],
    "locationQuery": "New York, USA",
    "maxCrawledPlacesPerSearch": 10,
    "language": "en",
    "maxImages": 1,
    "maxReviews": 0,
    "maxQuestions": 0,
    "countryCode": "",
    "allPlacesNoSearchAction": "",
}

# Run the Actor and wait for it to finish
run = client.actor("compass/crawler-google-places").call(run_input=run_input)


# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)