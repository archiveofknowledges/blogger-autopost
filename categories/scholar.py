import openai
import os
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_scholar_post():
    # ✅ 다양한 분야의 무작위 학술 주제 리스트
    topics = [
        "The impact of climate change on Arctic ecosystems",
        "Shakespeare's influence on modern literature",
        "Advancements in civil engineering materials",
        "The neuroscience of memory formation",
        "Evolution of classical music theory in the 20th century",
        "Economic effects of universal basic income",
        "Genetic engineering and CRISPR applications",
        "Architectural trends in postmodern urban design",
        "Sociological perspectives on digital identity",
        "Philosophical foundations of existential ethics"
    ]
    selected_topic = random.choice(topics)

    prompt = (
        f"You are an academic writer. Generate a well-structured, long-form blog post on the topic: '{selected_topic}'. "
        "Format everything in clean HTML: use <h2> for the title, <h3> for each section heading, and wrap all paragraphs in <p> tags. "
        "Avoid Markdown. The post should include the following sections: Introduction, Literature Review, Methodology, Results and Discussion, Conclusion, and References (formatted as <ul><li>). "
        "Ensure the tone is professional and the text is clearly segmented."
    )

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1800
    )

    content = response.choices[0].message.content.strip()

    post = {
        "title": selected_topic,
        "content": content,
        "category": "scholar",
        "tags": ["Scholarship", "Education", "Research", "Humanities", "Science"]
    }
    return post
