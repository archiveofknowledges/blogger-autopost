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
    "Gastroenterology": ["Indigestion", "Gastritis", "Liver Disease", "Irritable Bowel Syndrome"],
    "Cardiology": ["Heart Disease", "Hypertension", "Heart Attack", "Arrhythmia"],
    "Pulmonology": ["Asthma", "COPD", "Pneumonia", "Lung Cancer"],
    "Endocrinology": ["Diabetes", "Thyroid Disorders", "Obesity", "Hormonal Imbalance"],
    "Obstetrics and Gynecology": ["Menstrual Pain", "Pregnancy Symptoms", "Polycystic Ovary Syndrome", "Menopause"]
}

def generate_health_post():
    field = random.choice(list(medical_fields.keys()))
    topic = random.choice(medical_fields[field])

    prompt = (
        f"Write a blog post in casual, natural HTML format about '{topic}' in the field of {field}. "
        "Make it sound like a real person sharing useful advice and experience. Avoid robotic tone. "
        "Use <h2>, <h3>, and <p> tags for structure. Include symptoms, causes, when to see a doctor, and lifestyle recommendations. "
        "Finish with some empathetic advice."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You're a friendly health blogger explaining medical issues in a way that feels personal and helpful."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1400
        )

        content = response.choices[0].message.content.strip()
        title = f"Why {topic} Happens, and How to Resolve {topic} Symptoms"
        tags = [field.lower(), topic.lower(), "health", "medical advice"]

        return {
            "title": title,
            "content": content,
            "category": field,
            "tags": tags
        }

    except Exception as e:
        print(f"❌ Error generating health post: {e}")
        return None
