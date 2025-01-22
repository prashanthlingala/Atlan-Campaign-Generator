import random

def mock_engagement_metrics(channels):
    engagement = {}
    for channel in channels:
        engagement[channel] = random.randint(50, 100)  # Random engagement scores
    return engagement

