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
    "Urology": ["Urinary Tract Infection", "Kidney Stones", "Prostate Health", "Bladder Issues"],
    "Gastroenterology": ["Indigestion", "Gastritis", "Liver Disease", "IBS"],
    "Cardiology": ["Heart Disease", "Hypertension", "Arrhythmia"],
    "Pulmonology": ["Asthma", "COPD", "Pneumonia"],
    "Endocrinology": ["Diabetes", "Thyroid Disorders", "Obesity"],
    "Obstetrics and Gynecology": ["Menstrual Pain", "Pregnancy Symptoms", "PCOS", "Menopause"]
}

def generate_health_post():
    field = random.choice(list(medical_fields.keys()))
    topic = random.choice(medical_fields[field])

    prompt = f"""
You are a compassionate and knowledgeable health blogger writing for an American audience.
Write an HTML-formatted blog post about the topic "{topic}" under the field of {field}.
Your tone should be reassuring, clear, and slightly conversational.
Avoid sounding robotic or overly clinical. Instead, aim for empathy and understanding.

The post should include:
- <h3>Common Symptoms</h3>
- <h3>Possible Causes or Related Conditions</h3>
- <h3>When to See a Doctor</h3>
- <h3>Home Remedies or Lifestyle Tips</h3>
- <h3>Conclusion</h3>

Wrap all explanations in <p> tags.
Finish with a <p> tag citing general health platforms like MayoClinic or WebMD.
Do not use Markdown or triple backticks.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a kind health writer helping readers understand common medical symptoms with empathy."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75,
            max_tokens=1400
        )

        content = response.choices[0].message.content.strip()
        content += f'\n<p style="font-size: 0.9em; color: gray;">Sources: Based on general medical literature and community-informed platforms (e.g., MayoClinic, WebMD, Reddit health forums).</p>'

        return {
            "title": f"{topic} — Symptoms, Causes & Tips",
            "content": content,
            "category": field,
            "tags": [field.lower(), topic.lower(), "health", "symptoms", "self-care"]
        }

    except Exception as e:
        print(f"❌ Error generating health post: {e}")
        return None
