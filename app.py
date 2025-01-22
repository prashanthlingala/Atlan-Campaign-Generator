import streamlit as st
from content_generator import generate_content
from campaign_scheduler import create_campaign_schedule
from analytics import mock_engagement_metrics
from integrations import push_to_hubspot, post_to_twitter, post_to_linkedin
import matplotlib.pyplot as plt

# Predefined Personas
predefined_personas = {
    "data_engineer": {
        "tone": "Technical and informative",
        "message": "Highlight collaborative features and technical specs."
    },
    "data_scientist": {
        "tone": "Insightful and data-driven",
        "message": "Focus on analytics capabilities and outcomes."
    },
    "business_leader": {
        "tone": "Impact-focused and concise",
        "message": "Emphasize ROI, business impact, and scalability."
    }
}

# Store custom personas in session state
if "custom_personas" not in st.session_state:
    st.session_state.custom_personas = {}

# Function to combine predefined and custom personas
def get_all_personas():
    return {**predefined_personas, **st.session_state.custom_personas}

# Sidebar for Persona Creation
st.sidebar.header("Create a Custom Persona")
persona_name = st.sidebar.text_input("Persona Name")
tone = st.sidebar.text_input("Tone (e.g., casual, professional)")
message = st.sidebar.text_area("Message (e.g., key focus areas for this persona)")
preferred_channels = st.sidebar.multiselect(
    "Preferred Channels", ["LinkedIn", "Twitter", "Email", "Webinar"]
)
if st.sidebar.button("Add Persona"):
    if persona_name and tone and message:
        st.session_state.custom_personas[persona_name] = {
            "tone": tone,
            "message": message,
            "preferred_channels": preferred_channels,
        }
        st.sidebar.success(f"Persona '{persona_name}' added!")
    else:
        st.sidebar.error("Please fill in all fields to create a persona.")

# Main App
st.title("Smart Personalized Automation for Remarkable Campaigns (S.P.A.R.C)")

# Step 1: Select Persona
st.header("1. Select a Persona")
personas = get_all_personas()
persona = st.selectbox("Choose a Persona", options=personas.keys())

# Step 2: Define Campaign Goal
st.header("2. Define Campaign Goal")
campaign_goal = st.text_input("Enter Campaign Goal (e.g., Announce a new feature)")
channels = st.multiselect(
    "Select Channels", ["LinkedIn", "Twitter", "Email", "Webinar"]
)
start_date = st.date_input("Select Start Date")

# Step 3: Generate AI Content
if st.button("Generate Content"):
    persona_details = personas[persona]
    tone = persona_details['tone']
    message = persona_details['message']

    st.write("### Generated Content")
    for channel in channels:
        prompt = f"{message} Campaign Goal: {campaign_goal}. Tone: {tone}."
        content = generate_content(prompt, max_tokens=150)
        st.write(f"**{channel} Post:** {content}")

# Step 4: Schedule Campaign
if st.button("Schedule Campaign"):
    if not channels or not start_date:
        st.error("Please select at least one channel and a start date.")
    else:
        schedule = create_campaign_schedule(channels, str(start_date))
        st.write("### Campaign Schedule")
        st.dataframe(schedule)

# Step 5: Analytics Dashboard
if st.button("Show Analytics"):
    if not channels:
        st.error("Please select at least one channel to view analytics.")
    else:
        st.write("### Campaign Performance")
        
        # Get mock analytics data
        engagement_metrics = mock_engagement_metrics(channels)
        
        # Display metrics as cards for each channel
        for channel, metrics in engagement_metrics.items():
            st.subheader(f"{channel.capitalize()} Metrics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(label="Total Impressions", value=f"{metrics['Impressions']:,}")
            with col2:
                st.metric(label="Click-Through Rate", value=f"{metrics['CTR (%)']}%")
            with col3:
                st.metric(label="Conversions", value=f"{metrics['Conversions']:,}")
            with col4:
                st.metric(label="ROI", value=f"{metrics['ROI (x)']}x")

        # Add a note to explain ROI or other terms if needed
        st.write("_Note: ROI (Return on Investment) is a ratio of revenue generated to campaign cost._")

# Step 6: Push content to Platforms
if st.button("Push Content to Platforms"):
    for channel in channels:
        content = generate_content(channel, campaign_goal, persona_details["message"], persona_details["tone"])
        st.write(f"Generated Content for {channel}: {content}")

        # Push content to respective platforms
        if channel == "Email":
            result = push_to_hubspot("Campaign Subject", content, ["recipient@example.com"])
        elif channel == "Twitter":
            result = post_to_twitter(content)
        elif channel == "LinkedIn":
            result = post_to_linkedin(content)
        else:
            result = f"No integration for {channel} yet."

        st.write(f"Result for {channel}: {result}")


