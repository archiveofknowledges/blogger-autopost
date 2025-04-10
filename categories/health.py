import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

medical_fields = {
    "Orthopedics": ["Knee Pain", "Back Pain", "Joint Disorders", "Fractures"],
    "Internal Medicine": ["Diabetes", "High Blood Pressure", "Asthma", "Chronic Fatigue Syndrome"],
    "Surgery": ["Appendicitis", "Gallstones", "Hernia", "Trauma Surgery"],
    "Ophthalmology": ["Cataracts", "Glaucoma", "Macular Degeneration", "Dry Eyes"],
    "Dermatology": ["Acne", "Eczema", "Psoriasis", "Skin Cancer"],
    "ENT": ["Ear Pain", "Sinusitis", "Tonsillitis", "Hoarseness"],
    "Urology": ["UTI", "Kidney Stones", "Prostate Health", "Incontinence"],
    "Gastroenterology": ["Indigestion", "Gastritis", "Liver Disease", "IBS"],
    "Cardiology": ["Heart Disease", "Hypertension", "Arrhythmia", "Heart Attack"],
    "Pulmonology": ["Asthma", "COPD", "Pneumonia", "Lung Cancer"],
    "Endocrinology": ["Diabetes", "Thyroid Disorders", "Obesity", "Hormone Imbalance"],
    "Obstetrics and Gynecology": ["Menstrual Pain", "PCOS", "Menopause", "Pregnancy Symptoms"]
}

def generate_health_post():
    field = random.choice(list(medical_fields.keys()))
    topic = random.choice(medical_fields[field])

    prompt = f"""
    Write an empathetic and informative blog post in clean HTML format about '{topic}' in the field of {field}.
    Use <h3> for headings and <p> for paragraphs. Write in a helpful, slightly conversational tone to sound human-like.
    Vary sentence lengths and paragraph sizes. Cover:
    - Common symptoms
    - Possible causes
    - When to see a doctor
    - Lifestyle or treatment options
    - Final takeaway

    Do not use Markdown or triple backticks. Close with a short reference note like: “Based on health info from Mayo Clinic, WebMD, and community health forums.”
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly health blogger writing for general readers in the U.S."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
            max_tokens=1400
        )

        content = response.choices[0].message.content.strip()
        content += '\n<p style="font-size: 0.9em; color: gray;">Sources: Based on public health resources (Mayo Clinic, WebMD, Reddit Health threads).</p>'

        return {
            "title": f"Understanding {topic}: Symptoms, Causes, and What to Do",
            "content": content,
            "category": field,
            "tags": [field.lower(), topic.lower(), "health", "medical advice"]
        }

    except Exception as e:
        print(f"❌ Error generating health post: {e}")
        return None
