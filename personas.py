personas = {
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

def get_persona_details(persona):
    return personas.get(persona, {"tone": "Neutral", "message": "General content."})
