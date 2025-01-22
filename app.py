import streamlit as st
from content_generator import generate_content
from personas import get_persona_details
from campaign_scheduler import create_campaign_schedule
from analytics import mock_engagement_metrics
import matplotlib.pyplot as plt

st.title("AI-Powered Campaign Creation Tool")

# Step 1: Define Campaign Goals
st.header("1. Define Campaign Goals")
persona = st.selectbox("Select Audience Persona", options=["data_engineer", "data_scientist", "business_leader"])
campaign_goal = st.text_input("Enter Campaign Goal (e.g., Announce a new feature)")
channels = st.multiselect("Select Channels", options=["LinkedIn", "Twitter", "Email", "Webinar"])
start_date = st.date_input("Select Start Date")

# Step 2: Generate AI Content
if st.button("Generate Content"):
    persona_details = get_persona_details(persona)
    tone = persona_details['tone']
    message = persona_details['message']

    st.write("### Generated Content")
    for channel in channels:
        prompt = f"{message} Campaign Goal: {campaign_goal}. Tone: {tone}."
        content = generate_content(prompt, channel)
        st.write(f"**{channel} Post:** {content}")

# Step 3: Schedule Campaign
if st.button("Schedule Campaign"):
    if not channels or not start_date:
        st.error("Please select at least one channel and a start date.")
    else:
        schedule = create_campaign_schedule(channels, str(start_date))
        st.write("### Campaign Schedule")
        st.dataframe(schedule)

# Step 4: Analytics Dashboard
if st.button("Show Analytics"):
    st.write("### Engagement Metrics")
    engagement = mock_engagement_metrics(channels)
    for channel, score in engagement.items():
        st.write(f"**{channel}:** {score}% engagement")
    plt.bar(engagement.keys(), engagement.values())
    plt.title("Engagement Metrics by Channel")
    plt.xlabel("Channels")
    plt.ylabel("Engagement Score (%)")
    st.pyplot(plt.gcf())
