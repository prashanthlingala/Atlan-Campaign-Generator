import random

def mock_engagement_metrics(channels):
    metrics = {}
    for channel in channels:
        impressions = random.randint(5000, 20000)  # Total impressions
        clicks = random.randint(100, 500)  # Total clicks
        conversions = random.randint(20, 100)  # Conversions
        roi = round(random.uniform(1.5, 5.0), 2)  # ROI (1.5x to 5.0x)

        # Calculate CTR
        ctr = round((clicks / impressions) * 100, 2)

        metrics[channel] = {
            "Impressions": impressions,
            "CTR (%)": ctr,
            "Clicks": clicks,
            "Conversions": conversions,
            "ROI (x)": roi,
        }
    return metrics
