import os
import requests
from hubspot import HubSpot
import tweepy

# HubSpot Email Integration
def push_to_hubspot(email_subject, email_body, recipient_list):
    """
    Push email content to HubSpot for campaign creation.
    """
    client = HubSpot(api_key=os.getenv("HUBSPOT_API_KEY"))
    try:
        email_campaign = client.marketing_email.send_post(
            email={
                "subject": email_subject,
                "body": email_body,
                "recipients": recipient_list,
            }
        )
        return f"Email campaign created successfully! ID: {email_campaign['id']}"
    except Exception as e:
        return f"Error pushing to HubSpot: {e}"


# Twitter Posting Integration
def post_to_twitter(tweet_content):
    """
    Post content to Twitter using the Tweepy library.
    """
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.update_status(tweet_content)
        return "Tweet posted successfully!"
    except Exception as e:
        return f"Error posting to Twitter: {e}"


# LinkedIn Posting Integration
def post_to_linkedin(content):
    """
    Post content to LinkedIn using LinkedIn's API.
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {access_token}"}
    api_url = "https://api.linkedin.com/v2/ugcPosts"

    post_body = {
        "author": "urn:li:person:YOUR_PERSON_URN",  # Replace with your LinkedIn URN
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    try:
        response = requests.post(api_url, headers=headers, json=post_body)
        response.raise_for_status()
        return "Post published successfully to LinkedIn!"
    except Exception as e:
        return f"Error posting to LinkedIn: {e}"
