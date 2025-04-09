import openai
import random
import os

# OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Medical fields and topics definition (added Obstetrics and Gynecology)
medical_fields = {
    "Orthopedics": ["Knee Pain", "Back Pain", "Joint Disorders", "Fractures"],
    "Internal Medicine": ["Diabetes", "High Blood Pressure", "Asthma", "Chronic Fatigue Syndrome"],
    "Surgery": ["Appendicitis", "Gallstones", "Hernia", "Trauma Surgery"],
    "Ophthalmology": ["Cataracts", "Glaucoma", "Macular Degeneration", "Dry Eyes"],
    "Dermatology": ["Acne", "Eczema", "Psoriasis", "Skin Cancer"],
    "ENT": ["Ear Pain", "Sinusitis", "Tonsillitis", "Hoarseness"],  # ENT added
    "Urology": ["Urinary Tract Infection", "Kidney Stones", "Prostate Health", "Bladder Issues"],  # Urology added
    "Gastroenterology": ["Indigestion", "Gastritis", "Liver Disease", "Irritable Bowel Syndrome"],  # Gastroenterology added
    "Cardiology": ["Heart Disease", "Hypertension", "Heart Attack", "Arrhythmia"],  # Cardiology added
    "Pulmonology": ["Asthma", "COPD", "Pneumonia", "Lung Cancer"],  # Pulmonology added
    "Endocrinology": ["Diabetes", "Thyroid Disorders", "Obesity", "Hormonal Imbalance"],  # Endocrinology added
    "Obstetrics and Gynecology": ["Menstrual Pain", "Pregnancy Symptoms", "Polycystic Ovary Syndrome", "Menopause"]  # Obstetrics and Gynecology added
}

def generate_health_post():
    # Randomly select medical field and topic
    field = random.choice(list(medical_fields.keys()))
    topic = random.choice(medical_fields[field])
    
    # OpenAI API request to generate health-related content
    prompt = f"""
    Write a blog post in HTML format on the topic of {topic} under the field of {field}. 
    The blog post should include:
    - Common symptoms of {topic}
    - Possible causes or conditions related to {topic}
    - When to visit a doctor or specialist for {topic}
    - Recommended lifestyle modifications or treatments for managing {topic}
    - A conclusion with general advice on managing or preventing {topic}
    """

    try:
        response = openai.Completion.create(
            model="gpt-4-turbo",  # Using GPT-4 Turbo
            prompt=prompt,
            max_tokens=1000,  # Reasonable post length
            temperature=0.7  # Slight creativity
        )

        # Extract the generated content from OpenAI response
        content = response.choices[0].text.strip()

        # Generate title in the format "Topic symptoms and solution"
        title = f"Why {topic} Happens, and How to Resolve {topic} Symptoms"

        # Set tags
        tags = [field.lower(), topic.lower(), "health", "medical advice"]

        # HTML format content
        post_content = f"""
        <h3>Common Symptoms of {topic}</h3>
        <p>{content}</p>

        <h3>Possible Causes of {topic}</h3>
        <p>If you're experiencing {topic.lower()}, it might be caused by the following:</p>
        <ul>
            <li><strong>Possible Cause 1:</strong> Description of the cause.</li>
            <li><strong>Possible Cause 2:</strong> Description of the cause.</li>
            <li><strong>Possible Cause 3:</strong> Description of the cause.</li>
        </ul>

        <h3>When to Visit a Doctor</h3>
        <p>If symptoms persist or worsen, it is important to visit a <strong>{field} doctor</strong> or a specialist in {field.lower()}.</p>

        <h3>Lifestyle Modifications or Treatments</h3>
        <ul>
            <li><strong>Dietary Changes:</strong> Recommendations on diet.</li>
            <li><strong>Physical Activity:</strong> Exercise and movement suggestions.</li>
            <li><strong>Medications:</strong> Medications or treatments available for {topic.lower()}.</li>
        </ul>

        <p>In conclusion, understanding the causes of {topic.lower()} and making the necessary lifestyle changes can significantly reduce symptoms and improve quality of life.</p>
        """

        return {
            "title": title,
            "content": post_content,
            "category": field,
            "tags": tags
        }
    
    except Exception as e:
        print(f"❌ Error generating health post: {e}")
        return None
