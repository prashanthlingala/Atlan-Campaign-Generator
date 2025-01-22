import streamlit as st
from content_generator import generate_content
from campaign_scheduler import create_campaign_schedule
from analytics import mock_engagement_metrics
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
st.title("AI-Powered Campaign Creation Tool")

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
# Step 5: Analytics Dashboard
if st.button("Show Analytics"):
    if not channels:
        st.error("Please select at least one channel to view analytics.")
    else:
        st.write("### Engagement Metrics")

        # Get mock analytics data
        engagement_metrics = mock_engagement_metrics(channels)

        # Create a table of metrics
        st.write("#### Metrics Table")
        for channel, metrics in engagement_metrics.items():
            st.subheader(f"{channel.capitalize()} Metrics")
            st.write(f"- **Total Impressions:** {metrics['Impressions']}")
            st.write(f"- **Click-Through Rate (CTR):** {metrics['CTR (%)']}%")
            st.write(f"- **Clicks:** {metrics['Clicks']}")
            st.write(f"- **Conversions:** {metrics['Conversions']}")
            st.write(f"- **Return on Investment (ROI):** {metrics['ROI (x)']}x")

        # Display Bar Chart for Impressions
        st.write("#### Impressions by Channel")
        impressions = {channel: metrics["Impressions"] for channel, metrics in engagement_metrics.items()}
        plt.bar(impressions.keys(), impressions.values())
        plt.title("Impressions by Channel")
        plt.xlabel("Channel")
        plt.ylabel("Total Impressions")
        st.pyplot(plt.gcf())

        # Display Bar Chart for CTR
        st.write("#### Click-Through Rate (CTR) by Channel")
        ctrs = {channel: metrics["CTR (%)"] for channel, metrics in engagement_metrics.items()}
        plt.bar(ctrs.keys(), ctrs.values())
        plt.title("Click-Through Rate (CTR) by Channel")
        plt.xlabel("Channel")
        plt.ylabel("CTR (%)")
        st.pyplot(plt.gcf())

