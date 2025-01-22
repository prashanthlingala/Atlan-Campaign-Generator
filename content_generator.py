import openai
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_content(platform, campaign_goal, persona_message, tone, max_tokens=150):
    """
    Generate platform-specific content based on platform type, campaign goal, and persona details.
    """
    platform_prompts = {
        "Twitter": f"Write a concise and engaging tweet. Campaign Goal: {campaign_goal}. Tone: {tone}.",
        "LinkedIn": f"Write a professional and detailed LinkedIn post. Campaign Goal: {campaign_goal}. Message: {persona_message}. Tone: {tone}.",
        "Email": f"Write a formal email draft with a clear CTA. Campaign Goal: {campaign_goal}. Message: {persona_message}. Tone: {tone}.",
        "Webinar": f"Write a promotional message for a webinar invite. Campaign Goal: {campaign_goal}. Message: {persona_message}. Tone: {tone}.",
    }
    
    prompt = platform_prompts.get(platform, f"Write content for {platform}. Campaign Goal: {campaign_goal}. Tone: {tone}.")
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error generating content: {e}"
