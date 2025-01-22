import pandas as pd
from datetime import datetime, timedelta

def create_campaign_schedule(channels, start_date):
    schedule = []
    for i, channel in enumerate(channels):
        post_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        schedule.append({"Channel": channel, "Scheduled Date": post_date.strftime("%Y-%m-%d")})
    return pd.DataFrame(schedule)
